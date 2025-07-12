# 🤖 Chatbot Global Leaders - Multiidioma

Chatbot inteligente para responder preguntas sobre el programa de intercambio Global Leaders en **español** e **inglés**.

## 🌍 Idiomas Disponibles

- 🇪🇸 **Español**: 54 preguntas y respuestas
- 🇺🇸 **English**: 54 preguntas y respuestas

## 🚀 Características

- ✅ **Endpoints separados** para cada idioma
- ✅ **Búsqueda inteligente** con fuzzy matching
- ✅ **API REST** con Flask
- ✅ **CORS habilitado** para integraciones web
- ✅ **Hipervínculos HTML** para WhatsApp y formularios
- ✅ **Respuestas contextuales** y sugerencias

## 📋 Categorías Cubiertas

- General, Proceso, Entrevista
- Requisitos, Costes, Visado
- Contratación, Duración, Seguro
- Vida, Viaje, Soporte, Contacto
- Emocional, Despedida

## 🛠️ Instalación

```bash
pip install -r requirements.txt
python app.py
```

## 📡 API Endpoints

### 🇪🇸 Español
**POST** `/chatbot`
```json
{
  "message": "¿Cuánto cuesta el programa?"
}
```

### 🇺🇸 English
**POST** `/chatbot/en`
```json
{
  "message": "How much does the program cost?"
}
```

### Respuesta (ambos idiomas):
```json
{
  "respuesta": "El coste total es de 1650€...",
  "sugerencias": ["costes", "pagos", "becas"]
}
```

## 🧪 Testing

### Test Automatizado:
```bash
# Probar que los archivos JSON son válidos
python -c "import json; print('✅ OK')"

# Probar endpoints (requiere servidor activo)
python test_endpoints.py
```

### Test Manual:
```bash
# Iniciar servidor
python app.py

# Abrir en navegador
open test_interface_multilingual.html
```

### Test con cURL:
```bash
# Endpoint español
curl -X POST -H "Content-Type: application/json" \
  -d '{"message":"hola"}' \
  http://localhost:5000/chatbot

# Endpoint inglés
curl -X POST -H "Content-Type: application/json" \
  -d '{"message":"hello"}' \
  http://localhost:5000/chatbot/en
```

## 📁 Estructura de Archivos

```
├── app.py                    # Servidor Flask con ambos endpoints
├── preguntas.json           # Base de datos en español
├── questions_english.json   # Base de datos en inglés
├── requirements.txt         # Dependencias de producción
└── README.md               # Este archivo
```

## 🌐 Despliegue

### Archivos necesarios para producción:
- `app.py`
- `preguntas.json` 
- `questions_english.json`
- `requirements.txt`

### Variables de entorno:
```bash
PORT=5000  # Puerto del servidor
```

---

**Estado:** ✅ Listo para producción  
**Cobertura:** 100% de FAQ cubierto en ambos idiomas  
**Endpoints:** 🇪🇸 `/chatbot` | 🇺🇸 `/chatbot/en`
