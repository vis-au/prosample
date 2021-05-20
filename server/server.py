from flask import Flask, abort, jsonify, request
from datetime import datetime
from pipeline import Pipeline

app = Flask(__name__)


# stores Pipeline objects, as specified by the client using pipeline configurations
PIPELINES = {}


@app.route('/')
def hello_world():
  return 'Ok. Flask server successfully launched.'


def create_response(payload):
  response = jsonify(payload)
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response


def produce_response_for_sample(sample_as_list):
  payload = {
    "timestamp": str(datetime.now()),
    "sample": sample_as_list
  }

  return create_response(payload)


@app.route('/create_pipeline/<id>', methods=["PUT"])
def create_pipeline(id):
  configuration = request.args.get("configuration")
  pipeline = Pipeline(configuration)

  PIPELINES[str(id)] = pipeline
  return "ok"


@app.route('/update_pipeline/<id>', methods=["PUT"])
def update_pipeline(id):
  old_pipeline = PIPELINES.get(id)

  if old_pipeline == None:
      create_pipeline(id)

  configuration = request.args.get("configuration")
  pipeline = Pipeline(configuration)

  PIPELINES[id] = pipeline
  return "ok"


@app.route('/set_selection/<id>', methods=["PUT"])
def set_selection(id):
  pipeline = PIPELINES.get(id)

  if pipeline == None:
    print("couldn't find pipeline with id", id)
    abort(400)

  selection = request.args.get("selection")
  pipeline.update_selection(selection)
  return "ok"


@app.route('/sample/<id>', methods=["GET"])
def sample(id):
  pipeline = PIPELINES.get(id)

  if pipeline == None:
      print("couldn't find pipeline with id", id)
      abort(400)

  next_chunk = pipeline.get_next_chunk()
  return produce_response_for_sample(next_chunk.tolist())


@app.route('/reset', methods=["GET"])
def reset_pipelines():
  global PIPELINES
  PIPELINES = {}
  return "ok"


if __name__ == "__main__":
  app.run(debug=True)