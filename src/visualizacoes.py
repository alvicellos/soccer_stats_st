from mplsoccer import Pitch
import matplotlib.pyplot as plt
import seaborn as sns

def criar_mapa_chutes(chutes):
    chutes = chutes.copy()    
    gols = chutes[chutes['shot_outcome'] == 'Goal']
    no_gols = chutes[chutes['shot_outcome'] != 'Goal']    
    pitch = Pitch(pitch_type="statsbomb")
    fig, ax = pitch.draw()

    pitch.scatter(
        gols['x'],
        gols['y'],
        ax=ax,
        marker="*",
        s=150,
        label="Gol"
    )
    
    pitch.scatter(
    no_gols['x'],
    no_gols['y'],
    ax=ax,
    marker="o",
    label="Não foi gol"
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