from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
application=Flask(__name__)
app=application
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        print("Received POST request with form data:", request.form)
        try:
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )
            print("CustomData object created:", data.__dict__)

            pred_df = data.get_data_as_data_frame()
            print("DataFrame constructed:\n", pred_df)

            predict_pipeline = PredictPipeline()
            print("PredictPipeline created, calling predict()...")

            results = predict_pipeline.predict(pred_df)
            print("Prediction complete, results:", results)

            return render_template('index.html', result=results[0])

        except Exception as e:
            print("Error during prediction route:", e)
            return "An error occurred: " + str(e), 500

    

if __name__=="__main__":
    app.run(host="0.0.0.0")  