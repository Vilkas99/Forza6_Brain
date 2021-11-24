from flask import Flask
from flask.json import jsonify
from flask_restful import Api, Resource
from Mesa.main import Vecindad

app = Flask(__name__)
api = Api(app)


modelado = []

class InfoModelo(Resource):
        
    def get(self):
        miVecindad = modelado[0]
        if len(miVecindad) == 0:
            return {'error': "No hemos instanciado ninguna vecindad"}
        else: 
            return {'paso': miVecindad.paso}
  
    
    def post(self):
        modelado.append(Vecindad())
        return {"data": "Incializado"}

api.add_resource(InfoModelo, "/InfoModelo")

if __name__ == "__main__": 
    app.run(debug=True)