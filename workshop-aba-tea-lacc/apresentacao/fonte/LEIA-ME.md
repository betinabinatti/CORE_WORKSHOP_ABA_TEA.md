# Fonte da apresentação

- `slides/*.html`: um arquivo por slide; a ordem está em `deck.json`.
- `build.py`: junta os slides em um HTML único (e um HTML de notas), que é convertido em PDF com o Chromium:

```
python3 build.py <pasta com project/deck.json e project/slides> slides.html notas.html
chrome --headless --no-pdf-header-footer --print-to-pdf=slides.pdf slides.html
```

O conteúdo segue `SLIDES.md` v1.1 (com a vinheta do Theo dividida em 35 e 35b e o slide do vídeo, s34v = S34a).

- `animacao.py` + `audio.py`: geram o vídeo e a trilha (PIL, numpy, ffmpeg): `python3 animacao.py video_mudo.mp4`, `python3 audio.py trilha.wav`, depois `ffmpeg -i video_mudo.mp4 -i trilha.wav -c:v copy -c:a aac -shortest Video_Theo_animacao.mp4`.
