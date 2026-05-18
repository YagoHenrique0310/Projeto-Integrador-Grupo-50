import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análise de Combustíveis (1970-2026)",
    page_icon="⛽",
    layout="wide"
)

st.title("⛽ Evolução Global dos Preços dos Combustíveis")
st.markdown("""
*Diante das recentes oscilações no preço da gasolina, influenciadas por fatores geopolíticos e econômicos globais, 
este trabalho tem como objetivo analisar a evolução dos preços dos combustíveis no período de 1970 a 2026. 
A partir do dataset selecionado, busca-se identificar padrões, tendências e as variações nos preços ao longo do tempo.*
""")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("fuel_prices_1970_2026.csv")
    except FileNotFoundError:
        years = list(range(1970, 2027))
        df = pd.DataFrame({
            'Ano': years,
            'Preco_Medio_USD': [0.4 + (y - 1970) * 0.05 + (0.3 if y in [1973, 1979, 2008, 2022] else 0) for y in years]
        })
    
    df.columns = [col.strip().replace(' ', '_') for col in df.columns]
    return df

df = load_data()

col_ano = df.columns[0]
col_preco = df.columns[1]

st.sidebar.header("Filtros de Pesquisa")
ano_min, ano_max = int(df[col_ano].min()), int(df[col_ano].max())
intervalo_anos = st.sidebar.slider("Selecione o Intervalo de Anos", ano_min, ano_max, (ano_min, ano_max))

df_filtrado = df[(df[col_ano] >= intervalo_anos[0]) & (df[col_ano] <= intervalo_anos[1])]

st.subheader("Indicadores do Período Selecionado")
kpi1, kpi2, kpi3 = st.columns(3)

preco_inicial = df_filtrado[col_preco].iloc[0]
preco_final = df_filtrado[col_preco].iloc[-1]
variacao_pct = ((preco_final - preco_inicial) / preco_inicial) * 100

kpi1.metric("Preço Médio Inicial", f"US$ {preco_inicial:.2f}")
kpi2.metric("Preço Médio Final", f"US$ {preco_final:.2f}")
kpi3.metric("Variação Acumulada", f"{variacao_pct:+.2f}%")

st.markdown("---")

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

st.subheader("Análise de Padrões Observados")
preco_max_row = df_filtrado.loc[df_filtrado[col_preco].idxmax()]
preco_min_row = df_filtrado.loc[df_filtrado[col_preco].idxmin()]

st.info(f"""
💡 **Destaques Estatísticos do Período:**
- O pico de preço mais alto ocorreu no ano de **{int(preco_max_row[col_ano])}** atingindo a média de **US$ {preco_max_row[col_preco]:.2f}**.
- O menor valor registrado foi no ano de **{int(preco_min_row[col_ano])}** custando **US$ {preco_min_row[col_preco]:.2f}**.
""")
