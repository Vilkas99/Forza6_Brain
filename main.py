from flask import Flask
from flask.json import jsonify
from flask_restful import Api, Resource
from Mesa.brain import Vecindad

app = Flask(__name__)
api = Api(app)

#Avance M5
modelado = []

@app.route("/createModel", methods=["POST"])
def create():
    modelado.append(Vecindad())
    return 'ok', 201

@app.route("/getStepInfo", methods = ["GET"])
def stepInfo():
    if (len(modelado) == 0):
        return 'error: No hay ningún modelo', 404
    else:
        vecindad = modelado[0]
        vecindad.step()
        return jsonify({"paso": vecindad.paso})


if __name__ == "__main__": 
    app.run(debug=True)
