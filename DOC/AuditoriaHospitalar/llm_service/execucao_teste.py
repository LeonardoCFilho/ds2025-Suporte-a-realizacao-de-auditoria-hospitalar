"""
Teste SIMPLES do Gemini com dataset - sem imports complexos
"""
import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def teste_simples():
    print("TESTE SIMPLES - Gemini + Dataset")
    print("=" * 50)
    
    # Verificar API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("GEMINI_API_KEY não encontrada")
        return
    
    print("Gemini configurado")
    
    # Carregar dataset
    try:
        PASTA_DATASET = Path("./data")
        ARQUIVO_DATASET = PASTA_DATASET / "dataset_internacoes.csv"
        df = pd.read_csv(ARQUIVO_DATASET)
        print(f"Dataset carregado: {len(df)} registros")
        
        # Mostrar primeiras linhas
        print("\nPRIMEIRAS LINHAS DO DATASET:")
        print(df[['paciente_nome', 'patologia', 'tempo_permanencia', 'idade']].head(5))
        
        # Testar com apenas 1 caso
        print(f"\n\tTESTANDO")
        
        # Importar só o necessário
        import sys
        sys.path.append('.')
        
        from src.services import LLMService
        
        service = LLMService(api_key)
        
        # Pegar primeiro caso
        primeiro_caso = df.iloc[0] #df.loc[1]
        dados_internacao = {
            'patologia': primeiro_caso['patologia'],
            'tempo_permanencia': int(primeiro_caso['tempo_permanencia']),
            'setor': primeiro_caso['setor'],
            'idade': int(primeiro_caso['idade']),
            'comorbidades': eval(primeiro_caso['comorbidades']) if isinstance(primeiro_caso['comorbidades'], str) else primeiro_caso['comorbidades'],
            'tempo_ideal_patologia': int(primeiro_caso['tempo_ideal_patologia']),
            'paciente_id': primeiro_caso['paciente_id'],
            'internacao_id': primeiro_caso['internacao_id']
        }
        
        print(f"Analisando: {primeiro_caso['paciente_nome']} - {primeiro_caso['patologia']}")
        
        resultado = service.analisar_paciente_alta(dados_internacao)
        
        print("\n\tRESULTADO:")
        print(f"Prioridade: {resultado['prioridade']}")
        print(f"Confiança: {resultado['confianca']}")
        print(f"Razões: {resultado['razoes_alta'][:2]}")
        print(f"Pendências: {resultado['pendencias'][:2]}\n")
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    teste_simples()