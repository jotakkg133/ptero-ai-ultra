#!/usr/bin/env python3
"""Teste para descobrir qual modelo Gemini funciona"""

import google.generativeai as genai

API_KEY = "AIzaSyDJ6V-x0EP0vGVaJ4n7mGFSOBSy2EDZIRg"
genai.configure(api_key=API_KEY)

print("🔍 Listando modelos disponíveis...\n")

try:
    models = genai.list_models()
    
    print("📋 Modelos que suportam generateContent:\n")
    working_models = []
    
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
            working_models.append(m.name)
    
    print(f"\n🎯 Total: {len(working_models)} modelos disponíveis")
    
    # Testar o primeiro modelo
    if working_models:
        print(f"\n🧪 Testando {working_models[0]}...")
        
        # Extrair nome curto (models/gemini-pro -> gemini-pro)
        model_name = working_models[0].replace('models/', '')
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Responda apenas: OK")
        
        print(f"✅ FUNCIONA! Use: {model_name}")
        print(f"📝 Resposta: {response.text}")
        
except Exception as e:
    print(f"❌ Erro: {e}")
