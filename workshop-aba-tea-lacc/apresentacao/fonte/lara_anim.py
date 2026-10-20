"""Animação ilustrada da vinheta fictícia da Lara (um episódio), no estilo da animação do Theo.

Uso: python3 lara_anim.py saida_muda.mp4 [--preview pasta]
"""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import animacao as A  # noqa: E402  (reusa fontes, cores e helpers)
from PIL import Image, ImageDraw  # noqa: E402

W, H, SS, FPS = A.W, A.H, A.SS, A.FPS
s, box, ease, line, font = A.s, A.box, A.ease, A.line, A.font
INK, PAPER, WOOD, WOOD_D = A.INK, A.PAPER, A.WOOD, A.WOOD_D

HOOD = (122, 90, 166)
HOOD_D = (98, 70, 140)
HAIR_L = (74, 46, 30)
SKIN_L = (232, 186, 150)
PANTS_L = (60, 70, 90)
BOARD = (52, 92, 76)
WALL = (240, 236, 226)
FLOOR = (214, 200, 178)

# colegas: (pele, cabelo, camiseta)
MATES = [((200, 150, 110), (40, 30, 25), (214, 120, 80)),
         ((240, 200, 170), (180, 130, 60), (90, 150, 200)),
         ((150, 100, 70), (30, 25, 20), (120, 170, 110))]
TEACH = ((225, 180, 145), (90, 60, 50), (70, 90, 130))


def classroom(d, board_text=None):
    d.rectangle(box(0, 0, W, 470), fill=WALL)
    d.rectangle(box(0, 470, W, H), fill=FLOOR)
    d.rectangle(box(0, 464, W, 474), fill=(200, 188, 166))
    d.rounded_rectangle(box(70, 90, 470, 300), radius=s(6), fill=BOARD, outline=WOOD_D, width=s(10))
    if board_text:
        f = font(30, "SemiBold")
        d.text((s(100), s(170)), board_text, font=f, fill=(236, 240, 232))
    # janela e porta
    d.rounded_rectangle(box(560, 90, 760, 260), radius=s(6), fill=(207, 227, 241), outline=(190, 176, 150), width=s(8))
    d.line(box(660, 90, 660, 260), fill=(190, 176, 150), width=s(6))
    d.rectangle(box(1110, 170, 1230, 470), fill=(176, 140, 100))
    d.ellipse(box(1120, 320, 1132, 332), fill=(230, 200, 120))


def desk(d, x, y=560, w=150):
    d.rectangle(box(x - w / 2, y - 14, x + w / 2, y), fill=WOOD)
    d.rectangle(box(x - w / 2 + 10, y, x - w / 2 + 20, y + 90), fill=WOOD_D)
    d.rectangle(box(x + w / 2 - 20, y, x + w / 2 - 10, y + 90), fill=WOOD_D)


