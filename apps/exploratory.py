import streamlit as st
from streamlit.components import v1 as components 

def main():
    st.title('ANÁLISE EXPLORATÓRIA')

    plot_file = open('exploratory_data_analysis.html', 'r', encoding='utf-8')
    plot = plot_file.read()
    components.html(plot, width=900, height=700, scrolling=True)
    plot_file.close()



