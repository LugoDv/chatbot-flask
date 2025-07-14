# Chatbot Global Leaders - Docker Deploy con HTTPS

## Despliegue rápido

1. **Clona el repositorio en tu servidor**:
```bash
git clone https://github.com/LugoDv/chatbot-flask.git
cd chatbot-flask
```

2. **Genera certificados SSL** (para desarrollo/testing):
```bash
./generate_ssl.sh
```

3. **Ejecuta con Docker Compose**:
```bash
docker-compose up -d --build
```

4. **Verifica que funciona**:
```bash
# HTTP (redirige automáticamente a HTTPS)
curl -X POST http://localhost:8080/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "hola"}'

# HTTPS directo
curl -X POST https://localhost:8443/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "hola"}' \
  -k
```

## Endpoints

- **Español**: `POST https://tu-servidor:8443/chatbot`
- **Inglés**: `POST https://tu-servidor:8443/chatbot/en`
- **Health**: `GET https://tu-servidor:8443/health`

## Configuración SSL

### Certificados de desarrollo
Los certificados auto-firmados son generados automáticamente con `generate_ssl.sh`.

### Certificados de producción
Para producción, usa certificados reales de Let's Encrypt:
```bash
sudo apt install certbot
sudo certbot certonly --standalone -d tu-dominio.com
cp /etc/letsencrypt/live/tu-dominio.com/fullchain.pem ssl/cert.pem
cp /etc/letsencrypt/live/tu-dominio.com/privkey.pem ssl/key.pem
```

## Comandos útiles

```bash
# Ver logs
docker-compose logs -f

# Parar
docker-compose down

# Reiniciar
docker-compose restart
```

La aplicación estará disponible en:
- HTTP: puerto 8080 (redirige a HTTPS)
- HTTPS: puerto 8443

## Cambiar puertos

Si necesitas usar otros puertos, edita el `docker-compose.yml`:

```yaml
ports:
  - "PUERTO_HTTP:80"    # Por ejemplo: "3000:80"
  - "PUERTO_HTTPS:443"  # Por ejemplo: "3443:443"
```
