"""
Executor do Batch Processor - CHAMA a classe para rodar
"""
import os
from dotenv import load_dotenv
from batch_processor import BatchProcessor
from pathlib import Path

def main():
    print("INICIANDO PROCESSAMENTO EM LOTE")
    print("=" * 50)
    
    # Carregar configurações
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("ERRO: GEMINI_API_KEY não encontrada no .env")
        return
    
    # 1. Criar o processador
    
    processor = BatchProcessor(api_key)
    
    # 2. Carregar dataset
    try:
        PASTA_DATASET = Path("./data")
        ARQUIVO_DATASET = PASTA_DATASET / "dataset_internacoes.csv"
        df = processor.carregar_dataset(ARQUIVO_DATASET)
    except Exception as e:
        print(f"ERRO ao carregar dataset: {e}")
        return
    
    # 3. Processar (ex: apenas 5 casos para teste)
    print(f"Processando {len(df)} internações...")
    resultados = processor.analisar_lote(df, limite=5)
    
    # 4. Salvar resultados
    processor.salvar_resultados(resultados, 'resultados_analise.csv')
    
    # 5. Gerar relatório
    relatorio = processor.gerar_relatorio_estatistico(resultados)
    
    print("\nRELATORIO FINAL:")
    print(f"   Total processado: {relatorio.get('total_analisado', 0)}")
    print(f"   Confianca media: {relatorio.get('confianca_media', 0)}")
    print(f"   Casos alta prioridade: {relatorio.get('casos_alta_prioridade', 0)}")
    print(f"   Taxa concordancia: {relatorio.get('taxa_concordancia', 0)}%")

if __name__ == "__main__":
    main()