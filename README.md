# tiktok-deepfake
## Install Dependencies
Install Python3/pip and Node/npm.

Install [pipenv](https://pipenv.pypa.io/en/latest/) Python package manager:

```pip install --user pipenv```

Enter the backend directory:

```cd api```

Install the python dependencies:

```pipenv install```

Install the node dependencies:

```
cd ../app
npm install
```

## Run
```
cd api
pipenv run flask run -h 0.0.0.0
cd ../app
npm start
```

## Test
Make a test request:

```curl --header "Content-Type: application/json"   --request POST   --data '{"rawText": "hello world!"}'   http://localhost:5000/api/rawtext```

## Auto-format the code

```pipenv run black app.py```