def person(d, cx, base, skin, hair, shirt, long_hair=False, hood=0.0, head_down=0.0, mouth="smile",
           eye_dx=0.0, eyes_closed=False, talk=False, hand_y=None):
    """Pessoa sentada atrás da carteira (só tronco e cabeça). hood/head_down em 0..1."""
    hy = base - 150 + 14 * head_down
    if long_hair:
        d.rounded_rectangle(box(cx - 40, hy - 20, cx + 40, hy + 62), radius=s(26), fill=hair)
    d.rounded_rectangle(box(cx - 46, base - 118, cx + 46, base), radius=s(22), fill=shirt)
    if hood > 0:  # capuz atrás da cabeça
        d.ellipse(box(cx - 44, hy - 44, cx + 44, hy + 40), fill=HOOD_D)
    d.ellipse(box(cx - 33, hy - 33, cx + 33, hy + 33), fill=skin)
    d.pieslice(box(cx - 36, hy - 40, cx + 36, hy + 26), 180, 360, fill=hair)
    if hood > 0:  # capuz cobrindo o alto da cabeça
        g = 8 * hood
        d.pieslice(box(cx - 36 - g, hy - 40 - g, cx + 36 + g, hy + 26 + g), 180, 360, fill=HOOD)
    if eyes_closed or head_down > 0.6:
        d.arc(box(cx - 15, hy - 2, cx - 5, hy + 6), 20, 160, fill=INK, width=s(3))
        d.arc(box(cx + 5, hy - 2, cx + 15, hy + 6), 20, 160, fill=INK, width=s(3))
    else:
        d.ellipse(box(cx - 13 + eye_dx, hy - 2, cx - 7 + eye_dx, hy + 5), fill=INK)
        d.ellipse(box(cx + 7 + eye_dx, hy - 2, cx + 13 + eye_dx, hy + 5), fill=INK)
    if talk:
        d.ellipse(box(cx - 7, hy + 12, cx + 7, hy + 22), fill=(150, 70, 60))
    elif mouth == "smile":
        d.arc(box(cx - 10, hy + 8, cx + 10, hy + 20), 20, 160, fill=INK, width=s(3))
    elif mouth == "flat":
        d.line(box(cx - 7, hy + 16, cx + 7, hy + 16), fill=INK, width=s(3))
    elif mouth == "laugh":
        d.chord(box(cx - 11, hy + 8, cx + 11, hy + 24), 0, 180, fill=(150, 70, 60))
    hy2 = hand_y if hand_y is not None else base - 12
    line(d, (cx - 40, base - 100), (cx - 30, hy2), shirt, 18)
    line(d, (cx + 40, base - 100), (cx + 30, hy2), shirt, 18)
    d.ellipse(box(cx - 40, hy2 - 10, cx - 20, hy2 + 10), fill=skin)
    d.ellipse(box(cx + 20, hy2 - 10, cx + 40, hy2 + 10), fill=skin)


def teacher(d, talk=False):
    line(d, (182, 465), (178, 640), (60, 60, 75), 26)
    line(d, (218, 465), (222, 640), (60, 60, 75), 26)
    d.ellipse(box(160, 630, 196, 652), fill=INK)
    d.ellipse(box(204, 630, 240, 652), fill=INK)
    person(d, 200, 470, *TEACH, talk=talk)


def lara_walking(d, cx, base, t):
    """Lara de pé, de capuz, andando (vista lateral simplificada)."""
    sw = math.sin(t * 2 * math.pi * 1.6)
    line(d, (cx, base - 60), (cx - 16 * sw, base), PANTS_L, 22)
    line(d, (cx, base - 60), (cx + 16 * sw, base), PANTS_L, 22)
    d.rounded_rectangle(box(cx - 40, base - 180, cx + 40, base - 52), radius=s(22), fill=HOOD)
    hy = base - 212
    d.ellipse(box(cx - 44, hy - 44, cx + 44, hy + 40), fill=HOOD_D)
    d.ellipse(box(cx - 32, hy - 32, cx + 32, hy + 32), fill=SKIN_L)
    d.pieslice(box(cx - 42, hy - 46, cx + 42, hy + 36), 180, 360, fill=HOOD)
    d.arc(box(cx - 4, hy - 2, cx + 6, hy + 6), 20, 160, fill=INK, width=s(3))
    d.arc(box(cx + 12, hy - 2, cx + 22, hy + 6), 20, 160, fill=INK, width=s(3))
    d.line(box(cx + 4, hy + 16, cx + 16, hy + 16), fill=INK, width=s(3))
    line(d, (cx, base - 160), (cx + 10 - 12 * sw, base - 80), HOOD, 18)


def bubble(d, text, x, y, size=24):
    f = font(size, "SemiBold")
    tw = d.textlength(text, font=f) / SS
    d.rounded_rectangle(box(x, y, x + tw + 36, y + 54), radius=s(18), fill=PAPER, outline=(190, 196, 205), width=s(2))
    d.polygon([(s(x + 26), s(y + 54)), (s(x + 48), s(y + 54)), (s(x + 20), s(y + 74))], fill=PAPER)
    d.text((s(x + 18), s(y + 12)), text, font=f, fill=INK)


