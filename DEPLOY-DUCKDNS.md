# 🚀 Despliegue con Dominio DuckDNS

## Prerrequisitos en el servidor

### 1. Configurar DNS
En [duckdns.org](https://duckdns.org):
- Dominio: `chat-bot-globalleadersusa.duckdns.org`
- IP: `191.101.232.48`

### 2. Instalar dependencias
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Instalar Certbot para Let's Encrypt
sudo apt install snapd
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

### 3. Configurar firewall
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw --force enable
```

## Proceso de despliegue

### 1. Clonar repositorio
```bash
git clone -b develop --single-branch --depth 1 https://github.com/LugoDv/chatbot-flask.git
cd chatbot-flask
```

### 2. Generar certificado SSL
```bash
# Parar cualquier servicio en puerto 80
sudo systemctl stop apache2 nginx 2>/dev/null || true

# Generar certificado Let's Encrypt
sudo certbot certonly --standalone -d chat-bot-globalleadersusa.duckdns.org

# Verificar certificados
sudo ls -la /etc/letsencrypt/live/chat-bot-globalleadersusa.duckdns.org/
```

### 3. Desplegar aplicación
```bash
# Construir y ejecutar
sudo docker-compose build
sudo docker-compose up -d

# Verificar estado
sudo docker-compose ps
sudo docker-compose logs
```

### 4. Configurar renovación automática
```bash
# Hacer ejecutable el script
chmod +x renew_ssl_letsencrypt.sh

# Actualizar ruta en el script
sudo nano renew_ssl_letsencrypt.sh
# Cambiar PROJECT_DIR por la ruta real

# Mover script al sistema
sudo cp renew_ssl_letsencrypt.sh /usr/local/bin/

# Configurar cron para renovación automática
sudo crontab -e
# Añadir: 0 2 * * 1 /usr/local/bin/renew_ssl_letsencrypt.sh >> /var/log/ssl-renewal.log 2>&1
```

## URLs finales
- **Español**: `https://chat-bot-globalleadersusa.duckdns.org/chatbot`
- **Inglés**: `https://chat-bot-globalleadersusa.duckdns.org/chatbot/en`
- **Health check**: `https://chat-bot-globalleadersusa.duckdns.org/health`

## Pruebas
```bash
# Probar endpoint español
curl -k https://chat-bot-globalleadersusa.duckdns.org/chatbot -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "hola"}'

# Probar endpoint inglés
curl -k https://chat-bot-globalleadersusa.duckdns.org/chatbot/en -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

## Comandos útiles
```bash
# Ver logs
sudo docker-compose logs -f

# Reiniciar servicio
sudo docker-compose restart

# Actualizar aplicación
git pull origin develop
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d

# Verificar certificados
sudo certbot certificates

# Renovar manualmente
sudo certbot renew
```
