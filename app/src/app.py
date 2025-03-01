from flask import Flask, request, jsonify,render_template
from model import Model
from data_scraper import updateWeatherContext
import files_utils as files_utils
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from weather_today import get_today_weather
from crawler import updateScrapeData
import os
import pandas as pa
# from google.generativeai import genai


load_dotenv()

app = Flask(__name__)
model = None
# client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# def checkForScrape(query):
#     global client
#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents="Answer all my question in one word only, 'yes' or 'no'. Should you search the web for this question: " + query,
#     )
#     print(response.text == "Yes.")

def startScheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(prepareContext, 'cron', hour=0, minute=0)  # 0:00 hours daily
    scheduler.start()
    
def prepareContext():
    global chatBot
    updateWeatherContext()
    updateScrapeData("Agriculture in Illinois")

    context_list = ["GIVEN_CONTEXT_PATH","WEATHER_CONTEXT_PATH","SCRAPE_CONTEXT_PATH"]
    contexts = [os.getenv(env) for env in context_list if os.getenv(env)]
    if len(contexts) == 0:
        raise ValueError("context file paths are not set")

    
    context_path = os.getenv("CONTEXT_PATH")
    if not context_path:
        raise ValueError("CONTEXT_PATH environment variable is not set")

    files_utils.removeFile(context_path)
    files_utils.concatFiles(context_path, contexts) 

    chatBot = Model()

def updateContext(query):
    updateScrapeData(query)

    context_list = ["GIVEN_CONTEXT_PATH","WEATHER_CONTEXT_PATH","SCRAPE_CONTEXT_PATH"]
    contexts = [os.getenv(env) for env in context_list if os.getenv(env)]
    if len(contexts) == 0:
        raise ValueError("context file paths are not set")

    
    context_path = os.getenv("CONTEXT_PATH")
    if not context_path:
        raise ValueError("CONTEXT_PATH environment variable is not set")

    files_utils.removeFile(context_path)
    files_utils.concatFiles(context_path, contexts) 

    chatBot = Model()

def init():
    prepareContext()
    startScheduler() 

@app.route("/")
def home():
    return render_template("chatbot.html")

@app.route("/internal/query", methods=["POST"])
def query():
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        question = data.get('question')
        # if (checkForScrape(question)):
        updateContext(question)
        answer = chatBot.ask(question)
        return jsonify({
            'question': question,
            'answer': answer
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/internal/weather", methods=["POST"])
def send_weather():
    today_wea_df = get_today_weather()
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        category = data.get('category')
        #print(category)
        #print(today_wea_df[category] , "and ", type(today_wea_df[category]))
        #today_wea_df[category] = today_wea_df[category].astype("string")
        
        #stats = today_wea_df[category].tolist()
    
        
        return "{}".format(round(today_wea_df[category]))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

init()

if __name__ == "__main__":
    app.run(debug=True)  
