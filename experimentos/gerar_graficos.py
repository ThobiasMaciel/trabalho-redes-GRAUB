"""Le os resultados brutos e gera o resumo, as tabelas e todos os graficos.

    python experimentos/gerar_graficos.py

Saidas:
    resultados/resumo.csv      media, desvio padrao, minimo e maximo da BER por ponto
    resultados/tabelas.md      tabelas prontas (BER, variabilidade, compromisso)
    resultados/graficos/*.png
"""
import csv
import json
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, PASTA)

from src.canal import canal_awgn, canal_rajadas, energia_por_bit
from src.dados import texto_para_bits
from src.enlace import NOMES, MODULACOES, LINHAS
from src.linha import codificar_linha
from src.metricas import ber_teorica, eficiencia_espectral
from src.modulacao import modular

GRAFICOS = os.path.join(PASTA, "resultados", "graficos")
CORES = {"bpsk": "#2a78d6", "qpsk": "#eb6834", "16qam": "#1baf7a",
         "manchester": "#2a78d6", "ami": "#eb6834", "bpsk+hamming": "#eb6834"}
MARCAS = {"bpsk": "o", "qpsk": "s", "16qam": "^", "manchester": "o", "ami": "s", "bpsk+hamming": "s"}
NOME_CANAL = {"awgn": "AWGN", "rajadas": "Ruído em rajadas"}
CINZA = "#6b6b6b"
TEXTO = "#222222"
PISO = 1e-7          # limite inferior do eixo de BER


# ---------- leitura e resumo ----------

def ler_brutos():
    """Devolve {(esquema, canal, ebn0): [ber de cada repeticao]}."""
    dados = {}
    with open(os.path.join(PASTA, "resultados", "brutos", "ber_brutos.csv")) as f:
        for linha in csv.DictReader(f):
            chave = (linha["esquema"], linha["canal"], int(linha["ebn0_db"]))
            dados.setdefault(chave, []).append(float(linha["ber"]))
    return dados


def resumir(dados, n_bits):
    """Media, desvio padrao (amostral), minimo, maximo e total de erros de cada ponto."""
    resumo = {}
    for chave, valores in dados.items():
        v = np.array(valores)
        resumo[chave] = {"media": v.mean(), "desvio": v.std(ddof=1), "min": v.min(), "max": v.max(),
                         "erros": int(round(v.sum() * n_bits)), "n": len(v)}
    return resumo


def gravar_resumo(resumo):
    with open(os.path.join(PASTA, "resultados", "resumo.csv"), "w", newline="") as f:
        saida = csv.writer(f)
        saida.writerow(["esquema", "canal", "ebn0_db", "repeticoes", "ber_media", "ber_desvio",
                        "ber_min", "ber_max", "erros_totais"])
        for (esq, canal, eb), r in resumo.items():
            saida.writerow([esq, canal, eb, r["n"], f"{r['media']:.3e}", f"{r['desvio']:.3e}",
                            f"{r['min']:.3e}", f"{r['max']:.3e}", r["erros"]])


def ebn0_para_ber(resumo, esquema, canal, ebn0s, alvo):
    """Eb/N0 (dB) em que a BER media cruza o alvo, por interpolacao em escala log."""
    for a, b in zip(ebn0s[:-1], ebn0s[1:]):
        ya, yb = resumo[(esquema, canal, a)]["media"], resumo[(esquema, canal, b)]["media"]
        if ya >= alvo > yb:
            if yb == 0:
                return None
            fracao = (math.log10(ya) - math.log10(alvo)) / (math.log10(ya) - math.log10(yb))
            return a + fracao * (b - a)
    return None


# ---------- tabelas ----------

def fmt(x):
    if x == 0:
        return "0"
    return f"{x:.2e}".replace(".", ",")


