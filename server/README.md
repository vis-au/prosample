# ProSample Server and Pipeline Components
This directory contains the Python-based implementation of our pipeline for tailorable PVA-sampling.


## Installation
To install the Python dependencies, you have to have a local version of [Python 3.9](https://www.python.org/downloads/) with the package manager [pip](https://pypi.org/project/pip/) (version 21.1.1 or higher) installed.
Run the following command inside this directory to download and install the required dependencies (see [requirements.txt](./requirements.txt) for more details).
```sh
pip install -r requirements.txt
```

## Pipeline components
The implementation of the components of the pipeline can be found inside [./pipeline](./pipeline/). Please note that this implementation is still very much experimental and not intended as a standalone library, yet.

## Server
For legacy reasons, this directory also contains the code for the HTTP server that interfaces with the web-based frontend in the `client/` directory.
This server provides interactive access to the pipeline for testing purposes.

The server uses a simple [flask](https://flask.palletsprojects.com/en/2.0.x/) server to define the API, through which any number of sampling pipelines can be configured and accessed.

### Getting Started
After installing the dependencies as described above, you may launch the server from your terminal by running the following command inside this directory:
```sh
python server.py
```

This will launch the webserver on port ```:5000``` on ```localhost```.
After a while, you should see the following output in your terminal, indicating that everything went well:
```
* Serving Flask app 'server' (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

You can test the connection by accessing the following URL from your browser [http://localhost:5000](http://localhost:5000).
You should see a message saying ```Ok. Flask server successfully launched.```.

### API (incomplete!)
#### /
Test if the connection works. Responds with a string saying ```Ok. Flask server successfully launched.``` if the installation was successful.

#### / sample[size:int]
Request a sample of random floating point numbers, grouped into sublists of size > 2.
The required parameter size indicates the number of samples to draw from a random distribution.
Returns a JSON object of the following format:
```json
{
  "timestamp": string,
  "sample": number[][]
}
```
