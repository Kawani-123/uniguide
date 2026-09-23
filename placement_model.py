import pandas as pd
from sklearn.linear_model import LogisticRegression


model = None


# ==============================
# TRAIN MODEL
# ==============================
def train_model():
    global model

    df = pd.read_csv("datasets/placement_dataset.csv")

    X = df[["CGPA", "Internships", "Projects"]]
    y = df["Placed"]

    model = LogisticRegression()
    model.fit(X, y)

    return model


# ==============================
# PREDICT PLACEMENT
# ==============================
def predict_placement(cgpa, internships, projects):
    global model

    if model is None:
        train_model()

    prediction = model.predict([[cgpa, internships, projects]])

    return "Likely to be Placed" if prediction[0] == 1 else "Needs Improvement"