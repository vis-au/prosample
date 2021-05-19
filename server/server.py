from datetime import datetime
from flask import Flask, jsonify, request
import numpy as np
from numpy.random import uniform
import random

app = Flask(__name__)


RANDOM_DATASET_SIZE = 1000000
RANDOM_DATASET_DIMENSIONS = 2
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


@app.route('/sample', methods=["GET"])
def sample():
  sample_size = int(request.args.get("size"))
  sampling = sampling_a if request.args.get("sample") == "a" else sampling_b
  sampled = sampling.sum()

  remaining_indeces = sampling == 0
  remaining = remaining_indeces.sum()

  if remaining == 0:
    return produce_response_for_sample([])

  sample_size = sample_size if sampled+sample_size < RANDOM_DATASET_SIZE else RANDOM_DATASET_SIZE-sampled
  sample_size = int(sample_size)

  sampled_indeces = random.sample(list(remaining_indeces), sample_size)
  sampled_data = [RANDOM_DATASET[i].tolist() for i in sampled_indeces]
  sampling[np.array(sampled_indeces)] = 1

  response = produce_response_for_sample(sampled_data)

  return response


if __name__ == "__main__":
  app.run()