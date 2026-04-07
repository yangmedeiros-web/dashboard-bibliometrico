import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(layout="wide", page_title="Plataforma Celso Furtado")

# Cache para carregar os dados rapidamente
@st.cache_data
def carregar_dados():
    return pd.read_excel('banco_autores_assuntos.xlsx')

df = carregar_dados()

# --- NOVO CABEÇALHO ---
st.title("🏛️ Plataforma Celso Furtado")
st.markdown("### Dashboard de Análise Bibliométrica e Cruzamento de Dados")
st.divider()

# Adicionamos uma 5ª aba para a Rede de Conhecimento
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "1. Top Trabalhos por Autor", 
    "2. Top Autores por Trabalho", 
    "3. Trabalhos mais densos por Área", 
    "4. Autores mais citados por Área",
    "5. 🕸️ Rede de Conhecimento (Grafos)"
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
    # Aqui o código lerá automaticamente "Grande Área" se você tiver implementado a taxonomia, 
    # ou "Assunto" se tiver mantido o formato original.
    coluna_area = 'Grande Área' if 'Grande Área' in df.columns else 'Assunto'
    
    lista_areas = sorted(df[coluna_area].dropna().unique())
    area_selecionada_3 = st.selectbox("Selecione a Área de Estudo:", [""] + lista_areas, key="area3")
    
    if area_selecionada_3:
        df_filtrado = df[df[coluna_area] == area_selecionada_3]
        top10_trab_area = df_filtrado['Título do Trabalho'].value_counts().head(10).reset_index()
        top10_trab_area.columns = ['Título do Trabalho', 'Total de Referências Mapeadas']
        st.dataframe(top10_trab_area, use_container_width=True)

with aba4:
    st.subheader("Autores mais citados dentro de uma Área específica")
    area_selecionada_4 = st.selectbox("Selecione a Área de Estudo:", [""] + lista_areas, key="area4")
    
    if area_selecionada_4:
        df_filtrado = df[df[coluna_area] == area_selecionada_4]
        top10_autores_area = df_filtrado['Autor'].value_counts().head(10).reset_index()
        top10_autores_area.columns = ['Autor', 'Qtd. de Citações nesta Área']
        st.dataframe(top10_autores_area, use_container_width=True)

# --- NOVA ABA DE GRAFOS INTERATIVOS ---
with aba5:
    st.subheader("Teia de Autores e Trabalhos")
    st.markdown("Selecione um Trabalho para visualizar visualmente a rede de autores que compõem sua base teórica.")
    
    lista_trabalhos_grafo = sorted(df['Título do Trabalho'].dropna().unique())
    trabalho_rede = st.selectbox("Escolha um Trabalho:", [""] + lista_trabalhos_grafo, key="grafo_trab")
    
    if trabalho_rede:
        df_rede = df[df['Título do Trabalho'] == trabalho_rede]
        
        # Criação do objeto do grafo visual
        net = Network(height='500px', width='100%', bgcolor='#ffffff', font_color='black')
        
        # Cria o nó central (O Trabalho acadêmico) em tamanho maior e cor de destaque (Vermelho)
        net.add_node(trabalho_rede, label="O Trabalho", title=trabalho_rede, color="#FF4B4B", size=35)
        
        # Coleta os autores únicos daquele trabalho
        autores_unicos = df_rede['Autor'].unique()
        
        # Adiciona os autores (bolinhas azuis) e liga eles ao trabalho com uma linha (edge)
        for autor in autores_unicos:
            if str(autor).strip() != "":
                net.add_node(autor, label=autor, title=autor, color="#0068C9", size=15)
                net.add_edge(trabalho_rede, autor)
            
        # Adiciona uma "física" suave para os nós se organizarem de forma orgânica
        net.repulsion(node_distance=150, spring_length=100)
        
        # Salva o grafo em um arquivo HTML temporário e lê para jogar na tela do Streamlit
        try:
            path = "grafo_rede.html"
            net.save_graph(path)
            with open(path, 'r', encoding='utf-8') as f:
                html_data = f.read()
            components.html(html_data, height=515)
        except Exception as e:
            st.error(f"Erro ao gerar a visualização: {e}")
