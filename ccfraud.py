import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

import time
import datetime

# returns data cols, data, target col, targets
def load_ccfraud():
    ds = pd.read_csv("dataset/fraudTrain.csv")
    print("File \"fraudTrain.csv\" loaded...")

    data_cols = [x for x in ds if x != "is_fraud"]
    target_col = "is_fraud"

    return ds, data_cols, [ds[col] for col in data_cols], target_col, ds[target_col]

dataframe, data_cols, data, target_col, target = load_ccfraud()

for x in data_cols:
    print(x, "\t\t", dataframe[x].dtype)

labelEncoderTransformTypes = {}

# constants
const_transac_date_format = "%Y-%m-%d %H:%M:%S"
# const_dob_format = "%Y-%m-%d"
def getTransactionDateUnix(string):
    return time.mktime(datetime.datetime.strptime(string, const_transac_date_format).timetuple())

def getDobFormat(string):
    return int(string.replace("-", ""))





def labelEncode(feature: str, dataframe, map):
    le = LabelEncoder()
    le.fit(dataframe[feature])
    dataframe[feature] = le.transform(dataframe[feature])
    map[feature] = le


labelEncode("merchant", dataframe, labelEncoderTransformTypes)
labelEncode("category", dataframe, labelEncoderTransformTypes)
labelEncode("first", dataframe, labelEncoderTransformTypes)
labelEncode("last", dataframe, labelEncoderTransformTypes)
labelEncode("gender", dataframe, labelEncoderTransformTypes)
labelEncode("street", dataframe, labelEncoderTransformTypes)
labelEncode("city", dataframe, labelEncoderTransformTypes)
labelEncode("state", dataframe, labelEncoderTransformTypes)
labelEncode("trans_num", dataframe, labelEncoderTransformTypes)
labelEncode("job", dataframe, labelEncoderTransformTypes)

dataframe["trans_date_trans_time"] = [getTransactionDateUnix(x) for x in dataframe["trans_date_trans_time"]]
dataframe["dob"] = [getDobFormat(x) for x in dataframe["dob"]]

for x in data_cols:
    print(x, "\t\t", dataframe[x].dtype)










print("Finished datatype conversions...")

clf = DecisionTreeClassifier()
clf.fit([dataframe[col] for col in data_cols], target)

