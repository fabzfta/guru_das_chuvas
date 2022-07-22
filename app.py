import streamlit as st
from streamlit_option_menu import option_menu
from apps import guru, sobre, comparative, exploratory

with st.sidebar:
    selected = option_menu(
        "Storm Tellers",
        ["Guru das chuvas", 'Análise exploratória', 'Análise comparativa', 'Sobre'],
        icons=["umbrella", "graph-up", "robot", "people-fill"],
        menu_icon=["megaphone"],
        default_index=0
    )

if selected == "Guru das chuvas":
    guru.main()

if selected == "Sobre":
    sobre.main()


if selected == 'Análise exploratória':
    exploratory.main()

if selected == "Análise comparativa":
    comparative.main()
