# Ejemplos de configuración de puertos alternativos

# Para usar puertos estándar (requiere sudo/root)
ports:
  - "80:80"     # HTTP estándar
  - "443:443"   # HTTPS estándar

# Para usar puertos personalizados
ports:
  - "3000:80"   # HTTP en puerto 3000
  - "3443:443"  # HTTPS en puerto 3443

# Para usar solo HTTPS
ports:
  - "8443:443"  # Solo HTTPS (recomendado para producción)

# Para desarrollo local
ports:
  - "8080:80"   # HTTP en 8080
  - "8443:443"  # HTTPS en 8443 (configuración actual)
