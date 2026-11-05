# Minicurso_EPB
Atividade prática desenvolvida para o minicurso da Escola Paranaense de Bioinformática, abordando a identificação e análise de genes de resistência antimicrobiana em replicons bacterianos utilizando RGI e o banco de dados CARD.


# Identificação de genes de resistência - Atividade prática

Este repositório reúne os comandos e scripts utilizados na identificação de genes de resistência antimicrobiana em replicons bacterianos, utilizando o **RGI (Resistance Gene Identifier)** e o banco de dados **CARD (Comprehensive Antibiotic Resistance Database)**.

## 1. Configuração do ambiente Conda

Verificar se já existe um ambiente chamado `rgi`:

```bash
conda env list
```

Caso não exista, criar o ambiente:

```bash
conda create -n rgi python=3.10 -y
```

Verificar a criação:

```bash
conda env list
```

Ativar o ambiente:

```bash
conda activate rgi
```

Verificar se o RGI já está instalado:

```bash
rgi -h
```

Caso não esteja instalado:

```bash
conda install -c conda-forge -c bioconda rgi -y
```

## 2. Organização dos diretórios

Criar o diretório para a atividade e entrar nele:

```bash
mkdir resistencia
cd resistencia
```

Criar o diretório para o banco de dados CARD:

```bash
mkdir CARD
cd CARD
```

## 3. Download do banco de dados CARD

Realizar o carregamento do banco de dados:

```bash
rgi auto_load
```

Voltar ao diretório `resistencia`:

```bash
cd ..
```

## 4. Download dos replicons

Clonar o repositório da disciplina utilizando `git sparse-checkout`, selecionando somente a pasta `replicons`:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/Rodrigo-Lusa/disciplina_EPB_2026.git
```

Entrar no repositório:

```bash
cd disciplina_EPB_2026
```

Selecionar somente a pasta desejada:

```bash
git sparse-checkout set --no-cone genomas_completos/replicons
```

## 5. Organização dos arquivos

Mover a pasta `replicons` para o diretório da atividade:

```bash
mv genomas_completos/replicons/ ../
```

Voltar ao diretório `resistencia`:

```bash
cd ..
```

Excluir o repositório clonado:

```bash
rm -rf disciplina_EPB_2026
```

Verificar os diretórios:

```bash
ls
```

## 6. Verificação dos recursos computacionais

Verificar a quantidade de núcleos disponíveis no computador:

```bash
nproc
```

## 7. Criação do script para execução do RGI

Criar o diretório para armazenar os scripts:

```bash
mkdir scripts
cd scripts/
```

Criar o arquivo `rgi.sh`:

```bash
nano rgi.sh
```

Inserir o seguinte conteúdo:

```bash
#!/bin/bash

mkdir -p ../out_rgi

for arquivo in ../replicons/*.fasta; do

    nome=$(basename "$arquivo" .fasta)

    mkdir -p "../out_rgi/$nome"

    rgi main \
        -i "$arquivo" \
        -o "../out_rgi/$nome/$nome" \
        -t contig \
        -a DIAMOND \
        -n 4

done
```

### Tornar o script executável

```bash
chmod +x rgi.sh
```

### Executar o script

```bash
./rgi.sh
```

### Verificar os resultados

```bash
ls ../out_rgi/
```

## 8. Mesclagem dos resultados

Criar o arquivo Python responsável por reunir os resultados individuais do RGI:

```bash
nano mesclagem.py
```

Inserir o seguinte código:

```python
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
```

### Executar o script Python

```bash
python mesclagem.py
```

## 9. Visualização dos resultados

Acessar o diretório de resultados:

```bash
cd ../out_rgi/
```

Verificar os arquivos:

```bash
ls
```

Visualizar a tabela mesclada:

```bash
less rgi_mesclado.tsv
```

## 10. Visualização e análise no Google Colab

Acessar o notebook disponibilizado para a atividade:

[Google Colab - Análise dos resultados](https://colab.research.google.com/drive/1Zy-FTPjGIyxqWN72YVJOUVAiMmjQmYcl?usp=sharing)

### Preparação do notebook

1. Acessar **Arquivo → Salvar uma cópia no Drive**.
2. No menu lateral, acessar **Arquivos → Fazer upload**.
3. Selecionar o arquivo `rgi_mesclado.tsv`.
4. Após o upload, clicar nos três pontinhos ao lado do arquivo.
5. Selecionar **Copiar caminho**.

### Importação da tabela

No código do Google Colab, localizar a linha:

```python
df = pd.read_csv("COLAR", sep="\t")
```

Substituir `COLAR` pelo caminho copiado do arquivo `rgi_mesclado.tsv`.

Assim, a tabela poderá ser carregada no notebook para dar continuidade à análise dos genes de resistência identificados pelo RGI.
