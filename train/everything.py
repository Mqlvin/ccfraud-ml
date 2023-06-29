from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from ..ccfraud import load_ccfraud

X, y = load_ccfraud()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)