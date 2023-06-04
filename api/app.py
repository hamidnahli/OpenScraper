"""
- run spider http://127.0.0.1/run
- list all runs http://127.0.0.1/run_status
- display data for a single run http://127.0.0.1/run_status/2
- filter database
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from spiders.coingecko import run_scraper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class ScraperRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='Not started')
    records = db.relationship('CoinGeckoRecord', backref='run')


class CoinGeckoRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey('run.id'))
    name = db.Column(db.String(150))
    url = db.Column(db.Text)
    block_explorer = db.Column(db.Text)
    discord = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    telegram = db.Column(db.String(150))
    Website = db.Column(db.Text)
    contract = db.Column(db.Text)


@app.route('/run', methods=['POST'])
def start_scraper():
    # create a record for the run the ScraperRun table/db
    run = ScraperRun()
    # run = {id: 1, 'status': Not started, records: None
    db.session.add(run)
    db.session.commit()

    # change status
    # run = {id: 1, 'status': running, records: None
    run.status = 'running'
    db.session.commit()
    data = run_scraper()
    # save to db
    for record in data:
        new_record = CoinGeckoRecord(run_id=run.id, **record)
        db.session.add(new_record)
    # change run status
    # run = {id: 1, 'status':  complete, records: data}
    run.status = 'complete'
    db.session.commit()

    return jsonify({'run_id': run.id})


@app.route('/run_status', methods=['GET'])
def run_status():
    return {'scraer': 'CoinGecko', 'run_id': 1, 'status': 'finished'}


app.run(debug=True)
