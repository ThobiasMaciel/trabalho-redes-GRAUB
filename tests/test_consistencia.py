"""Teste de consistencia: em canal ideal (e em Eb/N0 muito alto) a mensagem volta identica.

    python tests/test_consistencia.py
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.dados import texto_para_bits, bits_para_texto
from src.enlace import transmitir, ESQUEMAS, NOMES
from src.metricas import ber, ber_teorica

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
with open(os.path.join(PASTA, "experimentos", "config.json")) as f:
    CONFIG = json.load(f)


def main():
    mensagem = CONFIG["mensagem"]
    bits = texto_para_bits(mensagem)
    falhas = 0

    print("1) Conversao ASCII -> bits -> ASCII")
    ok = bits_para_texto(bits) == mensagem
    falhas += not ok
    print("   ", "ok" if ok else "FALHOU")

    print("2) Canal ideal (sem ruido) e Eb/N0 = 40 dB: a mensagem deve voltar identica")
    for esquema in ESQUEMAS:
        for canal in CONFIG["canais"]:
            for ebn0 in (None, 40):
                rng = np.random.default_rng(1)
                rec, _, _ = transmitir(bits, esquema, canal, ebn0, rng, CONFIG["rajadas"])
                ok = bits_para_texto(rec) == mensagem and ber(bits, rec) == 0
                falhas += not ok
                nome = "ideal" if ebn0 is None else "40 dB"
                print(f"    {NOMES[esquema]:<20} {canal:<8} {nome:<6} {'ok' if ok else 'FALHOU'}")

    print("3) BER simulada x teorica em AWGN (200.000 bits, Eb/N0 = 6 dB)")
    rng = np.random.default_rng(2)
    aleatorios = rng.integers(0, 2, 200000)
    for esquema in ("bpsk", "qpsk", "16qam", "manchester", "ami"):
        rec, _, _ = transmitir(aleatorios, esquema, "awgn", 6, rng)
        simulada = ber(aleatorios, rec)
        teorica = ber_teorica(esquema, 6)
        ok = abs(simulada - teorica) < 0.15 * teorica      # tolerancia de 15%
        falhas += not ok
        print(f"    {NOMES[esquema]:<12} simulada = {simulada:.5f}  teorica = {teorica:.5f}  {'ok' if ok else 'FALHOU'}")

    print()
    print("Todos os testes passaram." if falhas == 0 else f"{falhas} teste(s) falharam.")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
