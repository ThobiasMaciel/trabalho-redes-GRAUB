"""Enlace completo: bits -> transmissor -> canal -> receptor -> bits."""
import numpy as np

from src import hamming
from src.canal import canal_awgn, canal_rajadas, energia_por_bit
from src.linha import codificar_linha, decodificar_linha
from src.modulacao import modular, demodular

LINHAS = ["manchester", "ami"]
MODULACOES = ["bpsk", "qpsk", "16qam"]
ESQUEMAS = LINHAS + MODULACOES + ["bpsk+hamming"]

NOMES = {"manchester": "Manchester", "ami": "AMI", "bpsk": "BPSK", "qpsk": "QPSK",
         "16qam": "16-QAM", "bpsk+hamming": "BPSK + Hamming(7,4)"}


def transmitir(bits, esquema, canal, ebn0_db, rng, rajadas=None):
    """Passa os bits pelo enlace e devolve (bits recebidos, sinal enviado, sinal recebido).

    esquema: "manchester", "ami", "bpsk", "qpsk", "16qam" ou "bpsk+hamming"
    canal:   "awgn" ou "rajadas"
    ebn0_db: Eb/N0 em dB (None = canal ideal, sem ruido)
    """
    bits = np.array(bits)
    n = len(bits)

    # transmissor
    if esquema in LINHAS:
        enviado = codificar_linha(bits, esquema)
    elif esquema == "bpsk+hamming":
        enviado = modular(hamming.codificar(bits), "bpsk")
    else:
        enviado = modular(bits, esquema)

    # canal (Eb e sempre a energia por bit de INFORMACAO)
    eb = energia_por_bit(enviado, n)
    if canal == "awgn":
        recebido = canal_awgn(enviado, ebn0_db, eb, rng)
    elif canal == "rajadas":
        recebido = canal_rajadas(enviado, ebn0_db, eb, rng, rajadas)
    else:
        raise ValueError("canal desconhecido: " + canal)

    # receptor
    if esquema in LINHAS:
        bits_rec = decodificar_linha(recebido, esquema)
    elif esquema == "bpsk+hamming":
        bits_rec = hamming.decodificar(demodular(recebido, "bpsk"))
    else:
        bits_rec = demodular(recebido, esquema)
    return bits_rec[:n], enviado, recebido