def gravar_tabelas(resumo, config):
    ebn0s = config["ebn0_db"]
    n_total = config["bits_por_ponto"] * config["repeticoes"]
    t = []
    t.append("# Tabelas de resultados\n")
    t.append(f"Gerado por `experimentos/gerar_graficos.py`. Cada ponto: {config['repeticoes']} repetições de "
             f"{config['bits_por_ponto']:,} bits.".replace(",", ".") + " BER = média ± desvio padrão das repetições. "
             f"\"0\" significa nenhum erro em {n_total:,} bits.\n".replace(",", "."))

    for canal in config["canais"]:
        for titulo, grupo in (("Modulações", MODULACOES), ("Codificações de linha", LINHAS),
                              ("Extra: BPSK com e sem Hamming(7,4)", ["bpsk", "bpsk+hamming"])):
            t.append(f"\n## {titulo} – canal {NOME_CANAL[canal]}\n")
            t.append("| Eb/N0 (dB) | " + " | ".join(NOMES[e] for e in grupo) + " |")
            t.append("|---|" + "---|" * len(grupo))
            for eb in ebn0s:
                celulas = []
                for e in grupo:
                    r = resumo[(e, canal, eb)]
                    celulas.append("0" if r["media"] == 0 else f"{fmt(r['media'])} ± {fmt(r['desvio'])}")
                t.append(f"| {eb} | " + " | ".join(celulas) + " |")

    t.append("\n## Variabilidade entre repetições (canal AWGN)\n")
    t.append("Coeficiente de variação = desvio padrão / média. Entre parênteses, o número médio de erros por repetição.\n")
    t.append("| Eb/N0 (dB) | " + " | ".join(NOMES[e] for e in MODULACOES) + " |")
    t.append("|---|---|---|---|")
    for eb in ebn0s:
        celulas = []
        for e in MODULACOES:
            r = resumo[(e, "awgn", eb)]
            if r["media"] == 0:
                celulas.append("sem erros")
            else:
                celulas.append(f"{100 * r['desvio'] / r['media']:.1f}% ({r['erros'] / r['n']:.0f})".replace(".", ","))
        t.append(f"| {eb} | " + " | ".join(celulas) + " |")

    t.append("\n## Compromisso entre BER e eficiência espectral\n")
    t.append("| Modulação | Eficiência nominal (bit/s/Hz) | BER em 6 dB (AWGN) | BER em 9 dB (AWGN) | BER em 12 dB (AWGN) "
             "| Eb/N0 para BER = 1e-3 (AWGN) | Eb/N0 para BER = 1e-3 (rajadas) |")
    t.append("|---|---|---|---|---|---|---|")
    for e in MODULACOES:
        linha = [NOMES[e], f"{eficiencia_espectral(e):.0f}"]
        linha += [fmt(resumo[(e, "awgn", eb)]["media"]) for eb in (6, 9, 12)]
        for canal in ("awgn", "rajadas"):
            x = ebn0_para_ber(resumo, e, canal, ebn0s, 1e-3)
            linha.append("acima de 21 dB" if x is None else f"{x:.1f} dB".replace(".", ","))
        t.append("| " + " | ".join(linha) + " |")

    with open(os.path.join(PASTA, "resultados", "tabelas.md"), "w") as f:
        f.write("\n".join(t) + "\n")


# ---------- graficos ----------

def novo_eixo(ax):
    ax.grid(True, which="major", color="#e4e4e4", linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#9a9a9a")
    ax.tick_params(colors=CINZA, labelsize=8)


def salvar(fig, nome):
    os.makedirs(GRAFICOS, exist_ok=True)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAFICOS, nome), dpi=180, facecolor="white")
    plt.close(fig)


def curva(ax, resumo, esquema, canal, ebn0s, rotulo, estilo="-", cor=None, preenchido=True):
    """Desenha a BER media com barras de erro (desvio padrao). Pontos com BER 0 ficam de fora."""
    xs, ys, baixo, cima = [], [], [], []
    for eb in ebn0s:
        r = resumo[(esquema, canal, eb)]
        if r["media"] > 0:
            xs.append(eb)
            ys.append(r["media"])
            baixo.append(min(r["desvio"], r["media"] - PISO / 10))   # nao deixa a barra passar de zero
            cima.append(r["desvio"])
    cor = cor or CORES[esquema]
    ax.errorbar(xs, ys, yerr=[baixo, cima], fmt=MARCAS[esquema] + estilo, color=cor, markersize=5,
                linewidth=1.4, capsize=3, elinewidth=1, label=rotulo,
                markerfacecolor=cor if preenchido else "white")


