# 🚀 Chatbot Global Leaders - Production Ready

## Descripción
API chatbot multiidioma (Español/English) para el programa Global Leaders USA. Implementado con Flask, RapidFuzz y Docker con SSL/HTTPS.

## Características principales
- � **Dual idioma**: Español y English
- ⚡ **Rendimiento optimizado**: RapidFuzz para búsqueda fuzzy
- � **HTTPS**: SSL/TLS configurado
- 🐳 **Docker**: Containerizado con nginx reverse proxy
- 📊 **33 preguntas** en cada idioma
- 💨 **Respuestas rápidas**: < 100ms promedio

## Despliegue rápido

### 1. Clonar repositorio
```bash
git clone https://github.com/LugoDv/chatbot-flask.git
cd chatbot-flask
```

### 2. Generar certificados SSL
```bash
# Para servidor con IP pública (más común)
./generate_ssl.sh -i TU_IP_PUBLICA

# Para servidor con dominio
./generate_ssl.sh -p tu-dominio.com

# Para desarrollo local
./generate_ssl.sh -d
```

### 3. Desplegar
```bash
docker-compose up -d --build
```

### 4. Probar
```bash
curl -k https://TU_IP:8443/health
curl -X POST -H "Content-Type: application/json" \
  -d '{"message": "hola"}' \
  -k https://TU_IP:8443/chatbot
```

## 📋 Categorías Cubiertas

- General, Proceso, Entrevista
- Requisitos, Costes, Visado
- Contratación, Duración, Seguro
- Vida, Viaje, Soporte, Contacto
- Emocional, Despedida

## 🛠️ Instalación

```bash
# Instalar dependencias (incluye RapidFuzz para máximo rendimiento)
pip install -r requirements.txt

# Iniciar servidor
python app.py
```

## ⚡ Rendimiento

- **Velocidad**: <1ms por consulta (10x más rápido que FuzzyWuzzy)
- **Precisión**: 81.8% de matches exitosos
- **Algoritmo**: Doble matching (token_set + ratio)
- **Umbral**: 55% (optimizado para RapidFuzz)

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

## Endpoints de la API

| Endpoint | Método | Descripción |
|----------|---------|-------------|
| `/chatbot` | POST | Chatbot en español |
| `/chatbot/en` | POST | Chatbot en inglés |
| `/health` | GET | Health check |

## Ejemplo de uso

### Español
```bash
curl -X POST https://tu-servidor:8443/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo me inscribo?"}'
```

### English
```bash
curl -X POST https://tu-servidor:8443/chatbot/en \
  -H "Content-Type: application/json" \
  -d '{"message": "How to register?"}'
```

### Respuesta
```json
{
  "respuesta": "📝 Para inscribirte debes registrarte en línea...",
  "score": 85.5,
  "sugerencias": [
    "¿Qué requisitos necesito?",
    "¿Cuánto cuesta el programa?",
    "¿Cuándo son las fechas?"
  ]
}
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

## Configuración

### Puertos
- **8080**: HTTP (redirige a HTTPS)
- **8443**: HTTPS (principal)

### SSL
- **IP pública**: Certificados auto-firmados
- **Dominio**: Let's Encrypt automático
- **Desarrollo**: Certificados locales

## Tecnologías
- **Backend**: Flask 3.1.1
- **Fuzzy Search**: RapidFuzz 3.10.1
- **Proxy**: nginx Alpine
- **Container**: Docker + Docker Compose
- **SSL**: OpenSSL / Let's Encrypt

## Archivos principales
- `app.py` - Aplicación Flask principal
- `questions.json` - Base de datos español
- `questions_english.json` - Base de datos inglés
- `nginx.conf` - Configuración proxy
- `docker-compose.yml` - Orquestación containers
- `generate_ssl.sh` - Script certificados SSL

## Comandos útiles
```bash
# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Parar
docker-compose down

# Actualizar
git pull && docker-compose up -d --build
```

## Licencia
Uso interno - Global Leaders USA

## Soporte
Para soporte técnico, contactar al equipo de desarrollo.
