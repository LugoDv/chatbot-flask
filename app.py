from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz
from flask_cors import CORS
import json ,os

app = Flask(__name__)
CORS(app)

# Carga el archivo JSON una vez al iniciar
with open("preguntas.json", "r", encoding="utf-8") as f:
    base = json.load(f)

@app.route("/chatbot", methods=["POST"])
def chatbot():
    datos = request.get_json()
    pregunta_usuario = datos.get("message", "").lower()

    mejor_puntaje = 0
    mejor_respuesta = ""
    sugerencias = []

    for item in base:
        pregunta_guardada = item["pregunta"].lower()
        puntaje = fuzz.token_set_ratio(pregunta_usuario, pregunta_guardada)

        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_respuesta = item["respuesta"]
            sugerencias = item.get("sugerencias", [])

    if mejor_puntaje < 60:
        mejor_respuesta = "🤔 No tengo una respuesta clara para eso. Pero puedes preguntarme sobre visado, entrevistas, requisitos, pagos... O escribirnos por WhatsApp 👉 https://wa.me/34TU_NUMERO"
        sugerencias = [
            "¿Cómo es la entrevista?",
            "¿Qué documentos necesito?",
            "¿Cuánto cuesta el programa?"
        ]

    return jsonify({
        "respuesta": mejor_respuesta,
        "sugerencias": sugerencias
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
