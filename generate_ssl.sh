#!/bin/bash

# Script para generar certificados SSL
# Soporta certificados auto-firmados para desarrollo, producción con IP, y Let's Encrypt con dominio

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}Uso: $0 [OPCIÓN] [DOMINIO/IP]${NC}"
    echo ""
    echo "Opciones:"
    echo "  -d, --dev                    Generar certificados auto-firmados para desarrollo"
    echo "  -i, --ip IP_PUBLICA          Generar certificados para IP pública (sin dominio)"
    echo "  -p, --prod DOMINIO           Generar certificados reales con Let's Encrypt"
    echo "  -h, --help                   Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 -d                        # Certificados para desarrollo local"
    echo "  $0 -i 192.168.1.100          # Certificados para IP pública"
    echo "  $0 -p chatbot.tudominio.com  # Certificados con dominio real"
}

# Función para certificados de desarrollo
generate_dev_certs() {
    echo -e "${YELLOW}🔧 Generando certificados SSL auto-firmados para desarrollo...${NC}"
    
    mkdir -p ssl
    
    # Generar certificado SSL auto-firmado para desarrollo
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=CO/ST=Bogota/L=Bogota/O=GlobalLeaders/OU=IT/CN=localhost" \
        -addext "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1"
    
    # Asegurar permisos correctos
    chmod 600 ssl/key.pem
    chmod 644 ssl/cert.pem
    
    echo -e "${GREEN}✅ Certificados SSL generados para desarrollo${NC}"
    echo -e "${YELLOW}⚠️  Estos son certificados auto-firmados, solo para desarrollo local${NC}"
    echo -e "${BLUE}🌐 Usar con: https://localhost:8443${NC}"
}

# Función para certificados con IP pública
generate_ip_certs() {
    local ip_address=$1
    
    if [[ -z "$ip_address" ]]; then
        echo -e "${RED}❌ Error: Debes especificar la IP pública del servidor${NC}"
        echo "Ejemplo: $0 -i 203.0.113.45"
        exit 1
    fi
    
    # Validar formato de IP
    if ! [[ $ip_address =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        echo -e "${RED}❌ Error: IP no válida: $ip_address${NC}"
        echo "Ejemplo: $0 -i 203.0.113.45"
        exit 1
    fi
    
    echo -e "${YELLOW}🔧 Generando certificados SSL para IP pública: $ip_address${NC}"
    
    mkdir -p ssl
    
    # Generar certificado SSL auto-firmado para IP específica
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=CO/ST=Bogota/L=Bogota/O=GlobalLeaders/OU=IT/CN=$ip_address" \
        -addext "subjectAltName=IP:$ip_address,IP:127.0.0.1"
    
    # Asegurar permisos correctos
    chmod 600 ssl/key.pem
    chmod 644 ssl/cert.pem
    
    echo -e "${GREEN}✅ Certificados SSL generados para IP pública${NC}"
    echo -e "${YELLOW}⚠️  Certificados auto-firmados para API sin dominio${NC}"
    echo -e "${BLUE}🌐 Usar con: https://$ip_address:8443/chatbot${NC}"
    echo -e "${BLUE}🔧 Los clientes deberán ignorar advertencias SSL o agregar excepción${NC}"
}

# Función para certificados de producción con dominio
generate_prod_certs() {
    local domain=$1
    
    if [[ -z "$domain" ]]; then
        echo -e "${RED}❌ Error: Debes especificar un dominio para Let's Encrypt${NC}"
        echo "Ejemplo: $0 -p chatbot.tudominio.com"
        exit 1
    fi
    
    echo -e "${YELLOW}🔧 Configurando certificados SSL reales para: $domain${NC}"
    
    # Verificar si certbot está instalado
    if ! command -v certbot &> /dev/null; then
        echo -e "${YELLOW}📦 Instalando certbot...${NC}"
        
        # Detectar el sistema operativo
        if [[ -f /etc/debian_version ]]; then
            # Ubuntu/Debian
            sudo apt update
            sudo apt install -y certbot
        elif [[ -f /etc/redhat-release ]]; then
            # CentOS/RHEL
            sudo yum install -y epel-release
            sudo yum install -y certbot
        else
            echo -e "${RED}❌ Sistema operativo no soportado automáticamente${NC}"
            echo "Instala certbot manualmente y vuelve a ejecutar el script"
            exit 1
        fi
    fi
    
    # Crear directorio SSL
    mkdir -p ssl
    
    echo -e "${BLUE}🌐 Generando certificados Let's Encrypt para $domain...${NC}"
    echo -e "${YELLOW}⚠️  Asegúrate de que:${NC}"
    echo "   - El dominio $domain apunta a este servidor"
    echo "   - Los puertos 80 y 443 están abiertos"
    echo "   - No hay otros servicios usando el puerto 80"
    echo ""
    
    # Generar certificados con Let's Encrypt
    sudo certbot certonly \
        --standalone \
        --preferred-challenges http \
        --email admin@$(echo $domain | cut -d. -f2-) \
        --agree-tos \
        --no-eff-email \
        -d $domain
    
    # Copiar certificados al directorio ssl
    sudo cp /etc/letsencrypt/live/$domain/fullchain.pem ssl/cert.pem
    sudo cp /etc/letsencrypt/live/$domain/privkey.pem ssl/key.pem
    
    # Ajustar permisos
    sudo chown $(whoami):$(whoami) ssl/cert.pem ssl/key.pem
    chmod 644 ssl/cert.pem
    chmod 600 ssl/key.pem
    
    echo -e "${GREEN}✅ Certificados SSL reales generados correctamente${NC}"
    echo -e "${BLUE}🌐 Usar con: https://$domain:8443/chatbot${NC}"
}

# Función para verificar certificados
verify_certs() {
    if [[ -f ssl/cert.pem && -f ssl/key.pem ]]; then
        echo -e "${GREEN}✅ Certificados encontrados${NC}"
        echo -e "${BLUE}📋 Información del certificado:${NC}"
        openssl x509 -in ssl/cert.pem -text -noout | grep -E "(Subject:|Issuer:|Not Before:|Not After :|DNS:|IP Address:)" | head -10
        echo ""
        echo -e "${BLUE}🔍 Verificación de la llave privada:${NC}"
        cert_hash=$(openssl x509 -in ssl/cert.pem -pubkey -noout | openssl md5)
        key_hash=$(openssl rsa -in ssl/key.pem -pubout 2>/dev/null | openssl md5)
        if [[ "$cert_hash" == "$key_hash" ]]; then
            echo -e "${GREEN}✅ Certificado y llave privada coinciden${NC}"
        else
            echo -e "${RED}❌ Error: Certificado y llave privada no coinciden${NC}"
        fi
    else
        echo -e "${RED}❌ No se encontraron certificados SSL${NC}"
    fi
}

# Parsear argumentos
case $1 in
    -d|--dev)
        generate_dev_certs
        verify_certs
        ;;
    -i|--ip)
        generate_ip_certs $2
        verify_certs
        ;;
    -p|--prod)
        generate_prod_certs $2
        verify_certs
        ;;
    -h|--help)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Opción no válida: $1${NC}"
        show_help
        exit 1
        ;;
esac

echo -e "${GREEN}🚀 ¡Listo! Ahora puedes ejecutar docker-compose up -d --build${NC}"
