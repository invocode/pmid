# PMID Clustering Web App

This is a Flask-based web application that accepts a list of PMIDs, fetches related GEO datasets, processes their metadata using TF-IDF and KMeans clustering, and displays a simple cluster visualization.

## Features
- Uses NCBI e-utils API to link PMIDs to GEO datasets
- Extracts metadata (title, summary, design, organism)
- Clusters datasets using TF-IDF + KMeans
- Simple interactive visualization (Plotly)

## Installation

```bash
git clone https://github.com/your/repo.git
cd pmid_clustering
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Example input
```
25404168, 30049270, 20090727
```