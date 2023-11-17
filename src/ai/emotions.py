from warnings import simplefilter

from deepface import DeepFace


simplefilter("ignore")

RESPONSE_PARAMS = ("age", "gender", "race", "emotion")


def get_person_description(img_path: str) -> tuple:
    return DeepFace.analyze(img_path=img_path)[0]


def structurize_for_gpt(demographies) -> str:
    return
    """
    Age: {}
    Gender: {}
    Race: {}
    Emotions: {}
    """.format(
        *map(lambda key: demographies[key], RESPONSE_PARAMS))
