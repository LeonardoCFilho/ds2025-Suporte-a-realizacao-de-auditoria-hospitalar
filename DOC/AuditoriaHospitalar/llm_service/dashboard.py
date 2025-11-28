import streamlit as st
import pandas as pd
import os
import time
from dotenv import load_dotenv
from pathlib import Path
from src.batch_processor import BatchProcessor

# Configuração da Página
st.set_page_config(page_title="Auditoria Hospitalar IA", page_icon="🏥", layout="wide")

# Título e Cabeçalho
st.title("🏥 Sistema de Suporte à Auditoria Hospitalar")
st.markdown("---")

# Sidebar com Configurações
with st.sidebar:
    st.header("Configurações")

    # Carregar API Key
    load_dotenv()
    api_key_env = os.getenv("GEMINI_API_KEY")

    # Status da API
    if api_key_env:
        st.success("✅ API Key Encontrada (.env)")
        api_key = api_key_env
    else:
        st.error("❌ API Key não encontrada")
        api_key = st.text_input("Insira sua Gemini API Key", type="password")

    st.markdown("---")
    qtd_analise = st.slider("Quantidade de internações para analisar", 1, 50, 5)

    modo_debug = st.checkbox("Modo Debug (Logs)")


# Função de Cache para não recarregar o dataset toda hora
@st.cache_data
def carregar_dados():
    caminho = Path("./data/dataset_internacoes.csv")
    if not caminho.exists():
        return None
    return pd.read_csv(caminho)


# Área Principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📁 Dataset de Internações")
    df = carregar_dados()

    if df is not None:
        st.dataframe(df.head(), use_container_width=True)
        st.caption(f"Total de registros disponíveis: {len(df)}")
    else:
        st.warning("Arquivo 'data/dataset_internacoes.csv' não encontrado.")

with col2:
    st.subheader("⚙️ Ação")
    if st.button(
        "🚀 Iniciar Auditoria com IA", type="primary", use_container_width=True
    ):
        if not api_key:
            st.error("Configure a API Key primeiro!")
        elif df is None:
            st.error("Sem dados para processar.")
        else:
            # Processamento
            try:
                processor = BatchProcessor(api_key)

                with st.status("Processando internações...", expanded=True) as status:
                    st.write("🧠 Inicializando Gemini...")
                    # Simula delay visual ou pega logs reais se adaptar a classe
                    time.sleep(1)

                    st.write(f"📂 Carregando lote de {qtd_analise} registros...")

                    # Chama sua classe existente
                    resultados = processor.analisar_lote(df, limite=qtd_analise)

                    status.update(
                        label="Análise Concluída!", state="complete", expanded=False
                    )

                # Salvar no session state para não perder ao recarregar
                st.session_state["resultados"] = resultados
                st.rerun()

            except Exception as e:
                st.error(f"Erro durante execução: {e}")

# Exibir Resultados (se existirem na sessão)
if "resultados" in st.session_state:
    st.markdown("---")
    st.header("📊 Resultados da Análise")

    res = st.session_state["resultados"]

    # Métricas
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Analisado", len(res))

    prioridade_alta = len(res[res["prioridade_gemini"] == "ALTA"])
    m2.metric("Alta Prioridade", prioridade_alta, delta_color="inverse")

    confianca_media = res["confianca_gemini"].mean()
    m3.metric("Confiança Média IA", f"{confianca_media:.2f}")

    concordancia = len(res[res["nivel_prontidao_kb"] == res["prioridade_gemini"]])
    taxa = (concordancia / len(res)) * 100 if len(res) > 0 else 0
    m4.metric("Concordância (IA x Protocolo)", f"{taxa:.1f}%")

    # Tabela detalhada
    st.subheader("Detalhamento dos Casos")

    # Filtros
    filtro_prioridade = st.multiselect(
        "Filtrar por Prioridade",
        options=["ALTA", "MEDIA", "BAIXA", "MANTER"],
        default=["ALTA", "MEDIA"],
    )

    if filtro_prioridade:
        df_display = res[res["prioridade_gemini"].isin(filtro_prioridade)]
    else:
        df_display = res

    # Exibição colorida baseada na prioridade
    def color_priority(val):
        color = "red" if val == "ALTA" else "orange" if val == "MEDIA" else "green"
        return f"color: {color}; font-weight: bold"

    st.dataframe(
        df_display[
            [
                "paciente_nome",
                "patologia",
                "tempo_permanencia",
                "prioridade_gemini",
                "razoes_alta_gemini",
                "confianca_gemini",
            ]
        ].style.applymap(color_priority, subset=["prioridade_gemini"]),
        use_container_width=True,
        height=400,
    )

    # Download
    csv = res.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Baixar Relatório Completo (CSV)",
        data=csv,
        file_name="resultado_auditoria.csv",
        mime="text/csv",
    )
