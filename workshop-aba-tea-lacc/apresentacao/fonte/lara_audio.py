"""Trilha e efeitos sintetizados para a animação da Lara (32 s). Tudo gerado com numpy.

Linha do tempo (s): título 0–3,5 · sala calma 3,5–8,5 · trabalho em grupo 8,5–15,5 ·
capuz e saída 15,5–23 · biblioteca 23–28 · final 28–32.
Uso: python3 lara_audio.py saida.wav
"""
import sys
import wave

import numpy as np

SR = 44100
DUR = 32.0
N = int(SR * DUR)
rng = np.random.default_rng(11)


def t_arr(n):
    return np.arange(n) / SR


def place(buf, start, sig, gain=1.0):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf):
        buf[i:j] += sig[: j - i] * gain


def smooth(x, ms):
    k = max(1, int(SR * ms / 1000))
    return np.convolve(x, np.ones(k) / k, mode="same")


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pluck(freq, dur=1.2):
    n = int(dur * SR); t = t_arr(n)
    sig = sum(np.sin(2 * np.pi * freq * h * t) * (0.6 ** (h - 1)) * np.exp(-t * (2.5 + h * 1.6)) for h in range(1, 7))
    e = np.exp(-t / 0.9); e[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    return sig * e


def soft_bass(freq, dur):
    n = int(dur * SR); t = t_arr(n)
    return (np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t)) * np.minimum(1, t / 0.05) * np.exp(-t / (dur * 0.8))


def pad(freqs, dur, attack=1.0, release=1.0):
    n = int(dur * SR); t = t_arr(n)
    sig = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate(freqs)) / len(freqs)
    return sig * np.clip(np.minimum(t / attack, (dur - t) / release), 0, 1)


def syllable(f0, dur, vowel, gain=1.0):
    """Sílaba de 'fala' estilizada (síntese aditiva com formantes de vogal)."""
    F = {"a": (800, 1250), "e": (500, 1800), "i": (300, 2200), "o": (500, 900), "u": (350, 800)}[vowel]
    n = int(dur * SR); t = t_arr(n)
    f = f0 * (1 + 0.06 * np.sin(2 * np.pi * rng.uniform(2, 5) * t) + rng.uniform(-0.08, 0.08) * t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    sig = np.zeros(n)
    for h in range(1, 16):
        fh = f0 * h
        amp = np.exp(-((fh - F[0]) / 200) ** 2) + 0.6 * np.exp(-((fh - F[1]) / 260) ** 2) + 0.05 / h
        sig += amp * np.sin(h * ph)
    e = np.clip(np.minimum(t / 0.02, (dur - t) / 0.05), 0, 1)
    return sig / 3 * e * gain


def babble(t0, t1, f0_range, density, gain):
    out = np.zeros(N)
    t = t0
    while t < t1:
        place(out, t, syllable(rng.uniform(*f0_range), rng.uniform(0.09, 0.2), rng.choice(list("aeiou"))), gain)
        t += rng.uniform(0.08, 0.22) / density
        if rng.random() < 0.12:
            t += rng.uniform(0.2, 0.5)
    return out


def laugh(t0, f0, gain):
    for k in range(5):
        place(sfx, t0 + k * 0.16, syllable(f0 * (1 - 0.04 * k), 0.11, "a"), gain * (1 - 0.12 * k))


def thud(f=70, dur=0.35):
    n = int(dur * SR); t = t_arr(n)
    return np.sin(2 * np.pi * f * t * (1 - 0.3 * t)) * np.exp(-t / 0.09) + smooth(rng.standard_normal(n), 2) * np.exp(-t / 0.03) * 0.6


def step():
    n = int(0.12 * SR); t = t_arr(n)
    return smooth(rng.standard_normal(n), 0.6) * np.exp(-t / 0.02) + 0.5 * np.sin(2 * np.pi * 110 * t) * np.exp(-t / 0.03)


def scrape(dur=0.6):
    n = int(dur * SR); t = t_arr(n)
    x = smooth(rng.standard_normal(n), 0.25) * (0.6 + 0.4 * np.sin(2 * np.pi * 37 * t))
    x += 0.3 * np.sin(2 * np.pi * (140 + 60 * t) * t)
    return x * np.clip(np.minimum(t / 0.05, (dur - t) / 0.1), 0, 1)


def creak(dur=0.5):
    n = int(dur * SR); t = t_arr(n)
    f = 320 + 260 * t / dur
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * t))
    return x * np.clip(np.minimum(t / 0.05, (dur - t) / 0.1), 0, 1)


