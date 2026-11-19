"""Metricas: BER, eficiencia espectral nominal e curvas teoricas de BER em AWGN."""
import math
import numpy as np

from src.modulacao import BITS_POR_SIMBOLO


def contar_erros(enviados, recebidos):
    return int(np.sum(np.array(enviados) != np.array(recebidos)))


def ber(enviados, recebidos):
    """Taxa de erro de bits = bits errados / bits transmitidos."""
    return contar_erros(enviados, recebidos) / len(enviados)


def eficiencia_espectral(esquema):
    """Eficiencia espectral nominal em bit/s/Hz: log2(M) = bits por simbolo.

    "Nominal" = filtro ideal de Nyquist (banda igual a taxa de simbolos), sem roll-off.
    """
    return float(BITS_POR_SIMBOLO[esquema])


def q_func(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


def ber_teorica(esquema, ebn0_db):
    """BER teorica em canal AWGN (aproximada para 16-QAM e AMI)."""
    ebn0 = 10 ** (ebn0_db / 10)
    if esquema in ("bpsk", "qpsk", "manchester"):
        return q_func(math.sqrt(2 * ebn0))
    if esquema == "16qam":
        return 0.75 * q_func(math.sqrt(0.8 * ebn0))
    if esquema == "ami":
        return 1.5 * q_func(math.sqrt(ebn0))
    raise ValueError("sem curva teorica para " + esquema)
