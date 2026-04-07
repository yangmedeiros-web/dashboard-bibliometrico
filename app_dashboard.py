import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Dashboard Bibliométrico")

@st.cache_data
def carregar_dados():
    return pd.read_excel('banco_autores_assuntos.xlsx')

df = carregar_dados()

st.title("📊 Análise Bibliométrica e Cruzamento de Dados")
st.markdown("Explore as relações entre Autores, Trabalhos e Áreas de Estudo.")
st.divider()

aba1, aba2, aba3, aba4 = st.tabs([
    "1. Top Trabalhos por Autor", 
    "2. Top Autores por Trabalho", 
    "3. Trabalhos mais densos por Área", 
    "4. Autores mais citados por Área"
])

with aba1:
    st.subheader("Trabalhos que mais citaram um Autor específico")
    busca_autor = st.text_input("Digite o nome ou sobrenome do Autor (ex: SILVA):", key="busca_autor")
    
    if busca_autor:
        df_filtrado = df[df['Autor'].str.contains(busca_autor, case=False, na=False)]
        if not df_filtrado.empty:
            top10_trab = df_filtrado['Título do Trabalho'].value_counts().head(10).reset_index()
            top10_trab.columns = ['Título do Trabalho', 'Qtd. de Citações a este Autor']
            st.dataframe(top10_trab, use_container_width=True)
        else:
            st.warning("Nenhum autor encontrado com esse nome.")

with aba2:
    st.subheader("Autores mais citados em um Trabalho específico")
    lista_trabalhos = sorted(df['Título do Trabalho'].dropna().unique())
    trabalho_selecionado = st.selectbox("Selecione ou digite o Título do Trabalho:", [""] + lista_trabalhos)
    
    if trabalho_selecionado:
        df_filtrado = df[df['Título do Trabalho'] == trabalho_selecionado]
        top10_autores = df_filtrado['Autor'].value_counts().head(10).reset_index()
        top10_autores.columns = ['Autor', 'Qtd. de Citações no Trabalho']
        st.dataframe(top10_autores, use_container_width=True)

with aba3:
    st.subheader("Trabalhos com maior volume de referências em uma Área")
    lista_areas = sorted(df['Assunto'].dropna().unique())
    area_selecionada_3 = st.selectbox("Selecione a Área de Estudo:", [""] + lista_areas, key="area3")
    
    if area_selecionada_3:
        df_filtrado = df[df['Assunto'] == area_selecionada_3]
        top10_trab_area = df_filtrado['Título do Trabalho'].value_counts().head(10).reset_index()
        top10_trab_area.columns = ['Título do Trabalho', 'Total de Referências Mapeadas']
        st.dataframe(top10_trab_area, use_container_width=True)

with aba4:
    st.subheader("Autores mais citados dentro de uma Área específica")
    area_selecionada_4 = st.selectbox("Selecione a Área de Estudo:", [""] + lista_areas, key="area4")
    
    if area_selecionada_4:
        df_filtrado = df[df['Assunto'] == area_selecionada_4]
        top10_autores_area = df_filtrado['Autor'].value_counts().head(10).reset_index()
        top10_autores_area.columns = ['Autor', 'Qtd. de Citações nesta Área']
        st.dataframe(top10_autores_area, use_container_width=True)