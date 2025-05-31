import csv
import psycopg2
from psycopg2.extras import execute_batch
import os

# ——————————————————————————————————————————————————————————————————————
# DB connection parameters (same as IMO upload)
DB_PARAMS = {
    'dbname':   os.environ.get('DB_NAME',   'trajecta'),
    'user':     os.environ.get('DB_USER',   'postgres'),
    'password': os.environ.get('DB_PASS',   'Astrosander12!'),
    'host':     os.environ.get('DB_HOST',   'imagesharing.c1ig8myqybl5.us-east-2.rds.amazonaws.com'),
    'port':     os.environ.get('DB_PORT',   '5432'),
}

def process_medal(text):
    """
    Process medal text to standardize values.
    """
    if text == 'G':
        return 'Gold Medal'
    elif text == 'S':
        return 'Silver Medal'
    elif text == 'B':
        return 'Bronze Medal'
    elif text == 'H':
        return 'Honorable Mention'
    else:
        return None


def safe_float(text):
    """
    Convert `text` to float, or return None on failure.
    """
    try:
        if text is None or text.strip() == '':
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def safe_int(text):
    """
    Convert `text` to int, or return None on failure.
    """
    try:
        if text is None or text.strip() == '':
            return None
        return int(text)
    except (TypeError, ValueError):
        return None


def parse_name(full_name):
    """
    Split full name into name and surname.
    """
    if not full_name:
        return None, None
    
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], None
    elif len(parts) >= 2:
        # First part is name, rest is surname
        name = parts[0]
        surname = ' '.join(parts[1:])
        return name, surname
    else:
        return None, None


def upload_ipho_data(csv_file_path='estudiantes.csv'):
    """
    Read the IPhO CSV file and upload data to the alumni database.
    CSV format: year, rank, name, country, medal, ipho_theory, ipho_experimental, ipho_overall
    """
    
    # SQL for inserting IPhO data
    insert_sql = """
        INSERT INTO alumni (
            id, olympiad, year, rank, name, surname, country, medal,
            ipho_theory, ipho_experimental, ipho_overall
        ) VALUES (
            %(id)s, %(olympiad)s, %(year)s, %(rank)s, %(name)s, %(surname)s, 
            %(country)s, %(medal)s, %(ipho_theory)s, %(ipho_experimental)s, %(ipho_overall)s
        );
    """
    
    # Get the next available ID
    with psycopg2.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(MAX(id), 0) FROM alumni;")
            last_id = cur.fetchone()[0]
    
    current_id = last_id + 1
    rows = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            
            for row_num, row in enumerate(csv_reader, 1):
                if len(row) < 5:
                    print(f"Skipping row {row_num}: insufficient columns")
                    continue
                
                # Parse CSV columns
                year = safe_int(row[0])
                rank = row[1].strip() if len(row) > 1 else None
                full_name = row[2].strip() if len(row) > 2 else None
                country = row[3].strip() if len(row) > 3 else None
                medal = row[4].strip() if len(row) > 4 else None
                
                # Parse IPhO scores (if available)
                ipho_theory = safe_float(row[5]) if len(row) > 5 else None
                ipho_experimental = safe_float(row[6]) if len(row) > 6 else None
                ipho_overall = safe_float(row[7]) if len(row) > 7 else None
                
                # Skip rows with invalid data
                if not year or not full_name:
                    print(f"Skipping row {row_num}: missing year or name")
                    continue
                
                # Parse name into first and last name
                name, surname = parse_name(full_name)
                
                # Normalize medal values
                if medal:
                    medal = medal.upper()
                    if medal not in ['G', 'S', 'B', 'H']:
                        medal = None
                
                row_data = {
                    'id': current_id,
                    'olympiad': 'IPhO',
                    'year': year,
                    'rank': rank,
                    'name': name,
                    'surname': surname,
                    'country': country,
                    'medal': process_medal(medal),
                    'ipho_theory': ipho_theory,
                    'ipho_experimental': ipho_experimental,
                    'ipho_overall': ipho_overall
                }
                
                rows.append(row_data)
                current_id += 1
                
                if row_num % 1000 == 0:
                    print(f"Processed {row_num} rows...")
    
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_file_path}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Batch insert the data
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                execute_batch(cur, insert_sql, rows, page_size=500)
            conn.commit()
        
        print(f"✅ Successfully uploaded {len(rows)} IPhO records to the database.")
        
    except Exception as e:
        print(f"Error uploading to database: {e}")


if __name__ == "__main__":
    upload_ipho_data('IPhO/estudiantes.csv')
