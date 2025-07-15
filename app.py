from flask import Flask, request, jsonify
from rapidfuzz import fuzz
from flask_cors import CORS
import json ,os
import re

app = Flask(__name__)
CORS(app)

# Carga los archivos JSON una vez al iniciar
with open("preguntas.json", "r", encoding="utf-8") as f:
    base_spanish = json.load(f)

with open("questions_english.json", "r", encoding="utf-8") as f:
    base_english = json.load(f)

def convert_links_to_html(text, language="es"):
    """Convierte enlaces en texto a hipervínculos HTML"""
    # Primero verificar si ya contiene enlaces HTML para evitar doble procesamiento
    if '<a href=' in text:
        return text
    
    # Convertir enlaces de WhatsApp según el idioma
    if language == "en":
        text = re.sub(
            r'(https://wa\.me/[0-9]+)',
            r'<a href="\1" target="_blank" rel="noopener noreferrer" style="color: #25D366; text-decoration: underline; font-weight: bold;">📱 Contact WhatsApp</a>',
            text
        )
        # Convertir enlaces de Google Forms
        text = re.sub(
            r'(https://docs\.google\.com/forms/d/[A-Za-z0-9_-]+/[^\s]*)',
            r'<a href="\1" target="_blank" rel="noopener noreferrer" style="color: #1a73e8; text-decoration: underline; font-weight: bold;">📝 Registration Form</a>',
            text
        )
    else:
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

def process_chatbot_query(pregunta_usuario, base_preguntas, fallback_message, language="es"):
    """Procesa una consulta del chatbot usando la base de datos especificada"""
    mejor_puntaje = 0
    mejor_respuesta = ""
    sugerencias = []

    for item in base_preguntas:
        pregunta_guardada = item["pregunta"].lower()
        
        # Usar token_set_ratio para mejor matching con RapidFuzz
        puntaje = fuzz.token_set_ratio(pregunta_usuario, pregunta_guardada)
        
        # También probar con ratio simple para capturar más variaciones
        puntaje_simple = fuzz.ratio(pregunta_usuario, pregunta_guardada)
        
        # Usar el mejor puntaje de ambos métodos
        puntaje_final = max(puntaje, puntaje_simple)

        if puntaje_final > mejor_puntaje:
            mejor_puntaje = puntaje_final
            mejor_respuesta = item["respuesta"]
            sugerencias = item.get("sugerencias", [])

    # Umbral más bajo para aprovechar la mayor precisión de RapidFuzz
    if mejor_puntaje < 55:
        mejor_respuesta = fallback_message
        sugerencias = []

    # Convertir enlaces a HTML antes de enviar la respuesta
    mejor_respuesta_html = convert_links_to_html(mejor_respuesta, language)

    return {
        "respuesta": mejor_respuesta_html,
        "sugerencias": sugerencias,
        "score": mejor_puntaje  # Añadir score para debugging
    }

@app.route("/chatbot", methods=["POST"])
def chatbot_spanish():
    """Endpoint para consultas en español"""
    datos = request.get_json()
    pregunta_usuario = datos.get("message", "").lower()
    
    fallback_message = "🤔 No tengo una respuesta clara para eso. Pero puedes preguntarme sobre visado, entrevistas, requisitos, pagos... O escribirnos por WhatsApp 👉 https://wa.me/34640030604"
    
    result = process_chatbot_query(pregunta_usuario, base_spanish, fallback_message, "es")
    
    if not result["sugerencias"]:
        result["sugerencias"] = [
            "¿Cómo es la entrevista?",
            "¿Qué documentos necesito?",
            "¿Cuánto cuesta el programa?"
        ]
    
    return jsonify(result)

@app.route("/chatbot/en", methods=["POST"])
def chatbot_english():
    """Endpoint para consultas en inglés"""
    datos = request.get_json()
    pregunta_usuario = datos.get("message", "").lower()
    
    fallback_message = "🤔 I don't have a clear answer for that. But you can ask me about visas, interviews, requirements, payments... Or write to us on WhatsApp 👉 https://wa.me/34640030604"
    
    result = process_chatbot_query(pregunta_usuario, base_english, fallback_message, "en")
    
    if not result["sugerencias"]:
        result["sugerencias"] = [
            "How is the interview?",
            "What documents do I need?",
            "How much does the program cost?"
        ]
    
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
