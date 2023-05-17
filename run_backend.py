import gzip
import json
from time import time

from collab_filtering.api_objects import RequestInputData
from collab_filtering.backend import DataManager


dm = DataManager()

errors = 0
i = 0
time_ = time()
start = time()
PAUSE_ITER = 500_000
FILE_PATH = "data/sample.gz"

with gzip.open(FILE_PATH, "r") as events_file:
    # Time for 12,987,825 streams: 1366.657 secs
    for event in events_file:
        i += 1
        body = json.loads(event)

        try:
            stream = RequestInputData(**body)
        except Exception as e:
            errors += 1
            continue

        response = dm.run(stream)
        if i % PAUSE_ITER == 0:
            print(f"Endpoint hits: {dm.n_api_hits} / 12,987,825")
            print(json.dumps(response))
            print(f"Time taken for {PAUSE_ITER} iters {time()-time_} secs\n")
            time_ = time()

    # End of loop
    top_u, top_i = dm.report_statistics(plot=True)
    print(json.dumps(response))
    print(f"Top 5 Users: {list(top_u.keys())}")
    print(f"Top 5 Items: {list(top_i.keys())}")

    with open("exports/similarities.txt", "a") as sim_file:
        for it in dm.sims:
            if dm.sims[it]:
                sim_file.writelines(f"Item: {it} -> {dm.sims[it]}\n")

    print("Plots and results exported under exports/ dir >_")
    print(f"Time for {i} streams: {round(time()-start, 3)} secs")
