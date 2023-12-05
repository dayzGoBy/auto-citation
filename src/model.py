from qdrant_client import QdrantClient
from deepface import DeepFace
import requests
import os
from time import sleep

FEATURE_ORDER = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
FEATURE_SET = set(FEATURE_ORDER)

remote = QdrantClient(
    url="https://d4fbb97b-85ae-47ba-af87-d9a97711caff.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key=os.environ['QDRANT_API_TOKEN'],
)


def process_output(outputs):
    _translate = {
        'neutral': 'neutral',
        'joy': 'happy',
        'sadness': 'sad',
        'surprise': 'surprise',
        'fear': 'fear',
        'anger': 'angry',
        'disgust': 'disgust'
    }
    _map = {}
    for entry in outputs:
        if entry['label'] in _translate:
            label = _translate[entry['label']]
            _map[label] = entry['score']

    return [_map[key] for key in FEATURE_ORDER]


def classify_text(inputs: str):
    def _query(_payload):
        _headers = {"Authorization": f"Bearer {os.environ['HF_API_TOKEN']}"}
        _API_URL = "https://api-inference.huggingface.co/models/seara/rubert-base-cased-ru-go-emotions"
        _response = requests.post(_API_URL, headers=_headers, json=_payload)
        return _response.json()

    payload = {'inputs': inputs}
    response = _query(payload)

    if 'error' in response:
        sleep(2)
        response = _query(payload)

    return process_output(response[0])


def classify_face(path):
    outputs = DeepFace.analyze(img_path=path, actions=('emotion',))[0]['emotion']
    return [outputs[key] / 100 for key in FEATURE_ORDER]


def do_query(vector):
    query = remote.search(
        collection_name="quotes",
        query_vector=vector,
        limit=3,
    )
    return [q.payload for q in query]


def add_quote_to_db(quote: str, author: str, piece: str):
    # vec = classify_text(quote)
    pass
