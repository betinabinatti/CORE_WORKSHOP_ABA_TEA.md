"""Trilha sonora e efeitos sintetizados para a animação do Theo (34 s).

Tudo é sintetizado com numpy (sem amostras de terceiros). Gera WAV estéreo 44,1 kHz.
Uso: python3 audio.py saida.wav
Linha do tempo (s): título 0–3,5 · brincar 3,5–9,5 · guardar 9,5–16 ·
episódio 16–23,5 · devolver 23,5–30 · final 30–34.
"""
import sys
import wave

import numpy as np

SR = 44100
DUR = 34.0
N = int(SR * DUR)
rng = np.random.default_rng(7)


def t_arr(n):
    return np.arange(n) / SR


def place(buf, start, sig, gain=1.0):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i] * gain


def env_ad(n, a=0.005, decay=0.3):
    t = t_arr(n)
    e = np.exp(-t / decay)
    na = max(1, int(a * SR))
    e[:na] *= np.linspace(0, 1, na)
    return e


def smooth(x, ms):
    k = max(1, int(SR * ms / 1000))
    return np.convolve(x, np.ones(k) / k, mode="same")


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ---------- instrumentos ----------
def pluck(freq, dur=1.2):
    n = int(dur * SR); t = t_arr(n)
    sig = np.zeros(n)
    for h in range(1, 7):
        sig += np.sin(2 * np.pi * freq * h * t) * (0.6 ** (h - 1)) * np.exp(-t * (2.5 + h * 1.6))
    return sig * env_ad(n, 0.004, 0.9)


def soft_bass(freq, dur):
    n = int(dur * SR); t = t_arr(n)
    sig = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * 2 * freq * t)
    e = np.minimum(1, t / 0.05) * np.exp(-t / (dur * 0.8))
    return sig * e


def pad(freqs, dur, attack=1.0, release=1.0):
    n = int(dur * SR); t = t_arr(n)
    sig = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate(freqs)) / len(freqs)
    e = np.minimum(1, t / attack) * np.minimum(1, (dur - t) / release)
    return sig * np.clip(e, 0, 1)


# ---------- música ----------
music = np.zeros(N)
BEAT = 60 / 92
BAR = 4 * BEAT
CHORDS = [  # C, Am, F, G (MIDI)
    (48, [60, 64, 67, 72]),
    (45, [57, 60, 64, 69]),
    (41, [53, 57, 60, 65]),
    (43, [55, 59, 62, 67]),
]
ARP = [0, 1, 2, 3, 2, 1, 2, 3]


def calm_section(t0, t1):
    bar = 0
    t = t0
    while t < t1 - 0.2:
        root, notes = CHORDS[bar % 4]
        place(music, t, soft_bass(midi(root), BAR * 0.95), 0.35)
        for k, idx in enumerate(ARP):
            tk = t + k * BEAT / 2
            if tk < t1 - 0.1:
                place(music, tk, pluck(midi(notes[idx] + 12) if k % 4 == 3 else midi(notes[idx])), 0.22)
        bar += 1
        t += BAR


calm_section(0.0, 16.2)
calm_section(25.0, 30.2)
# acorde final
place(music, 30.0, pad([midi(60), midi(64), midi(67), midi(72)], 4.0, attack=0.6, release=1.5), 0.35)
place(music, 30.0, pluck(midi(72), 3.0), 0.25)

# trecho tenso (episódio): drone grave com batimento + pulso + dissonância aguda leve
tension = np.zeros(N)
tt = t_arr(int(8.5 * SR))
drone = (np.sin(2 * np.pi * 73.4 * tt) + np.sin(2 * np.pi * 77.8 * tt)) * 0.5
trem = 0.6 + 0.4 * np.sin(2 * np.pi * 5 * tt)
hi = (np.sin(2 * np.pi * midi(75) * tt) + np.sin(2 * np.pi * midi(76) * tt)) * 0.12
shape = np.clip(np.minimum(tt / 0.8, (8.5 - tt) / 1.2), 0, 1)
place(tension, 15.6, (drone * trem + hi) * shape, 0.45)
for k in range(12):  # pulso tipo coração
    for off, g in ((0.0, 1.0), (0.22, 0.6)):
        n = int(0.25 * SR); t = t_arr(n)
        place(tension, 16.2 + k * 0.62 + off, np.sin(2 * np.pi * 55 * t) * np.exp(-t / 0.08), 0.5 * g)

# envelope geral da música: abaixa durante o episódio
mt = t_arr(N)
duck = np.ones(N)
duck[(mt > 15.6) & (mt < 25.0)] = 0.0
duck = smooth(duck, 600)
music = music * duck + tension

