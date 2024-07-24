from flask import Flask, request
from flask_cors import CORS, cross_origin
from src.pipeline.qa_pipeline import QAPipeline
from src.components.sentiment_analysis import SentimentAnalyzer
from src.pipeline.summarizer_pipeline import SummarizationPipeline
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@cross_origin
@app.route("/")
def test():
    return {"message": "Hello World!"}


@cross_origin
@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')  # Get list of files from the request
    if not files:
        return {"error": "No files provided"}, 400

    qa_pipeline = QAPipeline(files)
    qa_pipeline.start_processing_documents()
    return {"result": "Data Processed"}


@cross_origin
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data['question']

    #download files
    response = QAPipeline.start_qa(question)

    return {"answer": response}


@cross_origin
@app.route('/sentiment', methods=['POST'])
def sentiment():
    data = request.get_json()
    text = data['text']

    analyzer = SentimentAnalyzer()
    sentiment = analyzer.analyze_sentiment(text)

    return {"sentiment": sentiment}


@cross_origin
@app.route('/summarize', methods=['POST'])
def summarize():
    files = request.files.getlist('file')  # Get list of files from the request
    if not files:
        return {"error": "No files provided"}, 400

    summarizer_pipeline = SummarizationPipeline(files)
    summaries = summarizer_pipeline.start_summmarization()
    print(summaries)

    return {"summaries": summaries}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
