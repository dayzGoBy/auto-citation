from sentence_transformers import SentenceTransformer, util
import os
import replicate
import random
import uuid
from qdrant_client import QdrantClient, models

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
replapi = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])
remote = QdrantClient(
    url="https://d4fbb97b-85ae-47ba-af87-d9a97711caff.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key=os.environ['QDRANT_API_TOKEN'],
)


def describe(path):
    return "".join(replapi.run(
        "yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
        input={
            "image": open(path, "rb"),
            "top_p": 1,
            "prompt": "Provide me a prose piece, matching this image. Do not use words human, person, man or woman",
            "max_tokens": 64,
            "temperature": 0.05
        }
    ))


def classify_face(path):
    return model.encode(describe(path))


def do_query(vector):
    query = remote.search(
        collection_name="quotes-new",
        query_vector=vector,
        limit=5,
    )

    return random.sample([q.payload for q in query], 3)


def add_quote(quote: str, author: str, piece: str):
    remote.upload_records(
        collection_name="quotes-new",
        records=[models.Record(
            id=uuid.uuid4().fields[-1],
            vector=model.encode(quote).tolist(),
            payload={'text': quote, 'author': author, 'piece': piece}
        )]
    )
