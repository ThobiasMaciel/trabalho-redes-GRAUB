"""Roda todos os experimentos de BER e grava os resultados brutos.

    python experimentos/rodar_experimentos.py

Para cada esquema, canal, Eb/N0 e repeticao: gera bits aleatorios, transmite e conta os erros.
Saidas:
    resultados/brutos/ber_brutos.csv   uma linha por execucao
    resultados/brutos/mensagens.txt    mensagem ASCII recebida em varias condicoes
"""
import csv
import json
import os
import sys
import time

import numpy as np

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, PASTA)

from src.dados import texto_para_bits, bits_para_texto, marcar_erros
from src.enlace import transmitir, NOMES
from src.metricas import contar_erros


def rodar_ber(config, arquivo):
    n_bits = config["bits_por_ponto"]
    with open(arquivo, "w", newline="") as f:
        saida = csv.writer(f)
        saida.writerow(["esquema", "canal", "ebn0_db", "repeticao", "semente", "n_bits", "n_erros", "ber"])
        for i_esq, esquema in enumerate(config["esquemas"]):
            for i_canal, canal in enumerate(config["canais"]):
                inicio = time.time()
                for i_eb, ebn0 in enumerate(config["ebn0_db"]):
                    for rep in range(1, config["repeticoes"] + 1):
                        # cada repeticao tem a sua semente; os indices garantem que
                        # cada combinacao usa numeros aleatorios diferentes
                        semente = config["semente_base"] + rep
                        rng = np.random.default_rng([semente, i_esq, i_canal, i_eb])
                        bits = rng.integers(0, 2, n_bits)
                        recebidos, _, _ = transmitir(bits, esquema, canal, ebn0, rng, config["rajadas"])
                        erros = contar_erros(bits, recebidos)
                        saida.writerow([esquema, canal, ebn0, rep, semente, n_bits, erros, erros / n_bits])
                print(f"  {NOMES[esquema]:<20} {canal:<8} pronto em {time.time() - inicio:.1f} s")


def rodar_mensagens(config, arquivo):
    """Transmite a mensagem ASCII e registra o texto recebido e os erros."""
    mensagem = config["mensagem"]
    bits = texto_para_bits(mensagem)
    with open(arquivo, "w") as f:
        f.write(f"Mensagem enviada ({len(bits)} bits):\n  {mensagem}\n")
        for canal in config["canais"]:
            for ebn0 in config["ebn0_mensagem_db"]:
                f.write(f"\n=== canal {canal}, Eb/N0 = {ebn0} dB ===\n")
                for i_esq, esquema in enumerate(config["esquemas"]):
                    rng = np.random.default_rng([config["semente_base"], i_esq, ebn0])
                    rec, _, _ = transmitir(bits, esquema, canal, ebn0, rng, config["rajadas"])
                    erros = contar_erros(bits, rec)
                    f.write(f"{NOMES[esquema]:<20} {erros:>3} bits errados (BER = {erros / len(bits):.4f})\n")
                    f.write(f"  {bits_para_texto(rec)}\n")
                    f.write(f"  {marcar_erros(bits, rec)}\n")


def main():
    with open(os.path.join(PASTA, "experimentos", "config.json")) as f:
        config = json.load(f)
    os.makedirs(os.path.join(PASTA, "resultados", "brutos"), exist_ok=True)

    print(f"Experimentos de BER: {config['bits_por_ponto']} bits por ponto, "
          f"{config['repeticoes']} repeticoes, Eb/N0 = {config['ebn0_db']} dB")
    rodar_ber(config, os.path.join(PASTA, "resultados", "brutos", "ber_brutos.csv"))
    rodar_mensagens(config, os.path.join(PASTA, "resultados", "brutos", "mensagens.txt"))
    print("Resultados gravados em resultados/brutos/")


if __name__ == "__main__":
    main()
