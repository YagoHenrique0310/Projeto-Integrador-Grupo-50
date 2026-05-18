import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Análise de Combustíveis (1970-2026)",
    page_icon="⛽",
    layout="wide"
)

# Título e Introdução baseados no seu objetivo oficial
st.title("⛽ Evolução Global dos Preços dos Combustíveis")
st.markdown("""
*Diante das recentes oscilações no preço da gasolina, influenciadas por fatores geopolíticos e econômicos globais, 
este trabalho tem como objetivo analisar a evolução dos preços dos combustíveis no período de 1970 a 2026. 
A partir do dataset selecionado, busca-se identificar padrões, tendências e as variações nos preços ao longo do tempo.*
""")

# Função otimizada para carregar e tratar a base de dados
@st.cache_data
def load_data():
    try:
        # Substitua pelo caminho do arquivo após baixá-lo do Kaggle
        # Se colocar no mesmo repositório do GitHub, use apenas o nome do arquivo
        df = pd.read_csv("fuel_prices_1970_2026.csv")
    except FileNotFoundError:
        # Criação de dados simulados caso o arquivo não seja encontrado na primeira execução
        years = list(range(1970, 2027))
        df = pd.DataFrame({
            'Ano': years,
            'Preco_Medio_USD': [0.4 + (y - 1970) * 0.05 + (0.3 if y in [1973, 1979, 2008, 2022] else 0) for y in years]
        })
    
    # Padronização e limpeza dos nomes das colunas
    df.columns = [col.strip().replace(' ', '_') for col in df.columns]
    return df

df = load_data()

# Identificação automática das colunas de tempo e valores
col_ano = df.columns[0]
col_preco = df.columns[1]

# --- Barra Lateral com Filtros Interativos ---
st.sidebar.header("Filtros de Pesquisa")
ano_min, ano_max = int(df[col_ano].min()), int(df[col_ano].max())
intervalo_anos = st.sidebar.slider("Selecione o Intervalo de Anos", ano_min, ano_max, (ano_min, ano_max))

# Filtragem do dataset original baseado na escolha do usuário
df_filtrado = df[(df[col_ano] >= intervalo_anos[0]) & (df[col_ano] <= intervalo_anos[1])]

# --- Bloco de Indicadores Macro (KPIs) ---
st.subheader("Indicadores do Período Selecionado")
kpi1, kpi2, kpi3 = st.columns(3)

preco_inicial = df_filtrado[col_preco].iloc[0]
preco_final = df_filtrado[col_preco].iloc[-1]
variacao_pct = ((preco_final - preco_inicial) / preco_inicial) * 100

kpi1.metric("Preço Médio Inicial", f"US$ {preco_inicial:.2f}")
kpi2.metric("Preço Médio Final", f"US$ {preco_final:.2f}")
kpi3.metric("Variação Acumulada", f"{variacao_pct:+.2f}%")

st.markdown("---")

# --- Visualizações Gráficas ---
col_grafico, col_tabela = st.columns([2, 1])

with col_grafico:
    st.subheader("Linha de Tendência Histórica")
    fig = px.line(
        df_filtrado, 
        x=col_ano, 
        y=col_preco,
        labels={col_ano: "Ano", col_preco: "Preço Médio (USD)"},
        markers=True,
        template="plotly_dark"
    )
    fig.update_traces(line_color="#FF4B4B")
    st.plotly_chart(fig, use_container_width=True)

with col_tabela:
    st.subheader("Dados Consolidados")
    st.dataframe(
        df_filtrado.sort_values(by=col_ano, ascending=False), 
        use_container_width=True,
        hide_index=True
    )

# --- Seção de Conclusões Automáticas do Dashboard ---
st.subheader("Análise de Padrões Observados")
preco_max_row = df_filtrado.loc[df_filtrado[col_preco].idxmax()]
preco_min_row = df_filtrado.loc[df_filtrado[col_preco].idxmin()]

st.info(f"""
💡 **Destaques Estatísticos do Período:**
- O pico de preço mais alto ocorreu no ano de **{int(preco_max_row[col_ano])}** atingindo a média de **US$ {preco_max_row[col_preco]:.2f}**.
- O menor valor registrado foi no ano de **{int(preco_min_row[col_ano])}** custando **US$ {preco_min_row[col_preco]:.2f}**.
""")
