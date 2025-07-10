# 🤖 Chatbot Global Leaders

Chatbot inteligente para responder preguntas sobre el programa de intercambio Global Leaders.

## 🚀 Características

- ✅ **48 preguntas y respuestas** organizadas en 15 categorías
- ✅ **Búsqueda inteligente** con fuzzy matching
- ✅ **API REST** con Flask
- ✅ **CORS habilitado** para integraciones web
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

## 📡 API

**POST** `/chatbot`
```json
{
  "message": "¿Cuánto cuesta el programa?"
}
```

**Respuesta:**
```json
{
  "respuesta": "El coste total es de 1650€...",
  "sugerencias": ["costes", "pagos", "becas"]
}
```

## 🧪 Testing

```bash
python tests_production.py
```

---

**Estado:** ✅ Listo para producción  
**Cobertura:** 100% de FAQ cubierto
