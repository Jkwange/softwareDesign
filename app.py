from flask import Flask, request, jsonify
from flask_cors import CORS
import matplotlib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import io
import base64
import logging



matplotlib.use('Agg')
app = Flask(__name__)
CORS(app)


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('voice_phishing')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, message):
        self.logger.info(message)


class ErrorHandler:
    def handle(self, error):
        return {"error": str(error)}, 500


class ConfigurationLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.filepath, 'r') as file:
                config = file.read()
            return config
        except FileNotFoundError:
            return "model_parameters: default\nlog_level: info"


class FeatureExtractor:
    def extract_features(self, data):
        return np.random.rand(len(data), 5)

class Preprocessor:
    def preprocess(self, data):
        return np.array(data)

class VoicePhishingModel:
    def __init__(self):
        self.model = RandomForestClassifier()
    
    def train(self, X, y):
        self.model.fit(X, y)
    
    def predict(self, X):
        return self.model.predict(X)

class DataHandler:
    def load_data(self, filepath):
        with open(filepath, 'r') as file:
            data = file.readlines()
        return data
    
    def save_data(self, data, filepath):
        with open(filepath, 'w') as file:
            file.writelines(data)

class TXTParser:
    def parse(self, txt_string):
        return txt_string.split('\n')

class Classifier:
    def __init__(self):
        self.model = VoicePhishingModel()
        self.feature_extractor = FeatureExtractor()
        self.preprocessor = Preprocessor()
    
    def classify(self, data):
        processed_data = self.preprocessor.preprocess(data)
        features = self.feature_extractor.extract_features(processed_data)
        return self.model.predict(features)

class ChartGenerator:
    def generate_chart(self, data):
        fig, ax = plt.subplots()
        ax.bar(data.keys(), data.values())
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode('utf-8')


data_handler = DataHandler()
classifier = Classifier()
chart_generator = ChartGenerator()
logger = Logger()
error_handler = ErrorHandler()
config_loader = ConfigurationLoader('config.txt')


example_data = np.random.rand(100, 5)
example_labels = np.random.randint(0, 2, 100)
classifier.model.train(example_data, example_labels)

@app.route('/classify', methods=['POST'])
def classify():
    try:
        txt_data = request.json['data']
        lines = TXTParser().parse(txt_data)
        
        predictions = classifier.classify(lines)
        result = {"phishing": int(sum(predictions)), "non_phishing": int(len(predictions) - sum(predictions))}
        
        chart = chart_generator.generate_chart(result)
        
        logger.log("Classification completed successfully.")
        return jsonify({"result": result, "chart": chart})
    except Exception as e:
        logger.log("An error occurred during classification.")
        return error_handler.handle(e)

if __name__ == '__main__':
    app.run(port=5000)
