# Ragnarok Online PixelBot MVP

Este projeto  um bot de automao visual para Ragnarok Online, utilizando Viso Computacional para deteco de movimento e template matching.

## Estrutura do Projeto
- `config.py`: Definies de resoluo e parmetros de deteco.
- `capture.py`: Captura de tela otimizada com MSS.
- `detector.py`: Lgica de processamento de imagem e deteco de mobs.
- `attacker.py`: Aes de clique e loot com simulao humana.
- `main.py`: Ponto de entrada do bot.
- `sprites/`: Pasta para armazenar capturas dos monstros (.png).

## Instalao
```bash
pip install -r requirements.txt
```

## Uso
1. Configure a resoluo do jogo em `config.py`.
2. Adicione capturas dos monstros na pasta `sprites/`.
3. Execute `python main.py`.
4. Pressione 'Q' para encerrar.

Para detalhes completos da arquitetura, veja o arquivo de documentao gerado no sistema.
