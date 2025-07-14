# 📦 Archivos Principales - Production Ready

## Archivos ESENCIALES para producción:

### ✅ Core Application
- `app.py` - Aplicación Flask principal
- `requirements.txt` - Dependencias Python
- `questions.json` - Base de datos español
- `questions_english.json` - Base de datos inglés

### ✅ Docker & Infrastructure
- `Dockerfile` - Imagen Docker de la aplicación
- `docker-compose.yml` - Orquestación de contenedores
- `nginx.conf` - Configuración nginx reverse proxy
- `.dockerignore` - Archivos excluidos del build

### ✅ SSL & Security
- `generate_ssl.sh` - Script para generar certificados SSL
- `renew_ssl.sh` - Script para renovar certificados (auto-generado)

### ✅ Documentation
- `README.md` - Documentación principal
- `README-DEPLOY.md` - Guía de despliegue

### ✅ Configuration
- `.gitignore` - Archivos excluidos del repositorio

## ❌ Archivos REMOVIDOS del repositorio:

### Tests & Development
- `tests_production.py`
- `test_https.html`
- `test_interface.html`
- `test_local.sh`

### Documentation (desarrollo)
- `TESTING_GUIDE.md`
- `PORTS_CONFIG.md`
- `FAQ´s Global Leaders.txt`

### Data duplicada
- `preguntas_new.json` (duplicado de preguntas.json)

## 🔒 Archivos en .gitignore:

### Certificados SSL
- `ssl/` - Directorio con certificados
- `*.pem`, `*.key`, `*.crt` - Archivos de certificados

### Desarrollo
- `venv/` - Entorno virtual
- `__pycache__/` - Cache de Python
- `*.log` - Logs
- Test files varios

### Sistema
- `.DS_Store`, `Thumbs.db` - Archivos del sistema

## 🎯 Resultado final:

Tu repositorio ahora contiene **SOLO** los archivos necesarios para producción:
- ✅ Aplicación optimizada
- ✅ Docker containerizado
- ✅ SSL/HTTPS configurado
- ✅ Documentación clara
- ✅ Sin archivos de desarrollo

**¡Listo para deploy en producción!** 🚀
