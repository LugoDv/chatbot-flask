#!/usr/bin/env python3
"""
Pruebas automatizadas específicas para validar respuestas del chatbot
"""

import json
from fuzzywuzzy import fuzz

# Cargar base de preguntas
with open("preguntas.json", "r", encoding="utf-8") as f:
    base_preguntas = json.load(f)

def simular_chatbot(pregunta_usuario):
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

# Tests específicos con respuestas esperadas
TESTS_VALIDACION = [
    {
        "categoria": "Saludos",
        "casos": [
            {"entrada": "hola", "debe_contener": ["👋", "gusto"], "tema_esperado": "General"},
            {"entrada": "que tal", "debe_contener": ["😊", "Global Leaders"], "tema_esperado": "General"},
            {"entrada": "buenos dias", "debe_contener": ["Buenos días", "☀️"], "tema_esperado": "General"},
        ]
    },
    {
        "categoria": "Entrevista",
        "casos": [
            {"entrada": "como es la entrevista", "debe_contener": ["🎥", "online", "Meet"], "tema_esperado": "Entrevista"},
            {"entrada": "por que pagar entrevista", "debe_contener": ["20 €", "formal"], "tema_esperado": "Entrevista"},
            {"entrada": "donde hacen entrevista", "debe_contener": ["convenio", "presencial"], "tema_esperado": "Entrevista"},
        ]
    },
    {
        "categoria": "Costes",
        "casos": [
            {"entrada": "cuanto cuesta", "debe_contener": ["329 €", "VIP"], "tema_esperado": "Costes"},
            {"entrada": "como se divide pago", "debe_contener": ["fases", "Registro"], "tema_esperado": "Costes"},
            {"entrada": "que incluye 150", "debe_contener": ["video", "plataforma"], "tema_esperado": "Costes"},
        ]
    },
    {
        "categoria": "Visado",
        "casos": [
            {"entrada": "como gestiono visado", "debe_contener": ["J-1", "Madrid"], "tema_esperado": "Visado"},
            {"entrada": "cuanto cuesta visado", "debe_contener": ["185 USD"], "tema_esperado": "Visado"},
            {"entrada": "cuanto tarda visado", "debe_contener": ["5", "10 días"], "tema_esperado": "Visado"},
        ]
    },
    {
        "categoria": "Requisitos",
        "casos": [
            {"entrada": "que edad necesito", "debe_contener": ["18 años", "14 de junio"], "tema_esperado": "Requisitos"},
            {"entrada": "necesito ser estudiante", "debe_contener": ["No", "obligatorio"], "tema_esperado": "Requisitos"},
            {"entrada": "que certificados necesito", "debe_contener": ["médico", "antecedentes"], "tema_esperado": "Requisitos"},
        ]
    }
]

def ejecutar_tests_validacion():
    """Ejecuta tests de validación específicos"""
    print("🎯 TESTS DE VALIDACIÓN DE RESPUESTAS")
    print("=" * 60)
    
    total_tests = 0
    tests_pasados = 0
    
    for categoria_test in TESTS_VALIDACION:
        categoria = categoria_test["categoria"]
        casos = categoria_test["casos"]
        
        print(f"\n📂 {categoria}")
        print("-" * 40)
        
        for caso in casos:
            total_tests += 1
            entrada = caso["entrada"]
            debe_contener = caso["debe_contener"]
            tema_esperado = caso.get("tema_esperado")
            
            # Simular respuesta del chatbot
            resultado = simular_chatbot(entrada)
            respuesta = resultado["respuesta"]
            puntaje = resultado["puntaje"]
            
            # Verificar contenido
            contiene_todos = all(palabra.lower() in respuesta.lower() for palabra in debe_contener)
            
            # Encontrar el tema de la pregunta matched
            tema_actual = None
            for item in base_preguntas:
                if item["pregunta"] == resultado["pregunta_matched"]:
                    tema_actual = item["tema"]
                    break
            
            # Verificar tema
            tema_correcto = (tema_actual == tema_esperado) if tema_esperado else True
            
            # Resultado del test
            if contiene_todos and tema_correcto and puntaje >= 60:
                status = "✅ PASS"
                tests_pasados += 1
            else:
                status = "❌ FAIL"
                
            print(f"  {entrada:<25} -> {status} ({puntaje}%)")
            
            if status == "❌ FAIL":
                if not contiene_todos:
                    print(f"    ⚠️  Falta contenido: {debe_contener}")
                if not tema_correcto:
                    print(f"    ⚠️  Tema incorrecto: esperado '{tema_esperado}', actual '{tema_actual}'")
                if puntaje < 60:
                    print(f"    ⚠️  Puntaje bajo: {puntaje}%")
    
    print(f"\n📊 RESULTADO FINAL: {tests_pasados}/{total_tests} tests pasados ({tests_pasados/total_tests*100:.1f}%)")
    
    return tests_pasados, total_tests

def test_edge_cases():
    """Testa casos extremos"""
    print("\n🔬 TESTS DE CASOS EXTREMOS")
    print("=" * 40)
    
    casos_extremos = [
        "",                    # Vacío
        "   ",                 # Solo espacios
        "asdfghjklñ",         # Gibberish
        "1234567890",         # Solo números
        "¿¿¿???!!!",          # Solo símbolos
        "a" * 500,            # Muy largo
        "HOLA GRITANDO TODO",  # Todo mayúsculas
        "pregunta muy específica sobre algo que no existe en la base de datos"
    ]
    
    for caso in casos_extremos:
        resultado = simular_chatbot(caso)
        entrada_mostrar = caso[:30] + "..." if len(caso) > 30 else caso
        entrada_mostrar = entrada_mostrar if entrada_mostrar.strip() else "[VACÍO]"
        
        # Debe devolver fallback
        es_fallback = resultado["puntaje"] < 60
        status = "✅ OK" if es_fallback else "❌ PROBLEMA"
        
        print(f"  {entrada_mostrar:<35} -> {status} ({resultado['puntaje']}%)")

def analizar_cobertura():
    """Analiza la cobertura de temas"""
    print("\n📈 ANÁLISIS DE COBERTURA")
    print("=" * 40)
    
    temas = {}
    for item in base_preguntas:
        tema = item["tema"]
        if tema not in temas:
            temas[tema] = 0
        temas[tema] += 1
    
    print("Preguntas por tema:")
    for tema, cantidad in sorted(temas.items()):
        print(f"  {tema:<15}: {cantidad} preguntas")
    
    print(f"\nTotal: {len(base_preguntas)} preguntas en {len(temas)} temas")

def main():
    print("🧪 SISTEMA DE VALIDACIÓN AVANZADO")
    print("=" * 60)
    
    # Tests de validación específicos
    tests_pasados, total_tests = ejecutar_tests_validacion()
    
    # Tests de casos extremos
    test_edge_cases()
    
    # Análisis de cobertura
    analizar_cobertura()
    
    # Recomendaciones finales
    print("\n💡 RECOMENDACIONES:")
    if tests_pasados / total_tests >= 0.9:
        print("🟢 Excelente! El chatbot responde correctamente.")
    elif tests_pasados / total_tests >= 0.7:
        print("🟡 Bueno, pero revisa los tests fallidos.")
    else:
        print("🔴 Necesita mejoras importantes.")
    
    print("\n🎯 Para probar manualmente:")
    print("1. Ejecuta: python app.py")
    print("2. Abre: test_interface.html en tu navegador")

if __name__ == "__main__":
    main()
