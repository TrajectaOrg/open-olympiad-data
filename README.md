
<h1 align="center">
  <img src="https://trajecta.org/img/logo.svg" width="60"/>
  <br/>
  open‑olympiad‑data
</h1>

<p align="center">
  <b>The missing public dataset for every International Science Olympiad.</b><br/>
  Pull → Parse → Load — in one command.
</p>

---

## 🚀 Features
|  |  |
|---|---|
| **All major Olympiads** | Math (IMO), Physics (IPhO), Chemistry (IChO), Biology (IBO), Informatics (IOI) — more coming. |
| **Pluggable extractors** | Each scraper is a self‑contained Python module ⇒ add new contests in minutes. |
| **Single‑command ETL** | `make postgres` streams everything into a normalized DB (Docker‑compose included). |
| **Data Lake‑ready** | Auto‑exports to <kbd>CSV</kbd>, <kbd>Parquet</kbd>, or <kbd>ndjson</kbd>. |
| **Type‑hinted & tested** | 90 %+ coverage, CI on push, mypy clean. |
| **Open license** | Apache‑2.0 — use it for papers, dashboards, startups. |

---

## 🏁 Quick‑start

```bash
git clone https://github.com/TrajectaOrg/open-olympiad-data
cd open-olympiad-data
pip install -r requirements.txt   # Python 3.10+
python run.py --csv               # dumps fresh CSVs to ./data
````

### Postgres snapshot (Docker)

```bash
docker compose up -d       # spins PG at localhost:5432
python run.py --pg         # streams data into postgres://trajecta/olympiads
```

---

## 📂 Repo layout

```
.
├─ scrapers/
│  ├─ imo_scraper.py       # XML → dict
│  ├─ ipho_scraper.py      # HTML tables → dict
│  ├─ icho_scraper.py      # PDF → OCR → dict
│  ├─ ibo_scraper.py
│  └─ ioi_scraper.py
├─ pipelines/
│  ├─ etl.py               # common load helpers
│  └─ models.sql           # DB schema
├─ data/                   # auto‑generated output
└─ run.py                  # unified CLI
```

---

## 🔍 Sample query

```sql
-- Who scored perfect 42 at IMO since 2000?
SELECT name, surname, country, year
FROM imo_results
WHERE total = 42 AND year >= 2000
ORDER BY year;
```

---

## 🤝 Contributing

1. Fork & create a feature branch.
2. `make dev && make test`
3. Send a PR — all humans welcome, even first‑timers.

Need a new Olympiad? Open an issue with the site URL or sample HTML and we’ll help you wire an extractor.

---

## 🌐 Citing

If you use this dataset in research, please cite:

```
@misc{open-olympiad-data,
  author       = {Trajecta Org},
  title        = {Open Olympiad Data},
  year         = {2025},
  howpublished = {\url{https://github.com/TrajectaOrg/open-olympiad-data}}
}
```

---

<p align="center">
  <i>Made with ❤️ by Olympiad alumni — to help the next generation bend their trajectories.</i>
</p>
