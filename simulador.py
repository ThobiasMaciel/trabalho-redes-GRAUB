
import argparse
import json
import os

import numpy as np

from src.dados import texto_para_bits, bits_para_texto, posicoes_erradas, marcar_erros
from src.enlace import transmitir, ESQUEMAS, NOMES, MODULACOES
from src.metricas import eficiencia_espectral

PASTA = os.path.dirname(os.path.abspath(__file__))


def main():
    with open(os.path.join(PASTA, "experimentos", "config.json")) as f:
        config = json.load(f)

    ap = argparse.ArgumentParser(description="Simulador de transmissao digital")
    ap.add_argument("--mensagem", default=config["mensagem"])
    ap.add_argument("--esquema", default="qpsk", choices=ESQUEMAS)
    ap.add_argument("--canal", default="awgn", choices=["awgn", "rajadas"])
    ap.add_argument("--ebn0", type=float, default=6.0, help="Eb/N0 em dB")
    ap.add_argument("--ideal", action="store_true", help="canal sem ruido")
    ap.add_argument("--semente", type=int, default=config["semente_base"])
    args = ap.parse_args()

    try:
        bits = texto_para_bits(args.mensagem)
    except UnicodeEncodeError:
        print("Erro: a mensagem deve ter apenas caracteres ASCII (sem acentos).")
        return

    rng = np.random.default_rng(args.semente)
    ebn0 = None if args.ideal else args.ebn0
    recebidos, _, _ = transmitir(bits, args.esquema, args.canal, ebn0, rng, config["rajadas"])
    erros = posicoes_erradas(bits, recebidos)

    print("Esquema ............", NOMES[args.esquema])
    if args.esquema in MODULACOES:
        print("Efic. espectral ....", f"{eficiencia_espectral(args.esquema):.0f} bit/s/Hz (nominal)")
    print("Canal ..............", args.canal, "(ideal, sem ruido)" if args.ideal else f"com Eb/N0 = {args.ebn0:g} dB")
    print("Bits transmitidos ..", len(bits))
    print("Primeiros bits .....", "".join(str(b) for b in bits[:32]), "...")
    print()
    print("Enviada :", args.mensagem)
    print("Recebida:", bits_para_texto(recebidos))
    print("         " + marcar_erros(bits, recebidos))
    print()
    print("Bits errados .......", len(erros), "de", len(bits), f"(BER = {len(erros) / len(bits):.4f})")
    if len(erros):
        print("Posicoes dos erros .", ", ".join(str(p) for p in erros[:20]) + (" ..." if len(erros) > 20 else ""))
    else:
        print("Mensagem recuperada sem erros.")


if __name__ == "__main__":
    main()
