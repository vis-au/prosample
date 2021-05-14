from datetime import datetime
from flask import Flask, jsonify, request
import numpy as np
from numpy.random import uniform
import random

app = Flask(__name__)


RANDOM_DATASET_SIZE = 1000000
RANDOM_DATASET_DIMENSIONS = 10
RANDOM_SAMPLE = uniform(0, 1, RANDOM_DATASET_SIZE * RANDOM_DATASET_DIMENSIONS)
RANDOM_DATASET = RANDOM_SAMPLE.reshape((RANDOM_DATASET_SIZE, RANDOM_DATASET_DIMENSIONS))

indexes = np.arange(0, RANDOM_DATASET_SIZE)

# vectors indicating, which elements of the random dataset have already been sampled
sampling_a = np.zeros(RANDOM_DATASET_SIZE)
sampling_b = np.zeros(RANDOM_DATASET_SIZE)


@app.route('/')
def hello_world():
  return 'Ok. Flask server successfully launched.'

@app.route('/sample', methods=["GET"])
def sample():
  sample_size = int(request.args.get("size"))
  sampling = sampling_a if request.args.get("sample") == "a" else sampling_b

  remaining_points = []
  for i in indexes:
    if sampling[i] == 0:
      remaining_points.append(i)

  sampled_indeces = random.sample(remaining_points, sample_size)
  sampled_data = [RANDOM_DATASET[i].tolist() for i in sampled_indeces]
  sampling[np.array(sampled_indeces)] = 1

  timestamp = datetime.now()
  payload = {
    "timestamp": str(timestamp),
    "sample": sampled_data
  }

  response = jsonify(payload)
  response.headers.add("Access-Control-Allow-Origin", "*")

  return response


if __name__ == "__main__":
  app.run()