def pencil(dur=0.35):
    n = int(dur * SR); t = t_arr(n)
    x = rng.standard_normal(n) - smooth(rng.standard_normal(n), 0.3)
    return x * (0.5 + 0.5 * np.sin(2 * np.pi * 6 * t)) * np.clip(np.minimum(t / 0.03, (dur - t) / 0.05), 0, 1)


# ---------- música ----------
music = np.zeros(N)
BEAT = 60 / 88
BAR = 4 * BEAT
CHORDS = [(50, [62, 65, 69, 74]), (46, [58, 62, 65, 70]), (48, [60, 64, 67, 72]), (45, [57, 60, 64, 69])]  # Dm Bb C Am
ARP = [0, 1, 2, 3, 2, 1, 2, 3]


def calm(t0, t1, gain=0.22):
    bar, t = 0, t0
    while t < t1 - 0.2:
        root, notes = CHORDS[bar % 4]
        place(music, t, soft_bass(midi(root), BAR * 0.95), 0.32)
        for k, idx in enumerate(ARP):
            if t + k * BEAT / 2 < t1 - 0.1:
                place(music, t + k * BEAT / 2, pluck(midi(notes[idx])), gain)
        bar += 1
        t += BAR


calm(0.0, 10.0)
calm(23.2, 28.4, 0.18)
place(music, 28.0, pad([midi(62), midi(65), midi(69), midi(74)], 4.0, 0.6, 1.5), 0.32)
mt = t_arr(N)
duck = np.ones(N); duck[(mt > 9.4) & (mt < 23.2)] = 0.0
music *= smooth(duck, 700)
# tensão: pad que sobe e pulsação leve durante o barulho e a saída
tt = t_arr(int(13.5 * SR))
rise = np.sin(2 * np.pi * (220 + 40 * tt / 13.5) * tt) + np.sin(2 * np.pi * (233 + 40 * tt / 13.5) * tt)
shape = np.clip(np.minimum(tt / 1.5, (13.5 - tt) / 1.5), 0, 1) * (0.4 + 0.6 * tt / 13.5)
place(music, 9.4, rise * 0.5 * shape, 0.35)
for k in range(18):
    n = int(0.25 * SR); t = t_arr(n)
    place(music, 10.5 + k * 0.66, np.sin(2 * np.pi * 55 * t) * np.exp(-t / 0.08), 0.4)

# ---------- efeitos e vozes ----------
sfx = np.zeros(N)
for k in range(4):  # lápis desenhando na sala calma
    place(sfx, 4.2 + k * 1.1, pencil(), 0.12)
place(sfx, 8.6, babble(0, 1.3, (190, 230), 1.0, 1.0)[: int(1.3 * SR)], 0.35)  # professora (fala estilizada)
crowd = babble(9.8, 22.6, (180, 320), 2.6, 1.0)
ramp = np.clip((mt - 9.8) / 2.0, 0, 1) * np.clip((22.8 - mt) / 0.6, 0, 1)
sfx += crowd * ramp * 0.42
for t0 in (10.6, 11.4, 12.6):  # mesas sendo arrastadas
    place(sfx, t0, scrape(0.45), 0.18)
laugh(11.9, 330, 0.5)
laugh(14.2, 290, 0.45)
laugh(17.3, 340, 0.4)
n = int(0.5 * SR); t = t_arr(n)
place(sfx, 15.7, smooth(rng.standard_normal(n), 1.2) * np.exp(-t / 0.2), 0.25)  # capuz (tecido)
place(sfx, 19.1, scrape(0.55), 0.3)  # cadeira
for k in range(8):  # passos até a porta
    place(sfx, 19.5 + k * 0.32, step(), 0.4)
place(sfx, 22.0, creak(0.45), 0.12)
place(sfx, 22.5, thud(90), 0.45)  # porta fecha
for k in range(4):  # biblioteca: lápis
    place(sfx, 24.0 + k * 0.9, pencil(0.4), 0.12)

mix = music * 0.75 + sfx
fade = np.ones(N)
fade[: int(0.5 * SR)] = np.linspace(0, 1, int(0.5 * SR))
fade[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR))
mix *= fade
mix /= np.max(np.abs(mix)) / 0.89
st = np.stack([mix + 0.05 * smooth(music, 3), mix - 0.05 * smooth(music, 3)], axis=1)
st /= np.max(np.abs(st)) / 0.89
with wave.open(sys.argv[1], "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((st * 32767).astype("<i2").tobytes())
print("ok")
