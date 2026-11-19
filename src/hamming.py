"""Extra: codigo de correcao de erros Hamming(7,4).

Serve para mostrar a diferenca entre codificacao de LINHA (formato do sinal)
e codificacao de CORRECAO DE ERROS (bits de redundancia que permitem corrigir).
Cada bloco de 4 bits de dados vira 7 bits; o receptor corrige 1 bit errado por bloco.
"""
import numpy as np

# matriz geradora (4 bits de dados + 3 de paridade) e matriz de verificacao
G = np.array([[1, 0, 0, 0, 1, 1, 0],
              [0, 1, 0, 0, 1, 0, 1],
              [0, 0, 1, 0, 0, 1, 1],
              [0, 0, 0, 1, 1, 1, 1]])
H = np.array([[1, 1, 0, 1, 1, 0, 0],
              [1, 0, 1, 1, 0, 1, 0],
              [0, 1, 1, 1, 0, 0, 1]])


def codificar(bits):
    bits = np.array(bits)
    falta = (-len(bits)) % 4
    if falta:
        bits = np.concatenate([bits, np.zeros(falta, dtype=int)])
    return (bits.reshape(-1, 4) @ G % 2).ravel()


def decodificar(bits):
    blocos = np.array(bits).reshape(-1, 7).copy()
    sindrome = blocos @ H.T % 2                  # 000 = sem erro detectado
    # a sindrome e igual a coluna de H da posicao errada: procura e inverte o bit
    for pos in range(7):
        errado = np.all(sindrome == H[:, pos], axis=1)
        blocos[errado, pos] ^= 1
    return blocos[:, :4].ravel()
