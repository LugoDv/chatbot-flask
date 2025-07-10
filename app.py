from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz
from flask_cors import CORS
import json ,os
import re

app = Flask(__name__)
CORS(app)

# Carga el archivo JSON una vez al iniciar
with open("preguntas.json", "r", encoding="utf-8") as f:
    base = json.load(f)

def convert_links_to_html(text):
    """Convierte enlaces en texto a hipervínculos HTML"""
    # Convertir enlaces de WhatsApp
    text = re.sub(
        r'(https://wa\.me/[0-9]+)',
        r'<a href="\1" target="_blank" rel="noopener noreferrer" style="color: #25D366; text-decoration: underline; font-weight: bold;">📱 Contactar por WhatsApp</a>',
        text
    )
    
    # Convertir enlaces de Google Forms
    text = re.sub(
        r'(https://docs\.google\.com/forms/d/[A-Za-z0-9_-]+/[^\s]*)',
        r'<a href="\1" target="_blank" rel="noopener noreferrer" style="color: #1a73e8; text-decoration: underline; font-weight: bold;">📝 Formulario de inscripción</a>',
        text
    )
    
    # Convertir saltos de línea a <br>
    text = text.replace('\n', '<br>')
    
    return text

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
        mejor_respuesta = "🤔 No tengo una respuesta clara para eso. Pero puedes preguntarme sobre visado, entrevistas, requisitos, pagos... O escribirnos por WhatsApp 👉 https://wa.me/34640030604"
        sugerencias = [
            "¿Cómo es la entrevista?",
            "¿Qué documentos necesito?",
            "¿Cuánto cuesta el programa?"
        ]

    # Convertir enlaces a HTML antes de enviar la respuesta
    mejor_respuesta_html = convert_links_to_html(mejor_respuesta)

    return jsonify({
        "respuesta": mejor_respuesta_html,
        "sugerencias": sugerencias
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
