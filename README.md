# Web-Scraping-API

# Household Resource REST API

## Introduction

The inputs required to generate a Picwell health insurance recommendation
include household information and information about the plans for which the
household is eligible. We would like to store the households, rather than accept
the information for each recommendation, so that we can track how many
people are using our service, and also to see how a household's needs and
choices change over the years.

## Problem Definition

Please design and implement a set of http endpoints that allows an API consumer
to create a household and read it back later.

A household has an income and household members. Household members have age and
sex information.

Based on a household's income and size, a percentage of the [Federal Poverty Level
(FPL)](https://aspe.hhs.gov/poverty-guidelines) can be calculated. The
percentage is simply `Household.income` divided by the applicable FPL for that
household size. One can use the levels associated with residence in the
contiguous states for this exercise.

### Objectives

We recommend that you tackle these one at a time. 1 or 2 completed objectives is
better than 3 partially-finished ones 😊.

- Allow API users to create a new household resource.
- Allow API users to retrieve a household by ID.
- Return an HTTP 400 Bad Request response if API users try to create a household
  with an invalid format.
- Allow API users to retrieve a household's "percentage of Federal Poverty
  Level" for a given household ID.

For each of the objectives listed above, please provide tests to
demonstrate correctness of your implementation. We have provided an example test
in `test_household_api.py`, which can be run using the `pytest` shell command
that is available when using a python environment with the pytest package
installed. For the purposes of this work sample, it is fine if your tests
require Redis to be running.

## Getting Started

We have provided a skeleton Flask application to help you get
started. [Flask](http://flask.pocoo.org/) is a Python-based web microframework
that has very little scaffolding. Hopefully the skeleton app will make it easy
to pick up, even if you've never used Flask (or Python) before.

### Running the Application

The application is set up to run in a docker container, so that you can run it
without needing to install a bunch of dependencies into your local
environment. It also makes it much easier for us to reproduce your results.

If you haven't already, install [Docker for Mac](https://docs.docker.com/docker-for-mac/) or
[Docker for Windows](https://docs.docker.com/docker-for-windows/).

Open the docker application to start the docker daemon. Verify that it is active
by running `docker help` from the command line.

Finally, `cd` into your project root (the directory that holds this README) and
run `./up.sh` to start the application. It may be slow to start the first time
because it has to download the base image, but it will be faster on subsequent
startups. At the top, it will print something like `Dev server will be accessible on http://0.0.0.0:8080/`, with the url in green. Use this url to
make requests to the application. To make a request against the test route, try:

```
curl localhost:8080/sample-household/
```

To kill the server, just hit `ctrl-C`. `./up.sh` will start the server again.

### Flask Stuff

The application is organized into a single file, for simplicity in getting
started. Please feel free to reorganize it however you wish.

The Flask `request` object is a thread-global object that contains all the
information for the current request. Access query string arguments with
`request.args`. Retrieve the JSON payload as Python native from `request.json`.

### Domain Models

We have provided `Household` and `User` domain models using the
[pydantic](https://pydantic-docs.helpmanual.io/) library. You should
be able to use these without much modification for building your REST API.

### Redis

We have also set you up to use Redis, a straightforward key-value store, for
storing your household data. The Redis server and Redis python client are
installed for you in your docker container, and we've written a small helper for
accessing redis.

You should be able to achieve your storage needs using the most basic Redis
commands, though of course you may get as fancy as you wish. Hint: one way to do
this is to store the household object as a JSON string.

```
In [1]: from household_api import get_redis_connection

In [2]: r = get_redis_connection()

In [3]: r.set('key', '{"household": "object"}')
Out[3]: True

In [4]: r.get('key')
Out[4]: '{"household": "object"}'
```

The documentation for Redis commands can be found
[here](http://redis.io/commands). We are using the python Redis client, so all
commands are methods against the Redis connection object, which you can
retrieve using the provided `get_redis_connection` helper function. For example,
the `.set('key', 'value')` method demonstrated above is documented as the `SET`
command in the Redis docs.

## Helpful Resources

We do not expect you to use all or even any of the tools below: feel free
to solve the problem in your own way and use whatever tools you prefer. These
resources are here to help you find Python-specific tools that you might need,
so that you can show off your software development skills even if you aren't
super familiar with the Python ecosystem.

- It might be useful to know how Python
  [exception-handling](https://docs.python.org/3.7/tutorial/errors.html#handling-exceptions)
  works.

- Python has a built-in [json
  library](https://docs.python.org/3.7/library/json.html) that can encode dicts
  and lists as JSON strings and decode JSON strings back to dicts or lists. The
  usage is simple:

```
In [1]: import json

In [2]: json.dumps({'key': 'value'})
Out[2]: '{"key": "value"}'

In [3]: json.loads('{"key": "value"}')
Out[3]: {u'key': u'value'}
```

It also raises exceptions when supplied invalid JSON strings:

```
In [4]: json.loads('("this","isnt","json")')
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-3-4613fa983c7b> in <module>()
----> 1 json.loads('("this","isnt","json")')
```

- For generating unique ids for newly-generated resources, check out the
  [built-in Python uuid library](https://docs.python.org/3.7/library/uuid.html).

- If you do not have a preferred Python testing framework, we recommend
  [pytest](https://pytest.org/en/stable/getting-started.html). The built-in
  Python `unittest` library is another option. See the Flask [test
  client](http://flask.pocoo.org/docs/0.10/testing/#testing) for writing tests
  against your API routes as well as our supplied example for getting started.

- If you need additional dependencies, add them to the `requirements.txt` file
  and rerun `up.sh`.
