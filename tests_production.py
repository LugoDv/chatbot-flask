#!/usr/bin/env python3
"""
Tests de validación para el chatbot Global Leaders
Optimizado para entornos de producción y CI/CD
"""

import json
import os
import sys
from fuzzywuzzy import fuzz

def cargar_preguntas():
    """Carga las preguntas con manejo de errores"""
    try:
        with open("preguntas.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: No se encuentra preguntas.json")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: preguntas.json no es un JSON válido")
        sys.exit(1)

def simular_chatbot(pregunta_usuario, base_preguntas):
    """Simula la lógica del chatbot"""
    mejor_puntaje = 0
    mejor_respuesta = ""
    sugerencias = []
    pregunta_matched = ""
    
    for item in base_preguntas:
        pregunta_guardada = item["pregunta"].lower()
        puntaje = fuzz.token_set_ratio(pregunta_usuario.lower(), pregunta_guardada)
        
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_respuesta = item["respuesta"]
            sugerencias = item.get("sugerencias", [])
            pregunta_matched = item["pregunta"]
    
    if mejor_puntaje < 60:
        mejor_respuesta = "🤔 No tengo una respuesta clara para eso..."
        sugerencias = ["¿Cómo es la entrevista?", "¿Qué documentos necesito?", "¿Cuánto cuesta el programa?"]
        pregunta_matched = "FALLBACK"
    
    return {
        "respuesta": mejor_respuesta,
        "sugerencias": sugerencias,
        "puntaje": mejor_puntaje,
        "pregunta_matched": pregunta_matched
    }

# Tests críticos para producción
TESTS_CRITICOS = [
    {
        "categoria": "Saludos",
        "casos": [
            {"entrada": "hola", "debe_contener": ["👋"], "min_score": 80},
            {"entrada": "que tal", "debe_contener": ["😊"], "min_score": 70},
        ]
    },
    {
        "categoria": "Entrevista",
        "casos": [
            {"entrada": "como es la entrevista", "debe_contener": ["🎥", "online"], "min_score": 85},
            {"entrada": "por que pagar entrevista", "debe_contener": ["20 €"], "min_score": 80},
        ]
    },
    {
        "categoria": "Costes",
        "casos": [
            {"entrada": "cuanto cuesta", "debe_contener": ["329 €"], "min_score": 80},
            {"entrada": "como se divide pago", "debe_contener": ["fases"], "min_score": 80},
        ]
    },
    {
        "categoria": "Visado",
        "casos": [
            {"entrada": "como gestiono visado", "debe_contener": ["J-1", "Madrid"], "min_score": 80},
            {"entrada": "cuanto cuesta visado", "debe_contener": ["185 USD"], "min_score": 85},
        ]
    }
]

def ejecutar_tests_criticos():
    """Ejecuta solo los tests críticos para producción"""
    base_preguntas = cargar_preguntas()
    
    print("🎯 TESTS CRÍTICOS DE PRODUCCIÓN")
    print("=" * 50)
    
    total_tests = 0
    tests_pasados = 0
    fallos = []
    
    for categoria_test in TESTS_CRITICOS:
        categoria = categoria_test["categoria"]
        casos = categoria_test["casos"]
        
        print(f"\n📂 {categoria}")
        print("-" * 30)
        
        for caso in casos:
            total_tests += 1
            entrada = caso["entrada"]
            debe_contener = caso["debe_contener"]
            min_score = caso.get("min_score", 70)
            
            resultado = simular_chatbot(entrada, base_preguntas)
            respuesta = resultado["respuesta"]
            puntaje = resultado["puntaje"]
            
            # Verificaciones
            contiene_todos = all(palabra.lower() in respuesta.lower() for palabra in debe_contener)
            score_ok = puntaje >= min_score
            
            if contiene_todos and score_ok:
                status = "✅ PASS"
                tests_pasados += 1
            else:
                status = "❌ FAIL"
                fallos.append({
                    "entrada": entrada,
                    "problema": f"Score: {puntaje}%, Contenido: {contiene_todos}"
                })
                
            print(f"  {entrada:<25} -> {status} ({puntaje}%)")
    
    # Resultado final
    porcentaje = (tests_pasados / total_tests * 100) if total_tests > 0 else 0
    print(f"\n📊 RESULTADO: {tests_pasados}/{total_tests} tests pasados ({porcentaje:.1f}%)")
    
    # Si hay fallos, mostrarlos
    if fallos:
        print("\n❌ FALLOS DETECTADOS:")
        for fallo in fallos:
            print(f"  - {fallo['entrada']}: {fallo['problema']}")
    
    # Exit code para CI/CD
    if porcentaje < 90:
        print("\n🔴 TESTS CRÍTICOS FALLARON - No apto para producción")
        sys.exit(1)
    else:
        print("\n🟢 TESTS CRÍTICOS PASADOS - Apto para producción")
        sys.exit(0)

def verificar_estructura_datos():
    """Verifica que la estructura de datos sea correcta"""
    base_preguntas = cargar_preguntas()
    
    print("\n🔍 VERIFICANDO ESTRUCTURA DE DATOS")
    print("-" * 40)
    
    errores = []
    
    for i, item in enumerate(base_preguntas):
        # Verificar campos obligatorios
        if "pregunta" not in item:
            errores.append(f"Item {i}: Falta campo 'pregunta'")
        if "respuesta" not in item:
            errores.append(f"Item {i}: Falta campo 'respuesta'")
        if "tema" not in item:
            errores.append(f"Item {i}: Falta campo 'tema'")
        
        # Verificar que no estén vacíos
        if item.get("pregunta", "").strip() == "":
            errores.append(f"Item {i}: Pregunta vacía")
        if item.get("respuesta", "").strip() == "":
            errores.append(f"Item {i}: Respuesta vacía")
    
    if errores:
        print("❌ ERRORES EN ESTRUCTURA:")
        for error in errores:
            print(f"  - {error}")
        return False
    else:
        print("✅ Estructura de datos correcta")
        return True

def main():
    """Función principal para CI/CD"""
    print("🤖 VALIDACIÓN DE PRODUCCIÓN - CHATBOT GLOBAL LEADERS")
    print("=" * 60)
    
    # Verificar estructura
    if not verificar_estructura_datos():
        sys.exit(1)
    
    # Ejecutar tests críticos
    ejecutar_tests_criticos()

if __name__ == "__main__":
    main()
