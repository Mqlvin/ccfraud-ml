from object_io import getClassifier, getLabelEncoders
import numpy as np
import pandas as pd
from random import randint

feature_headers_key = {"amt":0, "category":1, "dob":2, "gender":3}
headers = ["amt", "category", "dob", "gender"]


def is_fraud(amount: float, category: float, dob: float, gender: float):                      # remove warning
    """
    a = np.transpose((np.array(headers), np.array([ amount, category, gender, dob ], dtype = object))).T
    b = np.array([ amount, category, gender, dob ]).reshape(-1, 1)
    print(b)

    return getClassifier().predict(  b  )[0] == 1
    """

    return amount > randint(75, 79)



def get_valid_format(amount, category, dob, gender):
    return float(amount), int(encode_feature(category, "category")), int(dob.replace("-", "")), int(encode_feature(gender, "gender"))




def get_graph_points(start, end, category, gender, dob):
    amounts = [x for x in np.linspace(start, end, 30)]
    category_int = getLabelEncoders()["category"].transform([category])
    dob_int = dob.replace("-", "")
    gender_int = getLabelEncoders()["gender"].transform([gender])

    outcomes = {}
    
    for n in amounts:
        outcomes[round(n, 3)] = 1 if is_fraud(n, category_int, dob_int, gender_int) else 0

    return outcomes

def encode_feature(data, feature):
    return getLabelEncoders()[feature].transform([data])