"""
Força reindexação completa do RAG
"""
import os
from dotenv import load_dotenv
from src.rag import RAGSystem

load_dotenv()

def reindexar_tudo():
    print("REINDEXAÇÃO COMPLETA DO RAG")
    print("=" * 50)
    
    rag = RAGSystem()
    rag.reindexar_conhecimento()
    
    # Verificar resultado
    count = rag.collection.count()
    print(f"\nREINDEXAÇÃO CONCLUÍDA:")
    print(f"   • Documentos indexados: {count}")
    
    # Listar patologias indexadas
    results = rag.collection.get()
    patologias = set()
    for metadata in results['metadatas']:
        if metadata and 'patologia' in metadata:
            patologias.add(metadata['patologia'])
    
    print(f"   • Patologias disponíveis: {sorted(patologias)}")
    print(f"   • Total de patologias: {len(patologias)}")

if __name__ == "__main__":
    reindexar_tudo()