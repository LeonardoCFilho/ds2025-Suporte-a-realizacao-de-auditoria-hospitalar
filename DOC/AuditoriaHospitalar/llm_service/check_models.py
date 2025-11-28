import google.generativeai as genai
import os
from dotenv import load_dotenv
import sys

# Carrega a API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("=" * 50)
print(f"DIAGNÓSTICO GEMINI")
print("=" * 50)

# 1. Checar versão da biblioteca
try:
    print(f"1. Versão da biblioteca 'google-generativeai': {genai.__version__}")
except AttributeError:
    print("1. Versão: <Desconhecida/Muito Antiga>")

# 2. Testar Listagem de Modelos
print("\n2. Testando conexão e listando modelos disponíveis...")

if not api_key:
    print("ERRO: API Key não encontrada no arquivo .env")
else:
    try:
        genai.configure(api_key=api_key)

        encontrou_algum = False
        for m in genai.list_models():
            # Filtra apenas modelos que geram texto
            if "generateContent" in m.supported_generation_methods:
                print(f"   - {m.name}")
                encontrou_algum = True

        if not encontrou_algum:
            print(
                "   NENHUM modelo de texto encontrado. Verifique se sua API Key é do Google AI Studio."
            )

    except Exception as e:
        print(f"   ERRO CRÍTICO ao listar modelos: {e}")

print("=" * 50)
