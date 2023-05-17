# Incremental Collaborative Filtering

<br>

## FastAPI Endpoint for Incoming Streams


This project was developed in a `Lenovo T430` machine with `8GB` ram and an `Intel(R) Core(TM) i5-3320M CPU @ 2.60GHz` cpu.

The software is an API endpoint which receives streams from users.

When a user watches a `mediaId` until the end (`streamend`), the `mediaId` is considered consumed.

After the user consumes an item, the software updates itself and runs item-to-item collaborative filtering for the specific target `mediaId` which was just consumed.

The similarity is based on a hardcoded thresshold.

After the full data run in `run_backend.py` script, plots and results will be exported under `exports/` directory.

Please remember to move the dataset `sample.gz` under `data` folder before you start.

You can run the project either via poetry or pip.

------


### Dependencies:
 - `Python >=3.9`

### Poetry installation
You need to have poetry locally installed on your machine with `Python` `3.9` or greater.

Then you can just do:
```
cd collab_filtering
poetry shell
poetry install
```

<br>

### Pip installation
You need to have pip installed in your machine. 

You can always create a `venv` and install there dependencies.
```
cd collab_filtering
pip install -r requirements.txt
```

------

### FastAPI run
If you want to test the FastAPI endpoint run the following:
Open Terminal and run the fastAPI endpoint:
```
uvicorn collab_filtering.api:app
```
OR
```
python -m uvicorn collab_filtering.api:app
```

If the uvicorn is running on an instance, open another terminal, activate again the your venv and run:
```
python main.py
```

<br>

### Run Backend (without API call)
If you want to test the backend without hitting the endpoint run:
```
python run_backend.py
```

### Unit Testing
```
pytest
```
or
```
python -m pytest
```
or
```
poetry run pytest
```

### Execution time
- `1402` sec (backend)
