import os
import requests
from time import sleep

def download_imo_xml(year: int, out_dir: str = "imo_xml"):
    """Download and save the individual-results XML for a given IMO year."""
    url = "https://www.imo-official.org/year_individual_r.aspx"
    params = {
        "year": year,
        "column": "total",
        "order": "desc",
        "download": "XML"
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()

    # make sure output directory exists
    os.makedirs(out_dir, exist_ok=True)

    path = os.path.join(out_dir, f"{year}.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(f"✅ {year} → {path}")

if __name__ == "__main__":
    for y in range(2016, 2025):
        try:
            download_imo_xml(y)
            # be gentle on the server
            sleep(0.5)
        except Exception as e:
            print(f"❌ {y} failed: {e}")
