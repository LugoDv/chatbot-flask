#!/bin/bash

# Script para renovar certificados SSL de Let's Encrypt
# Debe ejecutarse con permisos de root

DOMAIN="chat-bot-globalleadersusa.duckdns.org"
PROJECT_DIR="/home/usuario/chatbot_global"  # Cambiar por tu ruta real

echo "🔄 Renovando certificados SSL para $DOMAIN..."

# Renovar certificados
certbot renew --quiet

# Verificar si la renovación fue exitosa
if [ $? -eq 0 ]; then
    echo "✅ Certificados renovados exitosamente"
    
    # Reiniciar nginx para aplicar los nuevos certificados
    cd $PROJECT_DIR
    docker-compose restart nginx
    
    if [ $? -eq 0 ]; then
        echo "✅ Nginx reiniciado correctamente"
    else
        echo "❌ Error al reiniciar nginx"
        exit 1
    fi
else
    echo "❌ Error al renovar certificados"
    exit 1
fi

echo "🎉 Proceso de renovación completado"
