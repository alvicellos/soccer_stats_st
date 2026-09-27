import streamlit as st

from src.dados import (
    carregar_competicoes,
    carregar_partidas,
    carregar_eventos
)

from src.tratamento import (
    filtrar_passes,
    filtrar_chutes,
    preparar_passes,
    preparar_chutes
)

from src.visualizacoes import (
    criar_mapa_chutes,
    criar_mapa_passes,
    criar_grafico_eventos
)


st.set_page_config(
    page_title="Estatísticas de Futebol com 'statsbombpy' e 'mplsoccer'",
    page_icon="⚽",
    #layout="wide"
)

st.title("⚽ Estatísticas de Futebol")

# =========================================================
# 2. SELEÇÃO DE COMPETIÇÃO E TEMPORADA
# =========================================================

with st.spinner("Carregando competições da partida..."):
    competicoes = carregar_competicoes()
        
nomes_competicoes =  competicoes['competition_name'].unique()

competicao_selecionada = st.sidebar.selectbox("Competição", nomes_competicoes)

temporadas_disponiveis = competicoes[competicoes['competition_name'] == competicao_selecionada]['season_name'].unique()

temporada_selecionada = st.sidebar.selectbox("Temporada", temporadas_disponiveis)

selecao = competicoes[
    (competicoes['competition_name'] == competicao_selecionada) &
    (competicoes['season_name'] == temporada_selecionada)
]

id_competicao = selecao.iloc[0]['competition_id']
id_temporada = selecao.iloc[0]['season_id']

partidas = carregar_partidas(
    id_competicao,
    id_temporada
)

# =========================================================
# 3. SELEÇÃO DA PARTIDA
# =========================================================

partidas['rotulo'] = partidas.apply(
    lambda linha:
        f"{linha['home_team']} "
        f"{linha['home_score']} x " 
        f"{linha['away_score']} "
        f"{linha['away_team']}",
    axis=1
)

partida_selecionada = st.sidebar.selectbox(
    "Partida",
    partidas['rotulo']
)

id_partida = partidas[partidas['rotulo'] == partida_selecionada].iloc[0]['match_id']

# =========================================================
# 4. CARREGAMENTO E TRATAMENTO DOS EVENTOS
# =========================================================

with st.spinner("Carregando eventos da partida..."):
    eventos = carregar_eventos(id_partida)

passes = filtrar_passes(eventos)
passes = preparar_passes(passes)

chutes = filtrar_chutes(eventos)
chutes = preparar_chutes(chutes)

# =========================================================
# 5. SELEÇÃO DO JOGADOR
# =========================================================

jogadores = passes['player'].dropna().unique()
jogadores_ordenado = sorted(jogadores)
jogador_selecionado = st.sidebar.selectbox(
    "Jogador",
    jogadores_ordenado
)

# =========================================================
# 6. CÁLCULO DAS ESTATÍSTICAS DO JOGADOR
# =========================================================

passes_jogador = passes[passes['player'] == jogador_selecionado]
total_passes = len(passes_jogador)

passes_completos = len(passes_jogador[passes_jogador['pass_outcome'].isna()])
passes_incompletos = len(passes_jogador[passes_jogador['pass_outcome'].notna()])

# =========================================================
# 7. CÁLCULO DAS ESTATÍSTICAS DOS TIMES
# =========================================================

partida = partidas[partidas['match_id'] == id_partida].iloc[0]

home_team = partida['home_team']
away_team = partida['away_team']

# Home team
chutes_home = chutes[chutes['team'] == home_team]
chute_counts_home = chutes_home['shot_outcome'].value_counts()
total_chutes_home = chute_counts_home.sum()
total_gols_home = chute_counts_home.get('Goal', 0)
taxa_conversao_home = total_gols_home / total_chutes_home  if total_chutes_home > 0 else 0

# Time visitante
chutes_away = chutes[chutes['team'] == away_team]
chute_counts_away = chutes_away['shot_outcome'].value_counts()
total_chutes_away = chute_counts_away.sum()
total_gols_away = chute_counts_away.get('Goal', 0)
taxa_conversao_away = total_gols_away / total_chutes_away if total_chutes_away > 0 else 0

# =========================================================
# 8. CRIAÇÃO DAS FIGURAS
# =========================================================

fig_chutes = criar_mapa_chutes(chutes)

fig_passes = criar_mapa_passes(
    passes,
    jogador_selecionado
)

fig_eventos = criar_grafico_eventos(eventos)

# =========================================================
# 9. INTERFACE PRINCIPAL
# =========================================================

with st.container(border=True):

    st.subheader(partida_selecionada)

    st.write(
        f"Competição: {competicao_selecionada} | "
        f"Temporada: {temporada_selecionada}"
    )

