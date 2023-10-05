# EPOCA PREDICTION API

Epoca Prediction is an API designed to implement and serve the Prediction Model generated in the Epoch Builder.


[API Errors](./API_ERRORS.md)



## Requirements

- Docker: v20.10.12

- Docker Compose: v1.29.2




## Local Testing

- Python: v3.8.10

- Pip: v20.0.2



## Local Development

Even though the container runs on **python:3.10-slim-buster**, it is not easy to organize the dependencies for this specific version of Python 3 and therefore, the coding guidelines should follow the version **3.8**.


Install dependencies on the host machine with:

`sudo apt-get update`

`pip install --upgrade pip`

`sudo apt-get install -y libpq-dev gcc g++`

`pip install -r requirements.txt`




#
# Modules Import

The environment variable **PYTHONPATH** is provided by the compose project. However, it is not present during local development and therefore some imports may be marked as invalid. To fix this, make sure to add **./dist** to Python's extra paths in the code editor.



#
# Tests

*IMPORTANT: These unit tests are designed to be executed inside of the containerized infrastructure. For more information goto `compose/README.md#ContainerizedUnitTests`*

**End-to-end:** `python -m unittest discover -s tests -p '*_test.py'`