def eixo_ber(ax, ebn0s, titulo):
    novo_eixo(ax)
    ax.set_yscale("log")
    ax.set_ylim(PISO, 1)
    ax.set_xticks(ebn0s)
    ax.set_xlim(ebn0s[0] - 1, ebn0s[-1] + 1)
    ax.set_xlabel("Eb/N0 (dB)", color=TEXTO, fontsize=9)
    ax.set_title(titulo, loc="left", fontsize=10, color=TEXTO)


def teoria(ax, esquema, ebn0s, rotulo=None):
    xs = np.linspace(ebn0s[0], ebn0s[-1], 200)
    ys = [ber_teorica(esquema, x) for x in xs]
    ax.plot(xs, ys, ":", color=CORES[esquema], linewidth=1.2, label=rotulo)


def grafico_ber_grupo(resumo, config, grupo, nome_arquivo, com_teoria=True):
    """Dois paineis lado a lado (AWGN e rajadas) com as curvas de um grupo de esquemas."""
    ebn0s = config["ebn0_db"]
    fig, eixos = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True)
    for ax, canal in zip(eixos, config["canais"]):
        eixo_ber(ax, ebn0s, "Canal " + NOME_CANAL[canal])
        for e in grupo:
            # QPSK tracejado e sem preenchimento para aparecer junto do BPSK (as curvas coincidem)
            if e == "qpsk":
                curva(ax, resumo, e, canal, ebn0s, "QPSK (coincide com BPSK)", estilo="--", preenchido=False)
            else:
                curva(ax, resumo, e, canal, ebn0s, NOMES[e])
            if com_teoria and canal == "awgn":
                teoria(ax, e, ebn0s)
        if com_teoria and canal == "awgn":
            ax.plot([], [], ":", color=CINZA, linewidth=1.2, label="teórica (AWGN)")
        ax.legend(frameon=False, fontsize=8, loc="lower left")
    eixos[0].set_ylabel("BER (média de 5 repetições, barra = desvio padrão)", color=TEXTO, fontsize=9)
    salvar(fig, nome_arquivo)


def grafico_comparacao_canais(resumo, config):
    """Um painel por modulacao, comparando AWGN e rajadas."""
    ebn0s = config["ebn0_db"]
    fig, eixos = plt.subplots(1, 3, figsize=(11, 4.2), sharey=True)
    for ax, e in zip(eixos, MODULACOES):
        eixo_ber(ax, ebn0s, NOMES[e])
        curva(ax, resumo, e, "awgn", ebn0s, "AWGN")
        curva(ax, resumo, e, "rajadas", ebn0s, "Rajadas", estilo="--", preenchido=False)
        ax.legend(frameon=False, fontsize=8, loc="lower left")
    eixos[0].set_ylabel("BER (média ± desvio padrão)", color=TEXTO, fontsize=9)
    salvar(fig, "ber_awgn_x_rajadas.png")


