from flask import Flask, abort, jsonify, request
import numpy as np
from datetime import datetime
from pipeline import Pipeline

app = Flask(__name__)


# stores Pipeline objects, as specified by the client using pipeline configurations
PIPELINES = {}


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


@app.route('/update_pipeline/<id>', methods=["GET"])
def update_pipeline(id):
  old_pipeline = PIPELINES.get(id)
  config = get_pipeline_config(request)

  if old_pipeline == None:
    PIPELINES[str(id)] = Pipeline(config)
    return cors_response("ok")

  old_pipeline.update_selection(config["selection"])
  return cors_response("ok")


@app.route('/set_selection/<id>', methods=["GET"])
def set_selection(id):
  pipeline = PIPELINES.get(id)

  if pipeline == None:
    print("couldn't find pipeline with id", id)
    abort(400)

  selection = request.args.get("selection")
  pipeline.update_selection(selection)
  return cors_response("ok")


def normalize_chunk_positions(chunk):
  x = chunk[:, 1]
  y = chunk[:, 2]

  # TODO: hardcoded transformation from geo to screen coordinates
  min_x = -179.8806635
  min_y = -85.3475888
  max_x = 179.9872917
  max_y = 83.5714722

  normalized_x = (x - min_x) / (max_x - min_x)
  normalized_y = (y - min_y) / (max_y - min_y)

  chunk[:, 1] = normalized_x
  chunk[:, 2] = 1 - normalized_y

  return chunk

@app.route('/sample/<id>', methods=["GET"])
def sample(id):
  pipeline = PIPELINES.get(id)

  if pipeline == None:
      print("couldn't find pipeline with id", id)
      abort(400)

  next_chunk = pipeline.get_next_chunk()
  normalized_chunk = normalize_chunk_positions(next_chunk)
  return produce_response_for_sample(normalized_chunk.tolist())


@app.route('/reset', methods=["GET"])
def reset_pipelines():
  global PIPELINES
  PIPELINES = {}
  return cors_response("ok")


if __name__ == "__main__":
  app.run(debug=True)