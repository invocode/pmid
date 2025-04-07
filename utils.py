import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import time

def get_gse_ids(pmid):
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
    params = {
        'dbfrom': 'pubmed',
        'db': 'gds',
        'linkname': 'pubmed_gds',
        'id': pmid,
        'retmode': 'xml'
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.content, 'xml')
    return [i.text for i in soup.find_all('Id')]

def get_gse_metadata(gse_id):
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
    params = {
        'db': 'gds',
        'id': gse_id,
        'retmode': 'json'
    }
    r = requests.get(url, params=params)
    data = r.json()
    doc = data['result'].get(gse_id)
    if doc:
        fields = [doc.get(k, '') for k in ['title', 'summary', 'overall_design', 'taxon', 'gse']]
        return ' '.join(fields)
    return ''

def process_pmids(pmids):
    texts = []
    labels = []
    pmid_to_gse = {}
    for pmid in pmids:
        try:
            gse_ids = get_gse_ids(pmid)
            pmid_to_gse[pmid] = gse_ids
            for gse in gse_ids:
                text = get_gse_metadata(gse)
                if text:
                    texts.append(text)
                    labels.append((gse, pmid))
            time.sleep(0.34)
        except Exception as e:
            print(f"Error with PMID {pmid}: {e}")
    if not texts:
        return [], {}

    vec = TfidfVectorizer(stop_words='english')
    X = vec.fit_transform(texts)
    km = KMeans(n_clusters=3, random_state=42).fit(X)

    clusters = []
    for i, (gse, pmid) in enumerate(labels):
        clusters.append({'label': f"{gse}", 'cluster': int(km.labels_[i])})

    return clusters, pmid_to_gse