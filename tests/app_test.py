import requests
import pytest
from fastapi.testclient import TestClient

from collab_filtering.api import app


test_client = TestClient(app)


def test_input_stream_event():
    body = {
        "EventId": "736a88a08e157cf1151f11bb76ef910d6160f33f75171e0c11b4ea8bc4a618fc",
        "UserId": 666,
        "MediaId": 12,
        "Timestamp": 729362,
        "DateTime": "1997-12-04T16:55:49",
        "EventType": "streamstart"
    }
    response = test_client.post("/inputStream/", json=body)
    assert response.status_code == 200


def test_bad_input_stream_event():
    body = {
        "EventId": "asdqwe123234asdscv",
        "UserId": 666,
        "MediaId": 12,
        "Timestamp": 40,
        "DateTime": "01/01/2001",
        "EventType": "streamstart"
    }
    response = test_client.post("/inputStream/", json=body)
    assert response.status_code == 422
