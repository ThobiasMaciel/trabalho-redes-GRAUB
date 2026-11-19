"""Modelos de canal: AWGN e ruido em rajadas.

O nivel de ruido e controlado por Eb/N0 (energia por bit / densidade de ruido), em dB.
Com Eb/N0 todas as tecnicas sao comparadas gastando a mesma energia por bit de informacao.

    N0 = Eb / (Eb/N0)        variancia do ruido por dimensao = N0 / 2
"""
import numpy as np


def energia_por_bit(sinal, n_bits):
    """Eb medio: energia total do sinal dividida pelo numero de bits de informacao."""
    return np.sum(np.abs(sinal) ** 2) / n_bits


def sigma_ruido(ebn0_db, eb):
    """Desvio padrao do ruido (por dimensao) para um Eb/N0 em dB."""
    ebn0 = 10 ** (ebn0_db / 10)
    n0 = eb / ebn0
    return np.sqrt(n0 / 2)


def gerar_ruido(sinal, sigma, rng):
    """Ruido gaussiano; se o sinal e complexo, o ruido tem parte real e imaginaria."""
    ruido = rng.normal(0, 1, len(sinal)) * sigma
    if np.iscomplexobj(sinal):
        ruido = ruido + 1j * rng.normal(0, 1, len(sinal)) * sigma
    return ruido


def canal_awgn(sinal, ebn0_db, eb, rng):
    """Canal AWGN. Com ebn0_db = None o canal e ideal (sem ruido)."""
    if ebn0_db is None:
        return np.array(sinal).copy()
    return sinal + gerar_ruido(sinal, sigma_ruido(ebn0_db, eb), rng)


def estados_rajada(n, p_bom_ruim, p_ruim_bom, rng):
    """Sequencia de estados do canal (False = bom, True = ruim) para n amostras.

    Modelo de dois estados (tipo Gilbert-Elliott): a cada amostra o canal pode
    trocar de estado. O tempo em cada estado segue uma distribuicao geometrica:
    duracao media no estado bom = 1/p_bom_ruim, no ruim = 1/p_ruim_bom.
    """
    estados = np.zeros(n, dtype=bool)
    pos = 0
    ruim = False                                # comeca no estado bom
    while pos < n:
        duracao = rng.geometric(p_ruim_bom if ruim else p_bom_ruim)
        estados[pos:pos + duracao] = ruim
        pos += duracao
        ruim = not ruim
    return estados


def canal_rajadas(sinal, ebn0_db, eb, rng, params, devolver_estados=False):
    """Canal com ruido em rajadas.

    No estado bom o ruido e o do Eb/N0 pedido (igual ao AWGN).
    No estado ruim (rajada) o ruido fica params["extra_db"] dB mais forte.
    """
    estados = estados_rajada(len(sinal), params["p_bom_ruim"], params["p_ruim_bom"], rng)
    if ebn0_db is None:
        recebido = np.array(sinal).copy()
    else:
        sigma = sigma_ruido(ebn0_db, eb)
        fator_ruim = 10 ** (params["extra_db"] / 20)     # dB de potencia -> fator de amplitude
        ruido = gerar_ruido(sinal, sigma, rng)
        ruido[estados] *= fator_ruim
        recebido = sinal + ruido
    if devolver_estados:
        return recebido, estados
    return recebido
