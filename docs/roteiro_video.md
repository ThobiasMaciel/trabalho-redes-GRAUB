# Roteiro do vídeo (máximo 5 minutos)

Gravação de tela com narração. Deixe o terminal aberto na pasta do repositório, com a fonte grande, e as imagens de `resultados/graficos/` abertas em abas. Ensaie uma vez com cronômetro: o total abaixo dá cerca de 4 min 45 s.

| Tempo | O que mostrar | O que falar |
|---|---|---|
| 0:00 – 0:25 | README no GitHub, no diagrama da arquitetura | "Somos [nomes]. Este é o nosso simulador de transmissão digital. A mensagem ASCII vira bits, passa por codificação de linha ou modulação, atravessa um canal com ruído, e o receptor reconstrói a mensagem. No fim medimos a BER e a eficiência espectral." |
| 0:25 – 0:55 | Terminal: `python simulador.py --ideal` e depois `python simulador.py --esquema qpsk --ebn0 3` | "Em canal ideal a mensagem volta idêntica. Com ruído, em 3 dB, alguns bits chegam errados: o programa mostra o texto recebido, marca os caracteres atingidos e lista as posições dos bits errados." |
| 0:55 – 1:20 | Terminal: `python simulador.py --esquema 16qam --canal rajadas --ebn0 9` | "Este é o segundo cenário de canal: ruído em rajadas. Os erros não ficam espalhados, eles vêm agrupados, e um trecho inteiro da mensagem se perde." |
| 1:20 – 1:40 | Terminal: `python tests/test_consistencia.py` | "O teste de consistência confirma que, sem ruído e em 40 dB, as seis técnicas recuperam a mensagem sem erro, e que a BER simulada bate com a teórica." |
| 1:40 – 2:05 | `experimentos/config.json` e o início de `ber_brutos.csv` | "O plano experimental está neste arquivo: 8 valores de Eb/N0, um milhão de bits por execução e 5 repetições com sementes fixas. São 480 execuções, e cada uma vira uma linha neste CSV. Dois comandos reproduzem todos os resultados e gráficos." |
| 2:05 – 2:50 | `ber_modulacoes.png` | "Estas são as curvas de BER por Eb/N0. Em AWGN os pontos caem sobre as curvas teóricas. BPSK e QPSK têm a mesma BER, mas o QPSK leva o dobro de bits na mesma banda. O 16-QAM leva quatro bits por símbolo e precisa de quase 4 dB a mais para a mesma BER. As barras são o desvio padrão das 5 repetições: só aparecem embaixo, onde há poucos erros contados." |
| 2:50 – 3:25 | `ber_awgn_x_rajadas.png` e `constelacoes.png` | "Com rajadas a curva cai muito mais devagar: para BER de 10⁻³ são cerca de 7 dB a mais. Na constelação dá para ver o motivo: os símbolos atingidos pela rajada, em vermelho, cruzam as fronteiras de decisão." |
| 3:25 – 4:00 | Tabela de compromisso no README | "Esta tabela resume o compromisso. O QPSK é a melhor escolha com sinal fraco. O 16-QAM compensa quando a banda é limitada e o canal é bom, acima de uns 10 dB em AWGN ou 18 dB com rajadas. É a ideia da modulação adaptativa do Wi-Fi." |
| 4:00 – 4:25 | `ber_linha.png` (e, se der tempo, `ber_hamming.png`) | "Nas codificações de linha, o Manchester tem a BER do BPSK, mas ocupa o dobro da banda; o AMI precisa de 3 dB a mais porque usa três níveis. Como extra, o Hamming mostra a diferença para a correção de erros: ele ajuda em AWGN com sinal bom, mas quase não ajuda com rajadas." |
| 4:25 – 4:45 | Seção "Conclusões" do README | "Conclusões: a simulação reproduz a teoria; eficiência espectral custa energia; o tipo de ruído importa tanto quanto o nível; e uma BER só é confiável com erros suficientes. Obrigado." |

## Dicas

- Os dois integrantes devem falar. Sugestão: uma pessoa até 2:05 (demonstração e plano) e a outra de 2:05 em diante (resultados e conclusões).
- Não rode `rodar_experimentos.py` no vídeo (leva ~40 s); mostre os arquivos já gerados.
- Depois de gravar, suba o arquivo em `docs/` ou coloque o link no topo do README. O item 10 da avaliação pede o vídeo disponível no GitHub.
