# Tabelas de resultados

Gerado por `experimentos/gerar_graficos.py`. Cada ponto: 5 repetições de 1.000.000 bits. BER = média ± desvio padrão das repetições. "0" significa nenhum erro em 5.000.000 bits.


## Modulações – canal AWGN

| Eb/N0 (dB) | BPSK | QPSK | 16-QAM |
|---|---|---|---|
| 0 | 7,85e-02 ± 9,71e-05 | 7,86e-02 ± 2,26e-04 | 1,41e-01 ± 1,96e-04 |
| 3 | 2,29e-02 ± 7,79e-05 | 2,27e-02 ± 1,68e-04 | 7,75e-02 ± 2,75e-04 |
| 6 | 2,37e-03 ± 2,56e-05 | 2,41e-03 ± 7,21e-05 | 2,80e-02 ± 1,09e-04 |
| 9 | 3,02e-05 ± 2,86e-06 | 3,30e-05 ± 7,18e-06 | 4,36e-03 ± 5,38e-05 |
| 12 | 0 | 2,00e-07 ± 4,47e-07 | 1,36e-04 ± 1,29e-05 |
| 15 | 0 | 0 | 0 |
| 18 | 0 | 0 | 0 |
| 21 | 0 | 0 | 0 |

## Codificações de linha – canal AWGN

| Eb/N0 (dB) | Manchester | AMI |
|---|---|---|
| 0 | 7,87e-02 ± 2,49e-04 | 2,37e-01 ± 6,16e-04 |
| 3 | 2,28e-02 ± 1,48e-04 | 1,18e-01 ± 1,93e-04 |
| 6 | 2,39e-03 ± 5,31e-05 | 3,47e-02 ± 2,55e-04 |
| 9 | 3,28e-05 ± 6,02e-06 | 3,59e-03 ± 4,77e-05 |
| 12 | 0 | 5,06e-05 ± 7,70e-06 |
| 15 | 0 | 0 |
| 18 | 0 | 0 |
| 21 | 0 | 0 |

## Extra: BPSK com e sem Hamming(7,4) – canal AWGN

| Eb/N0 (dB) | BPSK | BPSK + Hamming(7,4) |
|---|---|---|
| 0 | 7,85e-02 ± 9,71e-05 | 1,19e-01 ± 6,08e-04 |
| 3 | 2,29e-02 ± 7,79e-05 | 3,19e-02 ± 2,13e-04 |
| 6 | 2,37e-03 ± 2,56e-05 | 2,38e-03 ± 6,23e-05 |
| 9 | 3,02e-05 ± 2,86e-06 | 1,20e-05 ± 7,45e-06 |
| 12 | 0 | 0 |
| 15 | 0 | 0 |
| 18 | 0 | 0 |
| 21 | 0 | 0 |

## Modulações – canal Ruído em rajadas

| Eb/N0 (dB) | BPSK | QPSK | 16-QAM |
|---|---|---|---|
| 0 | 1,01e-01 ± 5,46e-04 | 1,01e-01 ± 5,38e-04 | 1,62e-01 ± 1,08e-03 |
| 3 | 4,47e-02 ± 2,43e-04 | 4,43e-02 ± 1,76e-04 | 9,90e-02 ± 4,46e-04 |
| 6 | 1,92e-02 ± 1,24e-04 | 1,91e-02 ± 2,32e-04 | 4,67e-02 ± 6,58e-04 |
| 9 | 9,37e-03 ± 1,46e-04 | 9,58e-03 ± 1,31e-04 | 1,87e-02 ± 2,67e-04 |
| 12 | 3,41e-03 ± 9,74e-05 | 3,39e-03 ± 8,27e-05 | 8,80e-03 ± 1,98e-04 |
| 15 | 5,13e-04 ± 2,75e-05 | 5,42e-04 ± 3,32e-05 | 3,81e-03 ± 9,21e-05 |
| 18 | 1,86e-05 ± 3,91e-06 | 1,60e-05 ± 4,95e-06 | 8,31e-04 ± 4,45e-05 |
| 21 | 0 | 0 | 5,58e-05 ± 3,11e-06 |

