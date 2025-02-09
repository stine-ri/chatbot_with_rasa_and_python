from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chatbot responses
@app.route('/get-response', methods=['POST'])
def get_response():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"reply": "Sorry, I didn't get that. Please try again."})
    
    # Rasa REST API endpoint
    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'

    try:
        # Send the user message to Rasa server
        response = requests.post(
            rasa_url,
            json={"sender": "user", "message": user_message}
        )
        
        if response.status_code == 200 and response.json():
            bot_reply = response.json()[0].get('text', "I'm not sure how to respond.")
        else:
            bot_reply = "No response from Rasa server."
    
    except requests.exceptions.RequestException as e:
        bot_reply = f"Error connecting to Rasa server: {str(e)}"
    
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
