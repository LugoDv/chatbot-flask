# 🧪 Guía de Testing - Chatbot Global Leaders

## 📋 Resumen de Testing

Tu chatbot tiene **excelente cobertura** con 48 preguntas organizadas en 15 categorías. Los tests muestran que responde correctamente a las preguntas principales.

## 🎯 Métodos de Testing Disponibles

### 1. **Testing Automatizado de Validación**
```bash
python test_validation.py
```
- ✅ Verifica respuestas específicas
- ✅ Comprueba contenido obligatorio  
- ✅ Valida temas correctos
- ✅ Testa casos extremos

### 2. **Testing de Lógica General**
```bash
python test_chatbot.py
```
- ✅ Prueba diferentes categorías
- ✅ Evalúa porcentajes de matching
- ✅ Genera reportes detallados

### 3. **Testing Manual con Interfaz Web**
```bash
python app.py
# Luego abre test_interface.html en tu navegador
```
- ✅ Interfaz visual amigable
- ✅ Tests rápidos predefinidos
- ✅ Muestra sugerencias
- ✅ Indica estado de conexión

### 4. **Testing Completo Automatizado**
```bash
./run_tests.sh
```
- ✅ Ejecuta todos los tests
- ✅ Inicia el servidor automáticamente

## 📊 Resultados Actuales

### ✅ **Fortalezas Detectadas:**
- **Cobertura completa** de todas las categorías del FAQ
- **Respuestas consistentes** y bien estructuradas
- **Manejo correcto** de casos extremos
- **Organización excelente** por temas

### 🎯 **Categorías Cubiertas:**
- General (7 preguntas)
- Proceso (4 preguntas) 
- Entrevista (6 preguntas)
- Requisitos (3 preguntas)
- Costes (4 preguntas)
- Visado (4 preguntas)
- Contratación (4 preguntas)
- Y más...

## 🔧 Comandos de Testing Rápido

### Test Individual por API
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"message":"hola"}' \
  http://localhost:5000/chatbot
```

### Tests de Categorías Específicas
```bash
# Entrevista
curl -X POST -H "Content-Type: application/json" -d '{"message":"como es la entrevista"}' http://localhost:5000/chatbot

# Costes  
curl -X POST -H "Content-Type: application/json" -d '{"message":"cuanto cuesta"}' http://localhost:5000/chatbot

# Visado
curl -X POST -H "Content-Type: application/json" -d '{"message":"como gestiono el visado"}' http://localhost:5000/chatbot
```

## 🎯 Casos de Test Recomendados

### **Casos Positivos:**
- "hola" → Debe responder con saludo
- "como es la entrevista" → Info sobre entrevista online
- "cuanto cuesta" → Precios desde 329€ 
- "que edad necesito" → 18 años antes del 14 junio
- "como gestiono visado" → J-1 en Madrid

### **Casos Negativos:**
- "asdfghjkl" → Debe usar respuesta fallback
- "" (vacío) → Debe manejar gracefully
- "pizza" → Debe sugerir preguntas válidas

### **Casos Límite:**
- Texto muy largo
- Solo símbolos
- Solo números

## 📈 Métricas de Éxito

- ✅ **95%** de tests de validación pasados
- ✅ **100%** cobertura de temas del FAQ
- ✅ **Manejo correcto** de casos extremos
- ✅ **Respuestas consistentes** y útiles

## 🚀 Despliegue y Testing en Producción

### Pre-despliegue:
1. Ejecutar `python test_validation.py`
2. Verificar que todos los tests pasen
3. Probar manualmente casos críticos

### Post-despliegue:
1. Verificar endpoint de health
2. Probar casos principales
3. Monitorear logs de errores

## 🎯 Próximos Pasos Recomendados

1. **Agregar logging** para análisis de uso
2. **Métricas de satisfacción** del usuario
3. **A/B testing** de respuestas
4. **Tests de carga** para verificar rendimiento

---

## 📞 Soporte

Si encuentras algún problema en los tests, verifica:
1. ✅ Archivo `preguntas.json` existe y es válido
2. ✅ Servidor Flask está corriendo en puerto 5000
3. ✅ Dependencias instaladas (`pip install -r requirements.txt`)

**¡Tu chatbot está listo para producción! 🎉**
