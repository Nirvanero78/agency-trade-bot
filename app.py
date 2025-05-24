from flask import Flask, request
import json
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@app.route('/', methods=['GET', 'HEAD'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Token incorrecto", 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data["entry"]:
        for msg in entry["messaging"]:
            if msg.get("message"):
                sender_id = msg["sender"]["id"]
                text = msg["message"].get("text")
                if text:
                    send_message(sender_id, create_response(text))
    return "ok", 200

def create_response(text):
    text = text.lower()
    if "enfermería" in text:
        return "🎓 ¡Perfecto! El curso de auxiliar de enfermería incluye certificación SEP y beca del 50%. ¿Quieres que te mande los pasos para inscribirte?"
    elif "lesiones" in text:
        return "🧴 El diplomado en lesiones cutáneas inicia pronto. ¡Solo 1 clase al mes! ¿Te gustaría recibir más info por WhatsApp?"
    else:
        return "👋 Hola, soy el bot de Agency Trade. ¿Te gustaría conocer nuestros cursos o inscribirte?"

def send_message(recipient_id, message_text):
    params = {"access_token": ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post("https://graph.facebook.com/v17.0/me/messages", params=params, headers=headers, data=json.dumps(data))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