def noise_lines(d, cx, cy, t, n=3, color=(180, 120, 90)):
    for i in range(n):
        r = 30 + i * 16
        if (math.sin(t * 9 - i) + 1) / 2 > 0.3:
            d.arc(box(cx - r, cy - r, cx + r, cy + r), 300, 350, fill=color, width=s(4))
            d.arc(box(cx - r, cy - r, cx + r, cy + r), 190, 240, fill=color, width=s(4))


def label(d):
    A.label(d)


def drawing_on_desk(d, x, y=546):
    d.rectangle(box(x - 34, y - 8, x + 34, y), fill=PAPER)
    d.line(box(x - 20, y - 5, x + 18, y - 5), fill=(90, 120, 200), width=s(2))
    d.ellipse(box(x + 6, y - 7, x + 14, y - 1), fill=(240, 200, 80))


def frame(scene_fn, t):
    img = Image.new("RGB", (W * SS, H * SS))
    d = ImageDraw.Draw(img)
    scene_fn(d, t)
    label(d)
    return img


LX = 380  # Lara na sala


def scene_calm(d, t):
    classroom(d)
    teacher(d)
    for x, (sk, hr, sh) in zip((680, 880), MATES[:2]):
        person(d, x, 548, sk, hr, sh)
        desk(d, x)
    person(d, LX, 548, SKIN_L, HAIR_L, HOOD, long_hair=True, eye_dx=0, hand_y=540)
    desk(d, LX)
    drawing_on_desk(d, LX)


def scene_group(d, t):
    classroom(d, board_text="Trabalho em grupo" if t > 0.6 else None)
    talk_t = t > 1.2
    teacher(d, talk=t < 1.4 and int(t * 6) % 2 == 0)
    if t < 1.6:
        bubble(d, "Agora, trabalho em grupo!", 230, 250)
    k = ease((t - 1.0) / 1.4)  # colegas se aproximam
    xs = [680 - 140 * k, 880 - 200 * k, 1020 - 180 * k]
    for i, (x, (sk, hr, sh)) in enumerate(zip(xs, MATES)):
        if i == 2 and k < 0.05:
            continue
        mouth = "laugh" if (i == 1 and talk_t and int(t * 3) % 3 == 0) else "smile"
        person(d, x, 548, sk, hr, sh, talk=talk_t and (int(t * 5 + i) % 2 == 0), mouth=mouth)
        if talk_t:
            noise_lines(d, x, 370, t + i)
    desk(d, (LX + xs[0]) / 2 + 40, w=360 + 300 * k)
    person(d, LX, 548, SKIN_L, HAIR_L, HOOD, long_hair=True, mouth="flat" if t > 2 else "smile",
           eye_dx=3 * math.sin(t * 5) if t > 2 else 0, hand_y=540)
    desk(d, LX)
    drawing_on_desk(d, LX)
    if talk_t:
        for i, (bx, by) in enumerate(((560, 300), (760, 280), (880, 320))):
            if int(t * 2 + i) % 2 == 0:
                bubble(d, "…", bx, by, 22)


def scene_leave(d, t):
    classroom(d, board_text="Trabalho em grupo")
    teacher(d)
    xs = [540, 680, 840]
    for i, (x, (sk, hr, sh)) in enumerate(zip(xs, MATES)):
        looking = t > 4.2 and i == 0
        person(d, x, 548, sk, hr, sh, talk=(not looking) and int(t * 5 + i) % 2 == 0,
               eye_dx=-4 if looking else 0)
        if not looking:
            noise_lines(d, x, 370, t + i)
    desk(d, 640, w=660)
    if t < 3.6:
        hood = ease(t / 1.2)
        down = ease((t - 1.4) / 1.2)
        person(d, LX, 548, SKIN_L, HAIR_L, HOOD, long_hair=hood < 0.5, hood=hood, head_down=down,
               mouth="flat", hand_y=540)
        desk(d, LX)
        drawing_on_desk(d, LX)
    else:
        desk(d, LX)
        drawing_on_desk(d, LX)
        u = ease((t - 3.6) / 2.6)
        x = LX + (1170 - LX) * u
        if x < 1160:
            lara_walking(d, x, 650, t)
        if t > 4.4:
            bubble(d, "?", 500, 300, 26)


