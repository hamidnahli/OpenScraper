"""
- run spider http://127.0.0.1/run
- list all runs http://127.0.0.1/run_status
- display data for a single run http://127.0.0.1/run_status/2
- filter database
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from spiders.amazon import run_scraper 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class scraperRun(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(50), default = 'Not started')
    record = db.relationship('amazonRecord', backref = 'run')

class amazonRecord(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    run_id = db.Column(db.Integer, db.Foreignkey('run.id'))
    title = db.column(db.String(150))
    rating = db.Column(db.String(150))
    price = db.Column(db.Integer(150))
    real_price = db.Column(db.String(150))
    delivery_price = db.Column(db.integer(150))

@app.route('/run', methods=['POST'])
def Start_scraper():
    run = scraperRun()
    db.session.add(run)
    db.session.commit()
    
    run.status = 'runing'
    db.session.commit()
    data = run_scraper()

    for record in data :
        new_record = amazonRecord(run_id = run.id, **record)
        db.session.add(new_record)
    run.status = 'complet'
    db.session.commit()

    return jsonify({'run_id':run.id})

# @app.route('/run_status', methods=['GET'])
# def run_status():
#     return {'scraer': 'amazon', 'run_id': 1, 'status': 'finished'}

app.run(debug=True)
