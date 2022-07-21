import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
from time import sleep


def get_month(n):
    return n-12 if n > 12 else n

# Starting database
# data = pd.read_csv('dataset_streamlit.csv')
df_names = [f"data/pr_mais_{i}_mun.csv" for i in [1, 2, 3]]
dfs = []
for i, df_name in enumerate(df_names):
    dfs.append((
        pd
        .read_csv(df_name)
        .rename(columns={'Unnamed: 0': 'datetime'})
    ))
    dfs[i] = dfs[i].assign(
        ano = dfs[i].datetime.apply(lambda x: x[:4]),
        mes = dfs[i].datetime.apply(lambda x: x[5:7])
    )

#App Title
st.title('O Guru das Chuvas')

# Selecting Month, year and Region
month_option = [
    'Janeiro',
    'Fevereiro',
    'Março',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro',
]

year_option = dfs[0]['ano'].unique().tolist()
bacia_option = dfs[0].columns.tolist()
bacia_option.remove('datetime')
bacia_option.remove('mes')
bacia_option.remove('ano')

with st.expander("Mais informações"):
    st.markdown("""
    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
    when an unknown printer took a galley of type and scrambled it to make a type
    specimen book. It has survived not only five centuries, but also the leap into
    electronic typesetting, remaining essentially unchanged. It was popularised
    in the 1960s with the release of Letraset sheets containing Lorem Ipsum
    passages, and more recently with desktop publishing software like Aldus
    PageMaker including versions of Lorem Ipsum.
    """)
# Starting Select boxes
col1, col2, col3 = st.columns(3)
# st.write(month_option, datetime.now().month-1)
month = col1.selectbox(
    "Mês",
    month_option,
    datetime.now().month-1
)
year = col2.selectbox(
    "Ano",
    year_option,
    year_option.index(year_option[-1])
)
municipio = col3.selectbox(
    "Município",
    bacia_option
)



# Ploting bar plot


btn = st.button("Pergunte ao guru!")

if btn:
    with st.spinner("Um momento, estou mentalizando..."):
        sleep(3)
        month_index = f"{month_option.index(month) + 1:02d}"
        precipitacoes = []
        for df in dfs:
            precipitacoes.append(
                df.query("mes == @month_index and ano == @year")[[municipio]].values.tolist()
            )
        if precipitacoes[0]:
            precipitacoes = sum(sum(precipitacoes, []), [])
            precipitacoes = [int(max([0, pre])) for pre in precipitacoes]
            
            meses = [month_option[get_month(month_option.index(month)+i+1)-1] for i in [1, 2, 3]]
            df3 = pd.DataFrame({
                'Precipitação (mm)': precipitacoes,
                'Mês': meses
            })

            fig = px.bar(df3, x='Mês', y='Precipitação (mm)')

            # Explaining bar plot
            st.info(
                f"""Para o mês de {month} de {year}, no município de {municipio.capitalize()},
                teremos uma previsão média de precipitação de {precipitacoes[0]} mm, {precipitacoes[1]} mm e {precipitacoes[2]} mm,
                para os próximos 3 meses, respectivamente."""
            )
            st.plotly_chart(fig)
        else:
            st.error("Desculpe, mas não posso realizar predições para os valores selecionados.")

