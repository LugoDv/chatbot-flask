from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz
import json ,os

app = Flask(__name__)

# Carga el archivo JSON una vez al iniciar
with open("preguntas.json", "r", encoding="utf-8") as f:
    base = json.load(f)

@app.route("/chatbot", methods=["POST"])
def chatbot():
    datos = request.get_json()
    pregunta_usuario = datos.get("message", "").lower()

    mejor_puntaje = 0
    mejor_respuesta = "Lo siento, no tengo una respuesta para eso aún."

    for item in base:
        pregunta_guardada = item["pregunta"].lower()
        puntaje = fuzz.token_set_ratio(pregunta_usuario, pregunta_guardada)

        if puntaje > mejor_puntaje and puntaje > 70:
            mejor_puntaje = puntaje
            mejor_respuesta = item["respuesta"]

    return jsonify({"respuesta": mejor_respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
