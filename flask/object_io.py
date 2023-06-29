import pickle as pkl

model_path = "./objects/tree.pkl"
label_encoders_path = "./objects/label_encoders.pkl"
classifier = None
label_encoders = None

def load():
    global classifier
    global label_encoders

    with open(model_path, "rb") as f:
        classifier = pkl.load(f)
    
    with open (label_encoders_path, "rb") as f:
        label_encoders = pkl.load(f)

def getClassifier():
    if classifier == None:
        load()
    
    return classifier

def getLabelEncoders():
    if label_encoders == None:
        load()
    
    return label_encoders