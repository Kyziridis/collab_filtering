import gzip
import json
from time import time
import requests


start = time()
i = 0
PAUSE_ITER = 10_000
FILE_PATH = "data/sample.gz"
with gzip.open(FILE_PATH, "r") as events_file:
    time_ = time()
    for event in events_file:
        i += 1
        body = json.loads(event)
        response = requests.post(
            'http://127.0.0.1:8000/inputStream/', json=body)

        if i % PAUSE_ITER == 0:
            print(f"Endpoint hits: {i} / 12,987,825")
            print(response.json())
            print(
                f"Time taken for {PAUSE_ITER} number of hits {round(time()-time_, 3)} secs.")
            time_ = time()

    print(f"Time needed: {round(time() - start, 2)} secs")
