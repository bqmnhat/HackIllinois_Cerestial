from flask import Flask, request, jsonify,render_template
from model import Model
from data_scraper import updateWeatherContext
import files_utils as files_utils
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from weather_today import get_current_weather, get_24h_weather
from crawler import updateScrapeData
import os
import pandas as pa
import conversation_repo
import google.generativeai as genai
import asyncio


load_dotenv()

app = Flask(__name__)
model = None
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client = genai.GenerativeModel('gemini-1.5-flash')

def checkForScrape(query):
    global client
    response = client.generate_content("Answer 'yes' if you need to search the web for additional information to answer the user's question correctly and sufficiently. Answer 'no' if the question pertains to casual conversation. " + query)
    print(response.text)
    yes_answers = ["Yes", "yes", "Yes.", "yes.", "YES", "YES."]
    print((yes_answers.count(response.text.strip()) > 0))
    if (yes_answers.count(response.text.strip()) > 0):
        return True
    return False

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

    chatBot.create_conversation_chain()

def read_file_to_text(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

def init():
    global db
    db = conversation_repo.DB()
    prepareContext()
    startScheduler() 

@app.route("/")
def home():
    return render_template("chatbot.html")

@app.route("/internal/get_count", methods=['GET'])
def get_count():
    return jsonify({'count': db.getCount()})

@app.route("/internal/load_chat", methods=["GET"])
def load_chat():
    try:
        n = request.args.get('n', type=int, default=10)
        page = request.args.get('page', type=int, default=0)
        max_id = request.args.get('max_id', type=int, default=db.getCount())

        if n <= 0:
            return jsonify({"error": "Invalid value for 'n', must be a positive integer."}), 400
        
        if page < 0:
            return jsonify({"error": "Invalid value for 'page', must be a non negative integer."}), 400
        
        if max_id < 0:
            return jsonify({"error": "Invalid value for 'max_id', must be a non negative integer."}), 400

        return jsonify({"messages": db.findLastMessages(n, page, max_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/internal/query", methods=["POST"])
def query():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        question = data.get('question')
        db.insertMessage(False, question)
        answer = ""
        if (checkForScrape(question)):
            print("openai")
            updateContext(question)
            answer = chatBot.ask(question)
            # answer = client.generate_content(read_file_to_text(os.getenv('CONTEXT_PATH')) + question).text
        else:
            print("gemini")    
            hist = asyncio.run(chatBot.get_messages_as_str())    
            answer = client.generate_content(hist + read_file_to_text(os.getenv('GIVEN_CONTEXT_PATH')) + question).text
        db.insertMessage(True, answer)
        return jsonify({
            'question': question,
            'answer': answer
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/internal/weather", methods=["POST"])
def weather():
    current_weather = get_current_weather()
    day_weather = get_24h_weather()
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        category = data.get('category')
        #print(category)
        #print(today_wea_df[category] , "and ", type(today_wea_df[category]))
        day_weather[category] = day_weather[category].astype(str)
        
        #stats = today_wea_df[category].tolist()
        print(day_weather[category])
        current = round(current_weather[category])
        dw_list = day_weather[category].values.tolist()

        # stats = {'current_weather': current, 'day': day}
        # print(stats)
        json_response = jsonify({'current_weather': current, 'day': dw_list})
        # return jsonify(stats)
        return json_response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

init()

if __name__ == "__main__":
    app.run(debug=True)  
