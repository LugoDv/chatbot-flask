#!/bin/bash

# Script para generar certificados SSL auto-firmados
# Para desarrollo y testing

mkdir -p ssl

# Generar certificado SSL auto-firmado
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/C=CO/ST=Bogota/L=Bogota/O=GlobalLeaders/OU=IT/CN=localhost"

echo "Certificados SSL generados en el directorio ssl/"
echo "Para usar en producción, reemplaza con certificados reales de Let's Encrypt o similar"

# Asegurar permisos correctos
chmod 600 ssl/key.pem
chmod 644 ssl/cert.pem

echo "Permisos configurados correctamente"
