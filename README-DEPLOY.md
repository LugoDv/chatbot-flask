# Chatbot Global Leaders - Docker Deploy con HTTPS

## Despliegue rápido

1. **Clona el repositorio en tu servidor**:
```bash
git clone https://github.com/LugoDv/chatbot-flask.git
cd chatbot-flask
```

2. **Genera certificados SSL**:

   **Para desarrollo/testing local:**
   ```bash
   ./generate_ssl.sh -d
   ```

   **Para servidor con IP pública (sin dominio):**
   ```bash
   # Ejemplo: si tu servidor tiene IP 203.0.113.45
   ./generate_ssl.sh -i 203.0.113.45
   ```

   **Para servidor con dominio (Let's Encrypt):**
   ```bash
   # Ejemplo: si tu dominio es chatbot.tuempresa.com
   ./generate_ssl.sh -p chatbot.tuempresa.com
   ```

   **Requisitos según el caso:**
   - **IP pública**: Solo necesitas la IP de tu servidor
   - **Dominio**: El dominio debe apuntar a tu servidor + puertos 80/443 abiertos

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

### 1. Servidor con IP pública (sin dominio) - MÁS COMÚN PARA APIs
```bash
# Usa la IP pública de tu servidor
./generate_ssl.sh -i TU_IP_PUBLICA

# Ejemplo:
./generate_ssl.sh -i 203.0.113.45
```

**Ventajas:**
- ✅ No necesitas dominio
- ✅ Funciona inmediatamente
- ✅ Perfecto para APIs

**Uso:**
- URL: `https://203.0.113.45:8443/chatbot`
- Los clientes deben usar `-k` con curl o aceptar certificado auto-firmado

### 2. Certificados de desarrollo local
```bash
./generate_ssl.sh -d
```

### 3. Servidor con dominio (Let's Encrypt)
```bash
./generate_ssl.sh -p tu-dominio.com
```

**Solo si tienes un dominio que apunte a tu servidor.**

### Renovación automática
Para renovar automáticamente los certificados, agrega esto al crontab:
```bash
# Editar crontab
crontab -e

# Agregar esta línea (renovar cada 12 horas)
0 0,12 * * * /ruta/a/tu/proyecto/renew_ssl.sh tu-dominio.com
```

O usar el script de renovación manualmente:
```bash
./renew_ssl.sh tu-dominio.com
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
