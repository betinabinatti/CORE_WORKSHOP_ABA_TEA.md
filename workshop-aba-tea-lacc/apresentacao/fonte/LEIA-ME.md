# Fonte da apresentação

- `slides/*.html`: um arquivo por slide; a ordem está em `deck.json`.
- `build.py`: junta os slides em um HTML único (e um HTML de notas), que é convertido em PDF com o Chromium:

```
python3 build.py <pasta com project/deck.json e project/slides> slides.html notas.html
chrome --headless --no-pdf-header-footer --print-to-pdf=slides.pdf slides.html
```

O conteúdo segue `SLIDES.md` v1.1 (com a vinheta do Theo dividida em 35 e 35b e o slide do vídeo, s34v = S34a).

- `animacao.py` + `audio.py`: geram o vídeo e a trilha (PIL, numpy, ffmpeg): `python3 animacao.py video_mudo.mp4`, `python3 audio.py trilha.wav`, depois `ffmpeg -i video_mudo.mp4 -i trilha.wav -c:v copy -c:a aac -shortest Video_Theo_animacao.mp4`.
- `lara_anim.py` + `lara_audio.py`: geram `Video_Lara_animacao.mp4` do mesmo jeito que o vídeo do Theo (`lara_anim.py` importa `animacao.py`).

## Versão PowerPoint

- `pptx_extrair.js` + `gerar_pptx.py`: geram `Apresentacao_Workshop_ABA_TEA.pptx` a partir do HTML de `build.py` (texto editável, tabelas nativas, notas e vídeos embutidos):

```
node pptx_extrair.js slides.html layout.json
python3 gerar_pptx.py layout.json ../Apresentacao_Workshop_ABA_TEA.pptx
```
