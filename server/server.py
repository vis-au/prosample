from datetime import datetime
from flask import Flask, jsonify, request
import numpy as np
from numpy.random import uniform
import random

app = Flask(__name__)


RANDOM_DATASET_SIZE = 1000000
RANDOM_DATASET_DIMENSIONS = 4
RANDOM_SAMPLE = uniform(0, 1, RANDOM_DATASET_SIZE * RANDOM_DATASET_DIMENSIONS)
RANDOM_DATASET = RANDOM_SAMPLE.reshape((RANDOM_DATASET_SIZE, RANDOM_DATASET_DIMENSIONS))

indexes = np.arange(0, RANDOM_DATASET_SIZE)

# vectors indicating, which elements of the random dataset have already been sampled
sampling_a = np.zeros(RANDOM_DATASET_SIZE)
sampling_b = np.zeros(RANDOM_DATASET_SIZE)


@app.route('/')
def hello_world():
  return 'Ok. Flask server successfully launched.'


def produce_response_for_sample(sample_as_list):
  payload = {
    "timestamp": str(datetime.now()),
    "sample": sample_as_list
  }

  response = jsonify(payload)
  response.headers.add("Access-Control-Allow-Origin", "*")

  return response


@app.route('/reset', methods=["GET"])
def reset_samplings():
  global sampling_a, sampling_b
  sampling_a = np.zeros(RANDOM_DATASET_SIZE)
  sampling_b = np.zeros(RANDOM_DATASET_SIZE)
  return "ok"


@app.route('/sample', methods=["GET"])
def sample():
  data = RANDOM_DATASET
  indeces = np.array(range(0, len(data)))

  sample_size = int(request.args.get("size"))
  sampling = sampling_a if request.args.get("sample") == "a" else sampling_b

  remaining = data[sampling == 0]
  remaining_indeces = indeces[sampling == 0]

  if remaining.size == 0:
    return produce_response_for_sample([])

  already_sampled = sampling.sum()
  sample_size = int(min(sample_size, len(data)-already_sampled))

  sample_indeces = random.sample(remaining_indeces.tolist(), sample_size)
  sample = data[sample_indeces]
  sampling[sample_indeces] = 1

  response = produce_response_for_sample(sample.tolist())

  return response


if __name__ == "__main__":
  app.run(debug=True)