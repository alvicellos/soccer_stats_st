from statsbombpy import sb
from pathlib import Path

pasta = Path("data")
pasta.mkdir(exist_ok=True)

# Todas as competições disponíveis
competicoes = sb.competitions()

competicoes.to_csv(
    pasta / "competicoes.csv",
    index=False
)

print(competicoes[
    ["competition_id", "season_id",
     "competition_name", "season_name"]
].to_string())