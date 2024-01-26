# Backend Test for Idoven

The following repository has been created in order to make a test.

## Information

* I have used poetry to manage dependencies, so we have the pyproject.toml file in the root.

* Only the required minimum endpoints have been created:
  * Create user
  * login
  * add ecg
  * get insights of the logged user

* I do not have much experience on FastAPI (I always use Django) but I decided to do the test on your tech and I liked it, but I spent more time.

* The following things that I did not do because I did not have enought time:
  * Implement the roles properly.
  * Unit tests with pytest.
  * Improve the configuration management.
  * Code style.
  * Add DockerFile and a docker-compose.yaml to deploy using other database different than sqlite.
  * Improve the E2E test.

## Setup

Setup virtual environment
```
python3 -m venv .idoven-test
source .idoven-test/bin/activate
pip install poetry
poetry install
```

To run the server in local
```
cd src
uvicorn main:app --reload
```

## Testing

Basically the test do the following:
* Start the server
* Use the API to create a new user
* Use the API to login.
* Use the API to create N ECGs
* Use the API to retrieve the Insights and check that the numbers are correct.
* Kill the server
  
From the root directory and with poetry installed execute:
```
./test.sh
```

## About the scalability

I would suggest to use the proper database depending on what we really need to store and show. Actually the data could be copied periodically from one db to another, so you could work on another db to get insights.
All the calculations might be done in the background and should not affect the API performance.
