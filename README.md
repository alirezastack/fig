# Fig - Frontier API Gateway

Frontier API Gateway for the whole micro-service infrastructure. It uses gRPC client in order to be able to call different services.

## Service Structure
 - fig
   - core
     - client
     - login
     - question
     - survey
   - __init__
   - fig_app
   - requirements.txt
   - run
   - schemas
   - uwsgi_app
   - uwsgi_fig.ini
 - tests


`core` folder is where all the classes that handle REST API HTTP Methods reside.

The `__init__` file in fig folder is the most important place that handles rate limiting, log initiation and error handling. Here you can see that config file is read from `/etc/fig/fig.json`. 

`fig_app` file house all the exposed endpoints to the outside world. If you have to expose a new collection or a new resource put it here in `fig_app`.

schemas is the file that contains all the schemas used to validate given json payloads. `jsonschema` library is used to handle this validation.

## Installation

```
$ pip install -r requirements.txt

$ pip install setup.py
```

## Error Management
Every error that needs to be specific has a mapping in configuration file. If for example a service returns save_error error, that error has the below structure in fig config file:

```
{
    "save_error": {
        "code": "save_error",
        "reason": "Document could not be saved",
        "status_code": 400
    }
}
```

NOTE: `status_code` is a status code that clients will receive as the HTTP status code of their response.

Sample error response returned by `Fig`:

```
{
    "result": {},
    "pagination": {},
    "error": {
        "code": "invalid_schema",
        "details": [
            {}
        ],
        "reason": "{} does not have enough properties"
    }
}
```
