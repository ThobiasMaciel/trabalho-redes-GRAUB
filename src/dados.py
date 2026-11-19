"""Conversao entre texto ASCII e bits, e identificacao dos bits errados."""
import numpy as np


def texto_para_bits(texto):
    """Texto ASCII -> array de bits (8 bits por caractere, mais significativo primeiro).

    Exemplo: "A" (codigo 65) -> [0, 1, 0, 0, 0, 0, 0, 1]
    """
    codigos = np.frombuffer(texto.encode("ascii"), dtype=np.uint8)
    return np.unpackbits(codigos).astype(int)


def bits_para_texto(bits):
    """Array de bits -> texto. Agrupa de 8 em 8 bits.

    Um bit errado pode gerar um codigo que nao e um caractere visivel;
    nesse caso o caractere aparece como '?'.
    """
    n = len(bits) // 8 * 8                      # ignora bits que sobram
    codigos = np.packbits(np.array(bits[:n], dtype=np.uint8))
    return "".join(chr(c) if 32 <= c < 127 else "?" for c in codigos)


def posicoes_erradas(enviados, recebidos):
    """Indices dos bits que chegaram diferentes do que foi enviado."""
    return np.flatnonzero(np.array(enviados) != np.array(recebidos))


def marcar_erros(enviados, recebidos):
    """Linha com '^' embaixo de cada caractere que tem pelo menos um bit errado."""
    erros = posicoes_erradas(enviados, recebidos)
    n_caracteres = len(enviados) // 8
    marca = [" "] * n_caracteres
    for pos in erros:
        if pos // 8 < n_caracteres:
            marca[pos // 8] = "^"
    return "".join(marca)
