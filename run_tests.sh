#!/bin/bash

# Script para testing completo del chatbot

echo "🚀 INICIANDO TESTING COMPLETO DEL CHATBOT"
echo "========================================"

# Verificar que existe el archivo principal
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encuentra app.py"
    exit 1
fi

if [ ! -f "preguntas.json" ]; then
    echo "❌ Error: No se encuentra preguntas.json"
    exit 1
fi

echo ""
echo "1️⃣ Ejecutando tests de validación..."
python test_validation.py

echo ""
echo "2️⃣ Ejecutando tests de lógica..."
python test_chatbot.py

echo ""
echo "3️⃣ Iniciando servidor Flask..."
echo "   (Ctrl+C para detener)"
echo ""
echo "🌐 Una vez que el servidor esté corriendo:"
echo "   - Abre test_interface.html en tu navegador"
echo "   - O prueba con curl:"
echo "     curl -X POST -H 'Content-Type: application/json' -d '{\"message\":\"hola\"}' http://localhost:5000/chatbot"
echo ""

# Ejecutar el servidor
python app.py
