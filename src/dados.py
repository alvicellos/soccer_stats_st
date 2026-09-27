import streamlit as st
from statsbombpy import sb

@st.cache_data
def carregar_competicoes():
    competicoes = sb.competitions()
    return competicoes

@st.cache_data
def carregar_partidas(id_competicao, id_temporada):
    partidas = sb.matches(
        competition_id=id_competicao,
        season_id=id_temporada        )
    return partidas
@st.cache_data
def carregar_eventos(id_partida):
    eventos_partida = sb.events(match_id=id_partida)
    return eventos_partida