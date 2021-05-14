from datetime import datetime
from flask import Flask, jsonify, request
from numpy.random import uniform

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Ok. Flask server successfully launched.'

@app.route('/sample', methods=["GET"])
def sample():
  sample_size = int(request.args.get("size"))

  x = uniform(0, 1, sample_size * 4)
  random_items = x.reshape((sample_size, 4)).tolist()

  timestamp = datetime.now()
  sample = {
    "timestamp": str(timestamp),
    "sample": random_items
  }

  response = jsonify(sample)
  response.headers.add("Access-Control-Allow-Origin", "*")

  return response


if __name__ == "__main__":
  app.run()