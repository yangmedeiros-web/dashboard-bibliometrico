import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Plataforma Celso Furtado")

@st.cache_data
def carregar_dados():
    return pd.read_excel('banco_autores_assuntos.xlsx')

df = carregar_dados()

st.title("🏛️ Plataforma Celso Furtado")
st.markdown("### Análise Bibliométrica e Repositório Digital")
st.divider()

aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "1. Trabalhos por Autor", 
    "2. Autores por Trabalho", 
    "3. Densidade por Área", 
    "4. Citações por Área",
    "5. 🕸️ Rede de Conhecimento"
])

# Configuração para as tabelas exibirem links clicáveis
config_link = {
    "Link do Trabalho": st.column_config.LinkColumn("Link Original", display_text="Acessar Documento")
}

with aba1:
    st.subheader("Trabalhos que mais citaram um Autor")
    busca_autor = st.text_input("Digite o nome do Autor:", key="b1")
    if busca_autor:
        df_f = df[df['Autor'].str.contains(busca_autor, case=False, na=False)]
        if not df_f.empty:
            # Agrupamos por Título e Link para manter a relação
            res = df_f.groupby(['Título do Trabalho', 'Link do Trabalho']).size().reset_index(name='Citações')
            res = res.sort_values('Citações', ascending=False).head(10)
            st.dataframe(res, use_container_width=True, column_config=config_link)

with aba2:
    st.subheader("Autores mais citados em um Trabalho")
    lista_t = sorted(df['Título do Trabalho'].dropna().unique())
    selecionado = st.selectbox("Selecione o Trabalho:", [""] + lista_t)
    if selecionado:
        # Mostra o link do trabalho selecionado em destaque
        link_atual = df[df['Título do Trabalho'] == selecionado]['Link do Trabalho'].iloc[0]
        if link_atual:
            st.link_button("🔗 Abrir Trabalho Original no Repositório", link_atual)
            
        df_f = df[df['Título do Trabalho'] == selecionado]
        res = df_f['Autor'].value_counts().head(15).reset_index()
        res.columns = ['Autor', 'Qtd. de Citações']
        st.dataframe(res, use_container_width=True)

with aba3:
    st.subheader("Trabalhos com maior volume de referências")
    col_area = 'Grande Área' if 'Grande Área' in df.columns else 'Assunto'
    area = st.selectbox("Selecione a Área:", [""] + sorted(df[col_area].unique()), key="b3")
    if area:
        df_f = df[df[col_area] == area]
        res = df_f.groupby(['Título do Trabalho', 'Link do Trabalho']).size().reset_index(name='Total de Referências')
        res = res.sort_values('Total de Referências', ascending=False).head(10)
        st.dataframe(res, use_container_width=True, column_config=config_link)

with aba4:
    st.subheader("Autores mais citados por Área")
    area4 = st.selectbox("Selecione a Área:", [""] + sorted(df[col_area].unique()), key="b4")
    if area4:
        df_f = df[df[col_area] == area4]
        res = df_f['Autor'].value_counts().head(10).reset_index()
        st.dataframe(res, use_container_width=True)

with aba5:
    st.subheader("Teia de Autores e Trabalhos")
    trabalho_rede = st.selectbox("Escolha um Trabalho para o Grafo:", [""] + lista_t, key="g1")
    if trabalho_rede:
        link_rede = df[df['Título do Trabalho'] == trabalho_rede]['Link do Trabalho'].iloc[0]
        if link_rede:
            st.info(f"Visualizando rede para: {trabalho_rede}")
            st.link_button("Ir para o PDF original", link_rede)
            
        df_rede = df[df['Título do Trabalho'] == trabalho_rede]
        net = Network(height='500px', width='100%', bgcolor='#ffffff', font_color='black')
        net.add_node(trabalho_rede, label="Trabalho", title=trabalho_rede, color="#FF4B4B", size=30)
        for autor in df_rede['Autor'].unique():
            if str(autor).strip():
                net.add_node(autor, label=autor, title=autor, color="#0068C9", size=15)
                net.add_edge(trabalho_rede, autor)
        net.repulsion(node_distance=150)
        net.save_graph("grafo.html")
        with open("grafo.html", 'r', encoding='utf-8') as f:
            components.html(f.read(), height=520)