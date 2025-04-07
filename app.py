from flask import Flask, render_template, request
from utils import process_pmids
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    clusters = []
    associations = {}
    if request.method == 'POST':
        pmid_input = request.form.get('pmids', '')
        pmids = [p.strip() for p in pmid_input.split(',') if p.strip()]
        clusters, associations = process_pmids(pmids)
    return render_template('index.html', clusters=json.dumps(clusters), associations=json.dumps(associations))

if __name__ == '__main__':
    app.run(debug=True)