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


def get_subdivision_params(req):
  params = {}
  params_in_req = req.args.get("params").split(" ")  # clients sends "+", but server reads " "??
  for param in params_in_req:
    if param == "-1":  # -1 indicates "no parameters"
      continue
    elif param == "subspace":
      params[param] = [int(x) for x in req.args.get(param).split(":")]
    elif param == "k" or param == "min_samples":
      params[param] = int(req.args.get(param))
    elif param == "eps":
      params[param] = float(req.args.get(param))
    else:
      params[param] = req.args.get(param)
  return params

def get_pipeline_config(req):
  # request contains list of supplied subdivision parameters

  params = get_subdivision_params(req)

  configuration = {
    "linearization": req.args.get("linearization"),
    "subdivision": req.args.get("subdivision"),
    "selection": req.args.get("selection"),
    "data": req.args.get("data"),
    "dimension": req.args.get("dimension"),
    "params": params,
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
  config["params"] = get_subdivision_params(request)

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

  dimension = request.args.get("dimension")
  pipeline.update_dimension(dimension)
  return cors_response("ok")


@app.route('/steer', methods=["GET"])
def steer():
  # get pipelines, set their selection's steering parameters
  dimension = request.args.get("dimension")
  min_value = request.args.get("min")
  max_value = request.args.get("max")
  for pipeline in PIPELINES:
    PIPELINES[pipeline].selection.steer(dimension, min_value, max_value)

  return cors_response("ok")


@app.route('/steer/cancel', methods=["GET"])
def cancel_steering():
  # get pipelines, clear their selection's steering parameters
  for pipeline in PIPELINES:
    PIPELINES[pipeline].selection.clear_steering()
  return cors_response("ok")


@app.route('/sample/<id>', methods=["GET"])
def sample(id):
  pipeline = PIPELINES.get(id)

  if pipeline is None:
      print("couldn't find pipeline with id", id)
      abort(400)

  next_chunk = pipeline.get_next_chunk()
  return produce_response_for_sample(next_chunk.tolist())


@app.route("/all_data/<id>", methods=["GET"])
def get_all_data(id):
  pipeline = PIPELINES.get(id)

  if pipeline is None:
    print("couldn't find pipeilne with id", id)
    abort(400)

  dataset_name = pipeline.sampler.data_set_name
  all_data = pipeline.linearization.read_linearization(dataset_name)
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
