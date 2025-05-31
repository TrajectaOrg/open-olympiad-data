from pathlib import Path
import xml.etree.ElementTree as ET
import psycopg2
from psycopg2.extras import execute_batch
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

DB_PARAMS = {
    'dbname':   os.environ.get('DB_NAME'),
    'user':     os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
    'host':     os.environ.get('DB_HOST'),
    'port':     os.environ.get('DB_PORT'),
}

def safe_int(text):
    """
    Convert `text` to int, or return None on failure.
    """
    try:
        return int(text)
    except (TypeError, ValueError):
        return None


def parse_and_insert(xml_folder):
    """
    Parse every .xml in `xml_folder`, build a row dict (including olympiad='IMO'),
    and batch‐upsert into alumni.
    """
    insert_sql = """
        INSERT INTO alumni (
            id, olympiad,
            imo_id, year, country,
            imo_problem1, imo_problem2, imo_problem3,
            imo_problem4, imo_problem5, imo_problem6,
            imo_total, name, surname, medal
        ) VALUES (
            %(id_real)s, %(olympiad)s,
            %(id)s, %(year)s, %(country)s,
            %(p1)s, %(p2)s, %(p3)s,
            %(p4)s, %(p5)s, %(p6)s,
            %(total)s, %(name)s, %(surname)s, %(medal)s
        )
    """

    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(MAX(id), 0) FROM alumni;")
            last_id = cur.fetchone()[0]
    x = last_id + 1

    rows = []
    for xml_path in sorted(Path(xml_folder).glob("*.xml")):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        year = safe_int(root.attrib.get('year'))

        # if year != 2000:
        #     continue

        print(year)
        for contestant in root.findall('contestant'):
            rows.append({
                'olympiad': 'IMO',                             # satisfy NOT NULL
                'id':        safe_int(contestant.get('id')),
                'year':      year,
                'country':   contestant.findtext('code'),
                'p1':        safe_int(contestant.findtext('problem1')),
                'p2':        safe_int(contestant.findtext('problem2')),
                'p3':        safe_int(contestant.findtext('problem3')),
                'p4':        safe_int(contestant.findtext('problem4')),
                'p5':        safe_int(contestant.findtext('problem5')),
                'p6':        safe_int(contestant.findtext('problem6')),
                'total':     safe_int(contestant.findtext('total')),
                'name':      contestant.findtext('name'),
                'surname':   contestant.findtext('surname'),
                'medal':   contestant.findtext('award'),
                'id_real': x
            })
            x+=1

    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            execute_batch(cur, insert_sql, rows, page_size=500)
        conn.commit()


if __name__ == "__main__":
    parse_and_insert('IMO_xml/imo_xml')
    print("✅ IMO data imported and upserted successfully.")