tab_chutes, tab_passes, tab_estatisticas, tab_eventos = st.tabs(
    ["⚽ Chutes", "🎯 Passes", "📊 Estatísticas", "📋 Eventos filtrados"]
)

with tab_chutes:
    st.pyplot(fig_chutes)

with tab_passes:
    st.markdown(f"## Jogador: {jogador_selecionado}")
    st.pyplot(fig_passes)

with tab_estatisticas:    
    # Time da casa
    st.subheader(home_team)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Gols",
            value=total_gols_home
        )        
    with col2:
        st.metric(
            label="Chutes",
            value=total_chutes_home)
    with col3:
        st.metric(
            label="Conversão",
            value=f"{float(taxa_conversao_home):.2f}"
        )

    # Time visitante
    st.subheader(away_team)
    
    col1_vis, col2_vis, col3_vis = st.columns(3)

    with col1_vis:
        st.metric(
            label="Gols",
            value=total_gols_away
        )
        
    with col2_vis:
        st.metric(
            label="Chutes",
            value=total_chutes_away)

    with col3_vis:
        st.metric(
            label="Conversão",
            value=f"{float(taxa_conversao_away):.2f}"
        )
        
        # Estatísticas do jogador
        
    st.divider()

    st.subheader(jogador_selecionado)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total de passes",
            value=total_passes
        )

    with col2:
        st.metric(
            label="Passes completos",
            value=passes_completos
        )

    with col3:
        st.metric(
            label="Passes incompletos",
            value=passes_incompletos
        )
    
    st.divider()
    
    st.subheader("Comparador de jogadores")
    with st.form("form_comparacao"):

        jogador_1 = st.selectbox(
            "Jogador 1",
            jogadores
        )

        jogador_2 = st.selectbox(
            "Jogador 2",
            jogadores,
            index=1
        )

        comparar = st.form_submit_button("Comparar jogadores")
        
    if comparar:
        passes_jogador_1 = passes[
            passes["player"] == jogador_1
        ]

        passes_jogador_2 = passes[
            passes["player"] == jogador_2
        ]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                f"{jogador_1} - nº de passes",
                len(passes_jogador_1),
            )

        with col2:
            st.metric(
                f"{jogador_2} - nº de passes",
                len(passes_jogador_2)
            )

st.divider()
st.subheader("Todos os Eventos da partida")        
st.dataframe(eventos)

st.subheader("Eventos mais frequentes da partida")
st.pyplot(fig_eventos)

slider_min = int(eventos['minute'].min())
slider_max = int(eventos['minute'].max())

## session_state filtro formulário

if "intervalo_aplicado" not in st.session_state:
    st.session_state["intervalo_aplicado"] = (
        slider_min,
        slider_max
    )
    
if "quantidade_aplicada" not in st.session_state:
    st.session_state["quantidade_aplicada"] = 20
    
intervalo_salvo = st.session_state["intervalo_aplicado"]

if (
    intervalo_salvo[0] < slider_min or
    intervalo_salvo[1] > slider_max
):
    st.session_state["intervalo_aplicado"] = (
        slider_min,
        slider_max
    )

with st.sidebar.form("form_eventos"):
    st.write("Filtro de eventos")
    intervalo_minutos = st.slider(
        label="Intervalo de minutos",
        min_value=slider_min,
        max_value=slider_max,
        value=st.session_state["intervalo_aplicado"]
    )

    quantidade_eventos = st.number_input(
        label="Quantidade de eventos",
        min_value=1,
        value=st.session_state["quantidade_aplicada"],
        max_value=50,
        step=1
    )
    
    aplicar_filtros = st.form_submit_button(
        "Aplicar filtros"
    )
    
    if aplicar_filtros:
        st.session_state["intervalo_aplicado"] = intervalo_minutos
        st.session_state["quantidade_aplicada"] = quantidade_eventos

intervalo_aplicado = st.session_state["intervalo_aplicado"]
quantidade_aplicada = st.session_state["quantidade_aplicada"]

eventos_filtrados = eventos[
    (eventos['minute'] >= intervalo_aplicado[0]) &
    (eventos['minute'] <= intervalo_aplicado[1])
]

with tab_eventos:
    
    st.subheader("Eventos selecionados da partida")
    st.write(f"Intervalo selecionado: {intervalo_aplicado[0]} - {intervalo_aplicado[1]}")
        
    st.dataframe(
        eventos_filtrados.head(quantidade_aplicada),
        use_container_width=True
    )

    csv = eventos_filtrados.to_csv(
    index=False
    ).encode("utf-8")
    
    st.download_button(
    label="Baixar eventos filtrados",
    data=csv,
    file_name="eventos_filtrados.csv",
    mime="text/csv"
    )