def library(d):
    d.rectangle(box(0, 0, W, 470), fill=(236, 230, 214))
    d.rectangle(box(0, 470, W, H), fill=(200, 180, 150))
    colors = [(180, 90, 80), (90, 120, 170), (200, 170, 90), (110, 150, 110), (150, 110, 160)]
    for sx in (60, 420, 900):
        d.rectangle(box(sx, 80, sx + 300, 440), fill=(150, 110, 70))
        for row in range(4):
            y = 100 + row * 86
            d.rectangle(box(sx + 10, y + 70, sx + 290, y + 78), fill=(120, 85, 55))
            for k in range(12):
                c = colors[(k + row * 3 + sx) % len(colors)]
                h = 50 + (k * 7 + row * 5) % 18
                d.rectangle(box(sx + 16 + k * 22, y + 70 - h, sx + 34 + k * 22, y + 70), fill=c)
    f = font(26, "SemiBold")
    d.text((s(560), s(30)), "Biblioteca", font=f, fill=(120, 90, 60))


def scene_library(d, t):
    library(d)
    person(d, 640, 568, SKIN_L, HAIR_L, HOOD, long_hair=True, mouth="smile", hand_y=560, eyes_closed=t < 0.8)
    d.rectangle(box(500, 566, 780, 582), fill=WOOD)
    d.rectangle(box(515, 582, 527, 680), fill=WOOD_D)
    d.rectangle(box(753, 582, 765, 680), fill=WOOD_D)
    drawing_on_desk(d, 640, 564)


TITLE = A.card([
    ("Lara: uma aula", 64, "Bold", (247, 246, 242)),
    ("Observem: o que acontece antes · o que ela faz · o que acontece depois", 28, "Regular", (201, 211, 222)),
    ("", 20, "Regular", (0, 0, 0)),
    ("Animação · exemplo fictício · não representa uma pessoa real", 24, "SemiBold", (232, 180, 143)),
])
END = A.card([
    ("Isto foi um episódio.", 56, "Bold", (247, 246, 242)),
    ("O que a escola registrou nos últimos dois meses está na história a seguir.", 30, "Regular", (201, 211, 222)),
    ("", 20, "Regular", (0, 0, 0)),
    ("Animação · exemplo fictício · não representa uma pessoa real", 24, "SemiBold", (232, 180, 143)),
])

TIMELINE = [
    (3.5, lambda t: TITLE),
    (5.0, lambda t: frame(scene_calm, t)),
    (7.0, lambda t: frame(scene_group, t)),
    (7.5, lambda t: frame(scene_leave, t)),
    (5.0, lambda t: frame(scene_library, t)),
    (4.0, lambda t: END),
]
FADE = 0.5


def frame_at(T):
    acc = 0.0
    for i, (dur, fn) in enumerate(TIMELINE):
        if T < acc + dur or i == len(TIMELINE) - 1:
            t = T - acc
            img = fn(t)
            if i + 1 < len(TIMELINE) and t > dur - FADE:
                img = Image.blend(img, TIMELINE[i + 1][1](0.0), (t - (dur - FADE)) / FADE)
            return img.resize((W, H), Image.LANCZOS)
        acc += dur


def main():
    out = sys.argv[1]
    total = sum(dd for dd, _ in TIMELINE)
    if "--preview" in sys.argv:
        folder = sys.argv[sys.argv.index("--preview") + 1]
        for T in (2.0, 6.0, 9.0, 12.5, 16.5, 19.0, 22.0, 25.0, 28.0, 31.0):
            frame_at(T).save(f"{folder}/l_{T:05.1f}.png")
        return
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                             "-crf", "20", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        proc.stdin.write(frame_at(i / FPS).tobytes())
    proc.stdin.close()
    proc.wait()
    print("ok", total, "s")


if __name__ == "__main__":
    main()
