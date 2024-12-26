from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import joblib

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model and preprocessing pipeline
model = joblib.load("model.pkl")  # Replace with the path to your saved model
preprocessor = joblib.load("preprocessor.pkl")  # Replace with your preprocessing pipeline if applicable

@app.route("/")
def home():
    """
    Renders the home page with an input form for user data.
    """
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles prediction based on user inputs from the form.
    """
    try:
        # Extract user inputs
        data = {
            "Pclass": int(request.form["Pclass"]),
            "Sex": request.form["Sex"],
            "Age": float(request.form["Age"]),
            "SibSp": int(request.form["SibSp"]),
            "Parch": int(request.form["Parch"]),
            "Fare": float(request.form["Fare"]),
            "Embarked": request.form["Embarked"]
        }

        # Convert to DataFrame
        input_data = pd.DataFrame([data])

        # Preprocess the input data
        if preprocessor:
            processed_data = preprocessor.transform(input_data)
        else:
            processed_data = input_data

        # Make prediction
        prediction = model.predict(processed_data)
        survival = "Survived" if prediction[0] == 1 else "Did Not Survive"

        return render_template("result.html", prediction=survival)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "_main_":
    app.run(debug=True)
