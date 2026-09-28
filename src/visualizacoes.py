from mplsoccer import Pitch
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd

def criar_mapa_chutes(chutes):
    chutes = chutes.copy()
    chutes['momento'] = pd.to_datetime(chutes['timestamp'], format='%H:%M:%S.%f')
    min_45= datetime(year=1900, month=1, day=1, hour=0, minute=45)
    
    times = chutes['team'].unique()
    time_a = times[0]
    time_b = times[1]
    
    # Chute time A
    chutes_time_a = chutes[chutes['team'] == time_a]
    # Inversão das coordenadas no segundo tempo
    chutes_time_a_2t = chutes_time_a[(chutes_time_a['minute'] > 45) & (chutes_time_a['momento'] < min_45)].index
    
    chutes_time_a.loc[chutes_time_a_2t, 'x'] = 120 - chutes_time_a.loc[chutes_time_a_2t, 'x']
    chutes_time_a.loc[chutes_time_a_2t, 'y'] = 80 - chutes_time_a.loc[chutes_time_a_2t, 'y']
    
    gols_time_a = chutes_time_a[chutes_time_a['shot_outcome'] == 'Goal']
    no_gols_time_a = chutes_time_a[chutes_time_a['shot_outcome'] != 'Goal']
    
    #Chutes time B
    chutes_time_b = chutes[chutes['team'] == time_b]
    # Inversão do lado do campo no primeiro tempo
    chutes_time_b_1t = chutes_time_b[((chutes_time_b['minute'] < 45) & (chutes_time_b['momento'] < min_45)) | ((chutes_time_b['minute'] > 45) & (chutes_time_b['momento'] > min_45))].index
    
    chutes_time_b.loc[chutes_time_b_1t, 'x'] = 120 - chutes_time_b.loc[chutes_time_b_1t, 'x']    
    chutes_time_b.loc[chutes_time_b_1t, 'y'] = 80 - chutes_time_b.loc[chutes_time_b_1t, 'y']

    gols_time_b = chutes_time_b[chutes_time_b['shot_outcome'] == 'Goal']
    no_gols_time_b = chutes_time_b[chutes_time_b['shot_outcome'] != 'Goal']
    
    pitch = Pitch(pitch_type="statsbomb")
    fig, ax = pitch.draw()

    pitch.scatter(
        gols_time_a['x'],
        gols_time_a['y'],
        ax=ax,
        marker="*",
        s=150,
        color = "darkblue",
        label=f"Gol - {time_a}"
    )
    
    pitch.scatter(
        no_gols_time_a['x'],
        no_gols_time_a['y'],
        ax=ax,
        marker="o",
        color = "royalblue",
        label=f"Não foi gol - {time_a}"
    )
    
    pitch.scatter(
        gols_time_b['x'],
        gols_time_b['y'],
        ax=ax,
        marker="*",
        s=150,
        color = "darkgreen",
        label=f"Gol - {time_b}"
        )
        
    pitch.scatter(
        no_gols_time_b['x'],
        no_gols_time_b['y'],
        ax=ax,
        marker="o",
        color = "limegreen",
        label=f"Não foi gol - {time_b}"
        )
        
    ax.legend()
    return fig

def criar_mapa_passes(passes, jogador):
    passes_jogador = passes[passes['player'] == jogador]
    
    passes_completos = passes_jogador[passes_jogador['pass_outcome'].isna()]
    passes_incompletos = passes_jogador[passes_jogador['pass_outcome'].notna()]
    
    pitch = Pitch(pitch_type="statsbomb")
    fig, ax = pitch.draw()

    pitch.arrows(
        passes_completos['x'],  
        passes_completos['y'], 
        passes_completos['end_x'],
        passes_completos['end_y'],
        ax=ax,
        color="green",
        label="Completo"
    )
    
    pitch.arrows(
        passes_incompletos['x'],  
        passes_incompletos['y'], 
        passes_incompletos['end_x'],
        passes_incompletos['end_y'],
        ax=ax,
        color="red",
        label="Incompleto"
        )
    
    ax.set_title("Mapa de passes")
    ax.legend()
    
    return fig

def criar_mapa_passes_tempos(passes, jogador):
    '''Função criada para verificar a necessidade de inverter as coordenadas dos passes como foi feito nas coordenadas dos chutes'''
    passes_jogador = passes[passes['player'] == jogador]
    
    min_45= datetime(year=1900, month=1, day=1, hour=0, minute=45)   
    primeiro_tempo = passes_jogador[(passes_jogador['minute'] > 45) & (passes_jogador['momento'] < min_45)].index
    segundo_tempo = passes_jogador[((passes_jogador['minute'] < 45) & (passes_jogador['momento'] < min_45)) | ((passes_jogador['minute'] > 45) & (passes_jogador['momento'] > min_45))].index
    
    passes_jogador.loc[primeiro_tempo, "tempo"] = "1º tempo"
    passes_jogador.loc[segundo_tempo, "tempo"] = "2º tempo"
    
    pitch = Pitch(pitch_type="statsbomb")
    fig, ax = pitch.draw()

    pitch.arrows(
        passes_jogador['x'],  
        passes_jogador['y'], 
        passes_jogador['end_x'],
        passes_jogador['end_y'],
        ax=ax,
        color="green",
        label="1º tempo"
    )
    
    pitch.arrows(
        passes_jogador['x'],  
        passes_jogador['y'], 
        passes_jogador['end_x'],
        passes_jogador['end_y'],
        ax=ax,
        color="red",
        label="2º tempo"
        )
    
    ax.set_title("Mapa de passes")
    ax.legend()
    
    return fig


def criar_grafico_eventos(eventos):

    contagem = (
        eventos["type"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    contagem.columns = ["evento", "quantidade"]

    fig, ax = plt.subplots()

    sns.barplot(
        data=contagem,
        x="evento",
        y="quantidade",
        ax=ax
    )

    ax.set_title("10 eventos mais frequentes")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()

    return fig