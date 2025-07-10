#!/usr/bin/env python3
"""
Script de testing para el chatbot Global Leaders
Prueba diferentes tipos de preguntas y evalúa las respuestas
"""

import json
import requests
import time
from fuzzywuzzy import fuzz

# Cargar las preguntas de referencia
with open("preguntas.json", "r", encoding="utf-8") as f:
    base_preguntas = json.load(f)

# Tests de casos específicos
CASOS_TEST = [
    # === CASOS BÁSICOS ===
    {
        "categoria": "Saludos",
        "tests": [
            "hola",
            "que tal",
            "buenas",
            "me puedes ayudar"
        ]
    },
    
    # === PROCESO ===
    {
        "categoria": "Proceso",
        "tests": [
            "como es el proceso",
            "cuales son los pasos",
            "que necesito hacer",
            "como me registro"
        ]
    },
    
    # === ENTREVISTA ===
    {
        "categoria": "Entrevista",
        "tests": [
            "como es la entrevista",
            "donde se hace la entrevista",
            "por que pagar entrevista",
            "que evaluan en la entrevista"
        ]
    },
    
    # === COSTES ===
    {
        "categoria": "Costes",
        "tests": [
            "cuanto cuesta",
            "como se divide el pago",
            "cuando es mas barato",
            "que incluye el pago de 150"
        ]
    },
    
    # === VISADO ===
    {
        "categoria": "Visado",
        "tests": [
            "como gestiono el visado",
            "cuanto cuesta el visado",
            "donde hago el visado",
            "cuanto tarda el visado"
        ]
    },
    
    # === REQUISITOS ===
    {
        "categoria": "Requisitos",
        "tests": [
            "que edad necesito",
            "necesito ser estudiante",
            "que certificados necesito"
        ]
    },
    
    # === CASOS EDGE ===
    {
        "categoria": "Edge Cases",
        "tests": [
            "asdfghjkl",  # Gibberish
            "pizza",      # Palabra random
            "",           # Vacío
            "123456",     # Números
            "¿¿¿???",     # Solo símbolos
        ]
    }
]

def test_local_logic():
    """Testa la lógica local sin servidor"""
    print("🧪 TESTING LÓGICA LOCAL")
    print("=" * 50)
    
    resultados = {
        "total": 0,
        "exitosos": 0,
        "fallidos": 0,
        "por_categoria": {}
    }
    
    for categoria_test in CASOS_TEST:
        categoria = categoria_test["categoria"]
        tests = categoria_test["tests"]
        
        print(f"\n📂 Categoría: {categoria}")
        print("-" * 30)
        
        categoria_stats = {"total": 0, "exitosos": 0}
        
        for pregunta_test in tests:
            resultados["total"] += 1
            categoria_stats["total"] += 1
            
            # Simular la lógica del chatbot
            mejor_puntaje = 0
            mejor_respuesta = ""
            mejor_pregunta = ""
            
            for item in base_preguntas:
                pregunta_guardada = item["pregunta"].lower()
                puntaje = fuzz.token_set_ratio(pregunta_test.lower(), pregunta_guardada)
                
                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    mejor_respuesta = item["respuesta"]
                    mejor_pregunta = item["pregunta"]
            
            # Evaluar resultado
            if mejor_puntaje >= 60:
                status = "✅ MATCH"
                resultados["exitosos"] += 1
                categoria_stats["exitosos"] += 1
                print(f"  {pregunta_test:<25} -> {mejor_pregunta[:40]}... ({mejor_puntaje}%)")
            else:
                status = "❌ NO MATCH"
                resultados["fallidos"] += 1
                print(f"  {pregunta_test:<25} -> NO ENCONTRADA ({mejor_puntaje}%)")
        
        resultados["por_categoria"][categoria] = categoria_stats
        print(f"  📊 {categoria}: {categoria_stats['exitosos']}/{categoria_stats['total']} exitosos")
    
    return resultados

def test_servidor_api(puerto=5000):
    """Testa el servidor Flask si está corriendo"""
    print(f"\n🌐 TESTING SERVIDOR API (Puerto {puerto})")
    print("=" * 50)
    
    url = f"http://localhost:{puerto}/chatbot"
    
    try:
        # Test de conectividad
        test_payload = {"message": "hola"}
        response = requests.post(url, json=test_payload, timeout=5)
        
        if response.status_code == 200:
            print("✅ Servidor respondiendo correctamente")
            
            # Hacer algunos tests rápidos
            tests_rapidos = [
                "hola",
                "como es la entrevista", 
                "cuanto cuesta",
                "palabra_inexistente"
            ]
            
            for test in tests_rapidos:
                payload = {"message": test}
                resp = requests.post(url, json=payload)
                data = resp.json()
                print(f"  📝 '{test}' -> {data['respuesta'][:50]}...")
                
        else:
            print(f"❌ Error del servidor: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose?")
        print(f"   Para iniciarlo: python app.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def generar_reporte(resultados):
    """Genera un reporte de los resultados"""
    print("\n📊 REPORTE FINAL")
    print("=" * 50)
    
    total = resultados["total"]
    exitosos = resultados["exitosos"]
    fallidos = resultados["fallidos"]
    porcentaje = (exitosos / total * 100) if total > 0 else 0
    
    print(f"Total de tests: {total}")
    print(f"Exitosos: {exitosos}")
    print(f"Fallidos: {fallidos}")
    print(f"Porcentaje de éxito: {porcentaje:.1f}%")
    
    print("\nPor categoría:")
    for categoria, stats in resultados["por_categoria"].items():
        cat_porcentaje = (stats["exitosos"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"  {categoria}: {stats['exitosos']}/{stats['total']} ({cat_porcentaje:.1f}%)")
    
    # Recomendaciones
    print("\n💡 RECOMENDACIONES:")
    if porcentaje >= 90:
        print("🟢 Excelente cobertura de preguntas!")
    elif porcentaje >= 70:
        print("🟡 Buena cobertura, considera agregar más variaciones de preguntas")
    else:
        print("🔴 Cobertura baja, revisa y agrega más preguntas similares")

def main():
    print("🤖 SISTEMA DE TESTING - CHATBOT GLOBAL LEADERS")
    print("=" * 60)
    
    # Test de lógica local
    resultados = test_local_logic()
    
    # Test de servidor (si está corriendo)
    test_servidor_api()
    
    # Generar reporte
    generar_reporte(resultados)
    
    print("\n🎯 Para testing completo:")
    print("1. Ejecuta: python app.py (en otra terminal)")
    print("2. Ejecuta: python test_chatbot.py")
    print("3. Prueba manualmente en: http://localhost:5000")

if __name__ == "__main__":
    main()
