from flask import Flask, request, jsonify,render_template
from model import Model
from data_scraper import updateWeatherContext
import files_utils
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
model = None

def startScheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(prepareContext, 'cron', hour=0, minute=0)  # 0:00 hours daily
    scheduler.start()
    
def prepareContext():
    updateWeatherContext()
    contexts = os.getenv("CONTEXT_LIST").split(",")
    context_path = os.getenv("CONTEXT_PATH")
    files_utils.removeFile(context_path)
    files_utils.concatFiles(context_path, contexts)    

def init():
    global chatBot  
    chatBot = Model()
    prepareContext()
    startScheduler() 

@app.route("/")
def home():
    return render_template("chatbot.html")

@app.route("/internal/query", methods=["POST"])
def query():
    try:
        data = request.get_json()
        print("abcd")
        
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        question = data.get('question')
        answer = chatBot.ask(question)
        return jsonify({
            'question': question,
            'answer': answer
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


init()

if __name__ == "__main__":
    app.run(debug=True)  
