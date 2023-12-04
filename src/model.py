from qdrant_client import QdrantClient
from deepface import DeepFace
import os

FEATURE_ORDER = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
FEATURE_SET = set(FEATURE_ORDER)

remote = QdrantClient(
    url="https://d4fbb97b-85ae-47ba-af87-d9a97711caff.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key=os.environ['QDRANT_API_TOKEN'],
)


"""def process_output(outputs):
    translate = {
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
        if entry['label'] in translate:
            label = translate[entry['label']]
            _map[label] = entry['score']

    return [_map[key] for key in FEATURE_ORDER]
    

def classify_text(inputs):
    return process_output(pipe(inputs, top_k=None))"""

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
    