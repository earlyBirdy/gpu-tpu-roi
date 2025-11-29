# GPU vs TPU – ROI-Based Selection Web (FastAPI + Static)

This repo provides a clean, ROI-driven comparison between **NVIDIA GPUs** and **Google TPUs**.

It includes:

- A **FastAPI web app** that renders Markdown docs and exposes an interactive ROI calculator API.
- A **static docs pipeline** (`scripts/build_static.py`) that converts Markdown in `docs/` to HTML in `site/`.
- A simple folder structure you can extend with diagrams and custom CSS.

## Structure

- `README.md` – this file
- `app/main.py` – FastAPI application
- `docs/` – Markdown source content  
  - `index.md` – main landing page  
  - `roi_tables.md` – ROI model & tables  
  - `decision_tree.md` – accelerator decision tree  
  - `business_summary.md` – business & GTM view  
  - `diagrams/` – SVG placeholders for diagrams  
  - `css/style.css` – basic styling for static HTML
- `scripts/build_static.py` – build script for static HTML
- `site/` – generated HTML pages (static version)
- `requirements.txt` – Python dependencies

## Run FastAPI App

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:

- `/` – main landing page (Markdown → HTML)
- `/roi` – ROI tables  
- `/decision` – decision tree  
- `/business` – business summary  
- `/api/roi` – interactive ROI calculator (JSON)

Example ROI call:

```bash
curl "http://localhost:8000/api/roi?flex=5&eco=5&training=4&cost=4&latency=5&ops=5"
```

## Build Static HTML

```bash
python scripts/build_static.py
```

This will populate `site/` with:

- `index.html`  
- `roi.html`  
- `decision.html`  
- `business.html`
