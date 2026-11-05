# Importação das bibliotecas
from pathlib import Path
import pandas as pd

# Diretório dos resultados do RGI
diretorio = Path("../out_rgi")

# Localizar arquivos TXT nas pastas pc*
arquivos = sorted(diretorio.glob("pc*/*.txt"))

resultados = []
arquivos_vazios = 0

for arquivo in arquivos:

    # Extrair PC e replicon do nome da pasta
    identificador = arquivo.parent.name
    pc, replicon = identificador.split("__", 1)

    # Identificar chromosome ou plasmídeo
    if replicon.lower() == "chromosome":
        plasmid_code = "-"
    else:
        plasmid_code = replicon

    # Importar tabela
    df = pd.read_csv(arquivo, sep="\t")

    # Verificar se existem resultados de resistência
    if "ORF_ID" not in df.columns:
        arquivos_vazios += 1
        continue

    df = df.dropna(subset=["ORF_ID"])

    if df.empty:
        arquivos_vazios += 1
        continue

    # Adicionar colunas
    df["pc"] = pc
    df["replicon"] = replicon
    df["plasmid_code"] = plasmid_code

    resultados.append(df)

# Mesclar resultados
if resultados:
    tabela_final = pd.concat(resultados, ignore_index=True)

    # Salvar tabela final
    tabela_final.to_csv(
        diretorio / "rgi_mesclado.tsv",
        sep="\t",
        index=False
    )