## Codificações de linha – canal Ruído em rajadas

| Eb/N0 (dB) | Manchester | AMI |
|---|---|---|
| 0 | 1,03e-01 ± 1,43e-04 | 2,59e-01 ± 3,82e-04 |
| 3 | 4,57e-02 ± 1,57e-04 | 1,48e-01 ± 2,44e-04 |
| 6 | 1,95e-02 ± 1,46e-04 | 6,63e-02 ± 3,62e-04 |
| 9 | 9,33e-03 ± 8,96e-05 | 2,82e-02 ± 3,59e-04 |
| 12 | 3,19e-03 ± 6,87e-05 | 1,42e-02 ± 1,47e-04 |
| 15 | 4,89e-04 ± 1,69e-05 | 5,13e-03 ± 9,12e-05 |
| 18 | 1,32e-05 ± 1,92e-06 | 8,36e-04 ± 3,34e-05 |
| 21 | 0 | 3,00e-05 ± 2,83e-06 |

## Extra: BPSK com e sem Hamming(7,4) – canal Ruído em rajadas

| Eb/N0 (dB) | BPSK | BPSK + Hamming(7,4) |
|---|---|---|
| 0 | 1,01e-01 ± 5,46e-04 | 1,45e-01 ± 4,13e-04 |
| 3 | 4,47e-02 ± 2,43e-04 | 6,02e-02 ± 3,09e-04 |
| 6 | 1,92e-02 ± 1,24e-04 | 2,41e-02 ± 3,50e-04 |
| 9 | 9,37e-03 ± 1,46e-04 | 1,20e-02 ± 2,47e-04 |
| 12 | 3,41e-03 ± 9,74e-05 | 4,02e-03 ± 4,72e-05 |
| 15 | 5,13e-04 ± 2,75e-05 | 4,89e-04 ± 3,81e-05 |
| 18 | 1,86e-05 ± 3,91e-06 | 6,40e-06 ± 3,21e-06 |
| 21 | 0 | 0 |

## Variabilidade entre repetições (canal AWGN)

Coeficiente de variação = desvio padrão / média. Entre parênteses, o número médio de erros por repetição.

| Eb/N0 (dB) | BPSK | QPSK | 16-QAM |
|---|---|---|---|
| 0 | 0,1% (78482) | 0,3% (78600) | 0,1% (140982) |
| 3 | 0,3% (22915) | 0,7% (22722) | 0,4% (77537) |
| 6 | 1,1% (2366) | 3,0% (2414) | 0,4% (28020) |
| 9 | 9,5% (30) | 21,7% (33) | 1,2% (4357) |
| 12 | sem erros | 223,6% (0) | 9,5% (136) |
| 15 | sem erros | sem erros | sem erros |
| 18 | sem erros | sem erros | sem erros |
| 21 | sem erros | sem erros | sem erros |

## Compromisso entre BER e eficiência espectral

| Modulação | Eficiência nominal (bit/s/Hz) | BER em 6 dB (AWGN) | BER em 9 dB (AWGN) | BER em 12 dB (AWGN) | Eb/N0 para BER = 1e-3 (AWGN) | Eb/N0 para BER = 1e-3 (rajadas) |
|---|---|---|---|---|---|---|
| BPSK | 1 | 2,37e-03 | 3,02e-05 | 0 | 6,6 dB | 13,9 dB |
| QPSK | 2 | 2,41e-03 | 3,30e-05 | 2,00e-07 | 6,6 dB | 14,0 dB |
| 16-QAM | 4 | 2,80e-02 | 4,36e-03 | 1,36e-04 | 10,3 dB | 17,6 dB |