# ---------- efeitos ----------
sfx = np.zeros(N)


def click(gain=1.0, bright=1.0):
    n = int(0.03 * SR)
    x = rng.standard_normal(n) * env_ad(n, 0.0005, 0.006)
    x = x - smooth(x, 0.4 / bright)
    return x * gain


def wood(gain=1.0):
    n = int(0.12 * SR); t = t_arr(n)
    f = rng.uniform(700, 1100)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.025) + 0.4 * rng.standard_normal(n) * np.exp(-t / 0.008)
    return x * gain


def thud(gain=1.0, f=70):
    n = int(0.35 * SR); t = t_arr(n)
    x = np.sin(2 * np.pi * f * t * (1 - 0.3 * t)) * np.exp(-t / 0.09)
    x += smooth(rng.standard_normal(n), 2) * np.exp(-t / 0.03) * 0.6
    return x * gain


def whistle(gain=1.0):
    n = int(0.6 * SR); t = t_arr(n)
    x = (np.sin(2 * np.pi * 880 * t) + 0.7 * np.sin(2 * np.pi * 1108 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t))
    x += 0.15 * smooth(rng.standard_normal(n), 0.3)
    e = np.minimum(1, t / 0.04) * np.minimum(1, (0.6 - t) / 0.15)
    return x * e * gain


def shout(dur, f0=420.0, gain=1.0):
    """Vocal estilizado "aaah" por síntese aditiva com formantes."""
    n = int(dur * SR); t = t_arr(n)
    vib = 1 + 0.03 * np.sin(2 * np.pi * 6 * t) + 0.04 * np.sin(2 * np.pi * 1.3 * t)
    glide = 1 + 0.12 * np.exp(-t / 0.15) - 0.08 * (t / dur)
    phase = 2 * np.pi * np.cumsum(f0 * vib * glide) / SR
    sig = np.zeros(n)
    for h in range(1, 18):
        fh = f0 * h
        amp = np.exp(-((fh - 900) / 260) ** 2) + 0.6 * np.exp(-((fh - 1400) / 300) ** 2) + 0.25 * np.exp(-((fh - 2900) / 500) ** 2) + 0.08 / h
        sig += amp * np.sin(h * phase)
    sig += 0.05 * smooth(rng.standard_normal(n), 0.2)
    e = np.minimum(1, t / 0.06) * np.minimum(1, (dur - t) / 0.25)
    return sig / 3 * np.clip(e, 0, 1) * gain


# trenzinho andando (cliques de trilho) e apito
for t0, t1 in ((3.6, 9.6), (26.4, 30.2)):
    t = t0
    k = 0
    while t < t1:
        place(sfx, t, click(0.5 if k % 2 == 0 else 0.3), 0.3)
        t += 0.19 if k % 2 == 0 else 0.11
        k += 1
place(sfx, 5.0, whistle(), 0.18)
place(sfx, 27.4, whistle(), 0.16)
# guardar os trilhos (peças de madeira) e fechar a caixa
for k in range(9):
    place(sfx, 10.7 + k * 0.18 + rng.uniform(-0.03, 0.03), wood(), 0.35)
place(sfx, 12.65, thud(f=95), 0.6)
# episódio: grito estilizado e batidas no chão sincronizadas com os chutes
for st, du, f0, g in ((16.15, 1.5, 430, 0.55), (18.2, 1.7, 450, 0.6), (20.6, 1.4, 410, 0.5), (22.3, 0.9, 380, 0.35)):
    place(sfx, st, shout(du, f0), g)
w = 2.2
k = 0
t = 16.0 + 0.25 / w
while t < 23.5:
    place(sfx, t, thud(f=60 + 10 * (k % 2)), 0.45)
    t += 1 / (2 * w)
    k += 1
# devolver os trilhos (abre a caixa, peças, fecha)
place(sfx, 23.8, thud(f=95), 0.4)
for k in range(8):
    place(sfx, 24.1 + k * 0.17 + rng.uniform(-0.03, 0.03), wood(), 0.33)
place(sfx, 25.75, thud(f=95), 0.5)

# ---------- mixagem ----------
mix = music * 0.7 + sfx
fade = np.ones(N)
fade[: int(0.5 * SR)] = np.linspace(0, 1, int(0.5 * SR))
fade[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
mix *= fade
mix /= max(1e-9, np.max(np.abs(mix))) / 0.89
# estéreo leve: música um pouco mais larga
left = mix + 0.06 * smooth(music, 3)
right = mix - 0.06 * smooth(music, 3)
st = np.stack([left, right], axis=1)
st /= max(1e-9, np.max(np.abs(st))) / 0.89
pcm = (st * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes(pcm.tobytes())
print("ok", sys.argv[1])
