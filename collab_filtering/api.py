from fastapi import FastAPI

from collab_filtering.api_objects import RequestInputData
from collab_filtering.backend import DataManager


app = FastAPI(title="Icremental Collaborating Filtering",
              description="Item-to-Item Incremental Collaborating Filtering on Streaming Data",
              docs_url='/')


data_manager = DataManager()


@app.post("/inputStream/")
async def input_stream(stream: RequestInputData):
    response = data_manager.run(stream)
    return {'response': response}
