from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from py_eureka_client import eureka_client

app_reclamation = Flask(__name__)
app_reclamation.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/db-related-entities'
app_reclamation.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app_reclamation)

# Your Eureka server URL
eureka_server = "http://localhost:8081/eureka"

# Register this service to eureka server
eureka_client.init(eureka_server=eureka_server,
                   app_name="reclamation-micro-service",
                   instance_port=5050)

class Reclamation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    sujet = db.Column(db.String(100), nullable=False)

with app_reclamation.app_context():
    db.create_all()

@app_reclamation.route('/reclamations', methods=['POST'])
def ajouter_reclamation():
    data = request.get_json()

    nouveau_nom = data.get('nom')
    nouveau_sujet = data.get('sujet')

    nouvelle_reclamation = Reclamation(nom=nouveau_nom, sujet=nouveau_sujet)

    db.session.add(nouvelle_reclamation)
    db.session.commit()

    return jsonify({'message': 'Réclamation ajoutée avec succès'}), 201

@app_reclamation.route('/reclamations', methods=['GET'])
def obtenir_reclamations():
    reclamations = Reclamation.query.all()
    result = []
    for reclamation in reclamations:
        reclamation_data = {'id': reclamation.id, 'nom': reclamation.nom, 'sujet': reclamation.sujet}
        result.append(reclamation_data)

    return jsonify({'reclamations': result})

@app_reclamation.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is your Flask service!'})
instance = {
        'app': 'reclamation-micro-service',
        'ipAddr': '127.0.0.1',  
        'port': 5050,
        # Add other relevant information as needed
    }
if __name__ == '__main__':
    eureka_client.register(eureka_server=eureka_server,instance=instance)
    app_reclamation.run(host='0.0.0.0', port=5050)
