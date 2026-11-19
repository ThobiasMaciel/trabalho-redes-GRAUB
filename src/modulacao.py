"""Modulacoes digitais em banda base equivalente: BPSK, QPSK e 16-QAM.

Cada simbolo e um numero complexo (parte real = eixo I, parte imaginaria = eixo Q).
Todas as constelacoes tem energia media de simbolo Es = 1.
QPSK e 16-QAM usam mapeamento de Gray (simbolos vizinhos diferem em 1 bit).
"""
import numpy as np

BITS_POR_SIMBOLO = {"bpsk": 1, "qpsk": 2, "16qam": 4}


def modular(bits, esquema):
    k = BITS_POR_SIMBOLO[esquema]
    bits = np.array(bits)
    falta = (-len(bits)) % k                    # completa com zeros se precisar
    if falta:
        bits = np.concatenate([bits, np.zeros(falta, dtype=int)])
    b = bits.reshape(-1, k)

    if esquema == "bpsk":
        # bit 1 -> +1, bit 0 -> -1
        return (2 * b[:, 0] - 1).astype(complex)
    if esquema == "qpsk":
        # 1 bit em cada eixo; divide por raiz(2) para Es = 1
        i = 2 * b[:, 0] - 1
        q = 2 * b[:, 1] - 1
        return (i + 1j * q) / np.sqrt(2)
    if esquema == "16qam":
        # 2 bits em cada eixo, niveis -3, -1, +1, +3 (Gray: 00, 01, 11, 10)
        i = (2 * b[:, 0] - 1) * (3 - 2 * b[:, 1])
        q = (2 * b[:, 2] - 1) * (3 - 2 * b[:, 3])
        return (i + 1j * q) / np.sqrt(10)       # raiz(10) para Es = 1
    raise ValueError("modulacao desconhecida: " + esquema)


def demodular(simbolos, esquema):
    """Decide o ponto da constelacao mais proximo e devolve os bits."""
    s = np.array(simbolos)
    if esquema == "bpsk":
        return (s.real > 0).astype(int)
    if esquema == "qpsk":
        return np.column_stack([s.real > 0, s.imag > 0]).astype(int).ravel()
    if esquema == "16qam":
        i = s.real * np.sqrt(10)
        q = s.imag * np.sqrt(10)
        # em cada eixo: 1o bit = lado (positivo/negativo), 2o bit = nivel interno (|x| < 2)
        return np.column_stack([i > 0, np.abs(i) < 2, q > 0, np.abs(q) < 2]).astype(int).ravel()
    raise ValueError("modulacao desconhecida: " + esquema)
