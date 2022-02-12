from flask import Flask, abort, jsonify, request
import numpy as np
from datetime import datetime
from pipeline import Pipeline

app = Flask(__name__)


# stores Pipeline objects, as specified by the client using pipeline configurations
PIPELINES: dict[str, Pipeline] = {}


@app.route('/')
def hello_world():
  return 'Ok. Flask server successfully launched.'


def cors_response(payload):
  response = jsonify(payload)
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response


def produce_response_for_sample(sample_as_list):
  payload = {
    "timestamp": str(datetime.now()),
    "sample": sample_as_list
  }

  return cors_response(payload)


def get_pipeline_config(req):
  configuration = {
    "linearization": req.args.get("linearization"),
    "subdivision": req.args.get("subdivision"),
    "selection": req.args.get("selection"),
    "data": req.args.get("data"),
    "dimension": req.args.get("dimension")
  }

  return configuration


@app.route('/create_pipeline/<id>', methods=["GET"])
def create_pipeline(id):
  PIPELINES[str(id)] = Pipeline(get_pipeline_config(request))
  return cors_response("ok")


@app.route('/update_linearization/<id>', methods=["GET"])
def update_linearization(id):
  pipeline = PIPELINES.get(id)

  if pipeline is None:
    print("couldn't find pipeline with id", id)
    abort(400)

  linearization = request.args.get("linearization")
  config = pipeline.get_config()
  config["linearization"] = linearization
  PIPELINES[str(id)] = Pipeline(config)
  return cors_response("ok")


@app.route('/update_subdivision/<id>', methods=["GET"])
def update_subdivision(id):
  pipeline = PIPELINES.get(id)

  if pipeline is None:
    print("couldn't find pipeline with id", id)
    abort(400)

  subdivision = request.args.get("subdivision")
  config = pipeline.get_config()
  config["subdivision"] = subdivision
  PIPELINES[str(id)] = Pipeline(config)
  return cors_response("ok")


@app.route('/update_selection/<id>', methods=["GET"])
def update_selection(id):
  pipeline = PIPELINES.get(id)

  if pipeline is None:
    print("couldn't find pipeline with id", id)
    abort(400)

  selection = request.args.get("selection")
  pipeline.update_selection(selection)
  return cors_response("ok")


@app.route('/update_dimension/<id>', methods=["GET"])
def update_dimension(id):
  pipeline = PIPELINES.get(id)

  if pipeline is None:
    print("couldn't find pipeline with id", id)
    abort(400)

  selection = request.args.get("selection")
  pipeline.update_dimension(selection)
  return cors_response("ok")


def normalize_chunk_positions(chunk, dataset_name):
  x = chunk[:, 1]
  y = chunk[:, 2]

  # TODO: hardcoded transformation from geo to screen coordinates

  if dataset_name == "mountain_peaks":
    min_x = -179.8806635
    min_y = -85.3475888
    max_x = 179.9872917
    max_y = 83.5714722
  elif dataset_name == "spotify":
    min_x = 0
    min_y = 3344
    max_x = 100
    max_y = 5621218

  normalized_x = (x - min_x) / (max_x - min_x)
  normalized_y = (y - min_y) / (max_y - min_y)

  chunk[:, 1] = normalized_x
  chunk[:, 2] = 1 - normalized_y

  return chunk


@app.route('/sample/<id>', methods=["GET"])
def sample(id):
  pipeline = PIPELINES.get(id)

  if pipeline is None:
      print("couldn't find pipeline with id", id)
      abort(400)

  next_chunk = pipeline.get_next_chunk()
  dataset_name = pipeline.get_config()["data"]
  normalized_chunk = normalize_chunk_positions(next_chunk, dataset_name)
  return produce_response_for_sample(normalized_chunk.tolist())


@app.route("/all_data/<id>", methods=["GET"])
def get_all_data(id):
  pipeline = PIPELINES.get(id)

  if pipeline is None:
    print("couldn't find pipeilne with id", id)
    abort(400)

  dataset_name = pipeline.sampler.data_set_name
  all_data = pipeline.linearization.read_linearization(dataset_name)
  normalize_chunk_positions(all_data, dataset_name)
  return cors_response(all_data.tolist())


@app.route('/reset', methods=["GET"])
def reset_pipelines():
  global PIPELINES
  PIPELINES = {}
  return cors_response("ok")


@app.route('/data_size/<id>', methods=["GET"])
def data_size(id):
  pipeline = PIPELINES.get(id)

  if pipeline is None:
    print("couldn't find pipeline with id", id)
    abort(400)

  dataset_size = pipeline.get_dataset_size()
  return cors_response(dataset_size)


if __name__ == "__main__":
  app.run(debug=True)