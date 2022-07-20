import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Starting database
data = pd.read_csv('dataset_streamlit.csv')

#App Title
st.title('O Guru das Chuvas')

# Selecting Month, year and Region
month_option = data['mes'].unique().tolist()
year_option = data['ano'].unique().tolist()
bacia_option = data['regiao_hidro'].unique().tolist()

# Starting Select boxes
month = st.selectbox("Selecione o mês: ", month_option, 0)
year = st.selectbox("Selecione o ano: ", year_option, 0)
bacia = st.selectbox("Selecione a sua Bacia Hidrográfica: ", bacia_option, 0)

# Filtering df according to selections
mask = (data['mes'] == month) & (data['ano'] == year) & (data['regiao_hidro'] == bacia )
df = data[mask]

# Preparing df to bar plot
grupo_barras = df.groupby(['mes','regiao_hidro'])[['prev_1_mes','prev_2_meses','prev_3_meses']].mean()
df3 = pd.DataFrame(grupo_barras).reset_index()
df_1 = df3[['mes','regiao_hidro','prev_1_mes']]
df_1.rename(columns = {'prev_1_mes':'Precipitação'}, inplace = True)
df_2 = df3[['mes','regiao_hidro','prev_2_meses']]
df_2.rename(columns = {'prev_2_meses':'Precipitação'},inplace = True)
df_3 = df3[['mes','regiao_hidro','prev_3_meses']]
df_3.rename(columns = {'prev_3_meses':'Precipitação'}, inplace = True)
df3 = pd.concat([df_1,df_2, df_3], axis=0).reset_index()
df3['mes'] = df3.index + 2

df3.rename(columns={'mes':'Mês'}, inplace = True)
# Ploting bar plot
fig = px.bar(df3, x='Mês', y='Precipitação')
st.plotly_chart(fig)

# Explaining bar plot
st.markdown(f"Para o mês de {month} de {year}, na Região Hidrográfica da {bacia}, teremos uma previsão média de precipitação de {round(df3['Precipitação'].values[0],2)} mm, {round(df3['Precipitação'].values[1],2)} mm e {round(df3['Precipitação'].values[2],2)} mm, para os próximos 3 meses, respectivamente.")


# Preparing dataframe to line plot
mask2 = (data['regiao_hidro'] == bacia ) & (data['mes'] == month)
data2= data[mask2]
df2 = data2.groupby(['mes','regiao_hidro', 'ano'])[['Real','prev_1_mes','prev_2_meses','prev_3_meses']].mean()
df2 = pd.DataFrame(df2).reset_index()
df2.rename(columns={'ano':'Ano','Real':'Precipitação histórica','prev_1_mes':'Previsão de Precipitação para 1 mês','prev_2_meses': 'Previsão de Precipitação para 2 meses', 'prev_3_meses':'Previsão de Precipitação para 3 meses'}, inplace = True)

# Ploting line plot
fig2 = px.line(df2, x= 'Ano', y=['Precipitação histórica','Previsão de Precipitação para 1 mês','Previsão de Precipitação para 2 meses','Previsão de Precipitação para 3 meses'])
st.plotly_chart(fig2)

st.markdown(f"Para o mês selecionado ({month}), podemos verificar através da linha azul a sua precipitação histórica média. As outras linhas representam as previsões de precipitação para os três próximos meses, durante os anos de 2011 a 2021.")




