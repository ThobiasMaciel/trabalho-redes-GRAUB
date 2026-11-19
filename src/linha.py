"""Codificacao de linha (banda base): Manchester e AMI.

Convencoes:
  Manchester: bit 1 = baixo (-1) -> alto (+1) no meio do bit
              bit 0 = alto (+1) -> baixo (-1) no meio do bit
              (cada bit vira 2 niveis)
  AMI:        bit 0 = nivel 0
              bit 1 = +1 e -1 alternados, comecando em +1
              (cada bit vira 1 nivel)
"""
import numpy as np


def codificar_linha(bits, tipo):
    bits = np.array(bits)
    if tipo == "manchester":
        nivel = 2 * bits - 1                    # bit 1 -> +1, bit 0 -> -1
        # primeira metade do bit = -nivel, segunda metade = +nivel
        return np.column_stack([-nivel, nivel]).ravel().astype(float)
    if tipo == "ami":
        sinal = np.zeros(len(bits))
        uns = np.flatnonzero(bits == 1)         # posicoes dos bits 1
        sinal[uns] = np.where(np.arange(len(uns)) % 2 == 0, 1.0, -1.0)
        return sinal
    raise ValueError("codificacao de linha desconhecida: " + tipo)


def decodificar_linha(sinal, tipo):
    """Recupera os bits de um sinal que pode ter ruido."""
    if tipo == "manchester":
        pares = np.array(sinal).reshape(-1, 2)
        # se a segunda metade e maior que a primeira, a transicao foi de subida -> bit 1
        return (pares[:, 1] > pares[:, 0]).astype(int)
    if tipo == "ami":
        # limiar no meio do caminho entre 0 e 1 (vale para +1 e -1)
        return (np.abs(sinal) > 0.5).astype(int)
    raise ValueError("codificacao de linha desconhecida: " + tipo)