def grafico_constelacoes(config):
    """Constelacoes: enviada, depois do AWGN e depois do canal em rajadas."""
    ebn0 = config["ebn0_constelacao_db"]
    rng = np.random.default_rng(config["semente_base"])
    fig, eixos = plt.subplots(3, 3, figsize=(9, 9))
    for linha, e in enumerate(MODULACOES):
        k = int(eficiencia_espectral(e))
        bits = rng.integers(0, 2, 1500 * k)
        enviado = modular(bits, e)
        eb = energia_por_bit(enviado, len(bits))
        awgn = canal_awgn(enviado, ebn0, eb, rng)
        rajadas, estados = canal_rajadas(enviado, ebn0, eb, rng, config["rajadas"], devolver_estados=True)

        ax = eixos[linha][0]
        ax.plot(enviado.real, enviado.imag, "o", color=CORES[e], markersize=6)
        ax.set_title(f"{NOMES[e]} – enviada", loc="left", fontsize=10, color=TEXTO)

        ax = eixos[linha][1]
        ax.plot(awgn.real, awgn.imag, ".", color=CORES[e], markersize=2.5, alpha=0.6)
        ax.set_title(f"depois do AWGN ({ebn0} dB)", loc="left", fontsize=10, color=TEXTO)

        ax = eixos[linha][2]
        ax.plot(rajadas[~estados].real, rajadas[~estados].imag, ".", color=CORES[e], markersize=2.5,
                alpha=0.6, label="estado bom")
        ax.plot(rajadas[estados].real, rajadas[estados].imag, "x", color="#d62728", markersize=3.5,
                alpha=0.8, label="em rajada")
        ax.set_title(f"depois das rajadas ({ebn0} dB)", loc="left", fontsize=10, color=TEXTO)
        if linha == 0:
            ax.legend(frameon=False, fontsize=8, loc="lower right", bbox_to_anchor=(1.02, 1.08),
                      ncol=2, markerscale=2, columnspacing=1, handletextpad=0.2)

        for ax in eixos[linha]:
            novo_eixo(ax)
            ax.set_xlim(-2, 2)
            ax.set_ylim(-2, 2)
            ax.set_aspect("equal")
            ax.axhline(0, color="#b5b5b5", linewidth=0.8)
            ax.axvline(0, color="#b5b5b5", linewidth=0.8)
    eixos[2][0].set_xlabel("I (em fase)", color=TEXTO, fontsize=9)
    eixos[2][0].set_ylabel("Q (quadratura)", color=TEXTO, fontsize=9)
    salvar(fig, "constelacoes.png")


def grafico_linha(config):
    """Formas de onda de Manchester e AMI para os 16 primeiros bits da mensagem."""
    bits = texto_para_bits(config["mensagem"])[:16]
    n = len(bits)
    fig, eixos = plt.subplots(2, 1, figsize=(9, 4.4), sharex=True)
    for ax, tipo in zip(eixos, LINHAS):
        sinal = codificar_linha(bits, tipo)
        por_bit = len(sinal) // n
        t = np.arange(len(sinal) + 1) / por_bit
        novo_eixo(ax)
        ax.step(t, np.append(sinal, sinal[-1]), where="post", color=CORES[tipo], linewidth=2)
        for i in range(n + 1):
            ax.axvline(i, color="#b5b5b5", linestyle="--", linewidth=0.8)
        ax.set_ylim(-1.5, 1.5)
        ax.set_yticks([-1, 0, 1])
        ax.set_yticklabels(["-1", "0", "+1"])
        ax.set_title(NOMES[tipo], loc="left", fontsize=10, color=TEXTO, pad=16 if tipo == LINHAS[0] else 6)
    for i, b in enumerate(bits):
        eixos[0].text(i + 0.5, 1.02, str(b), transform=eixos[0].get_xaxis_transform(),
                      ha="center", va="bottom", fontsize=9, color=TEXTO)
    eixos[-1].set_xlim(0, n)
    eixos[-1].set_xlabel("Tempo (intervalos de bit) – 16 primeiros bits da mensagem", color=TEXTO, fontsize=9)
    salvar(fig, "codificacao_linha.png")


def main():
    with open(os.path.join(PASTA, "experimentos", "config.json")) as f:
        config = json.load(f)
    resumo = resumir(ler_brutos(), config["bits_por_ponto"])
    gravar_resumo(resumo)
    gravar_tabelas(resumo, config)
    grafico_ber_grupo(resumo, config, MODULACOES, "ber_modulacoes.png")
    grafico_ber_grupo(resumo, config, LINHAS, "ber_linha.png")
    grafico_ber_grupo(resumo, config, ["bpsk", "bpsk+hamming"], "ber_hamming.png", com_teoria=False)
    grafico_comparacao_canais(resumo, config)
    grafico_constelacoes(config)
    grafico_linha(config)
    print("Resumo, tabelas e graficos gravados em resultados/")


if __name__ == "__main__":
    main()
