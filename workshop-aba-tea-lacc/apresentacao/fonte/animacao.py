"""Animação simples e ilustrada da vinheta fictícia do Theo (um episódio).

Gera quadros com PIL e envia ao ffmpeg (H.264, compatível com iPad).
Uso: python3 animacao.py saida.mp4 [--preview pasta]
"""
import math
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
SS = 2  # supersampling
FPS = 24
FONT_DIR = "/usr/share/fonts/opentype/inter/"


def font(size, weight="Regular"):
    return ImageFont.truetype(FONT_DIR + f"Inter-{weight}.otf", int(size * SS))


# ---------- paleta ----------
WALL = (243, 239, 230)
FLOOR = (226, 214, 195)
RUG = (184, 212, 200)
WOOD = (200, 159, 110)
WOOD_D = (160, 120, 78)
SKIN_C = (214, 160, 120)
SKIN_T = (227, 180, 143)
HAIR_C = (107, 66, 38)
HAIR_T = (46, 42, 40)
SHIRT = (74, 132, 196)
PANTS = (59, 74, 107)
CARDIGAN = (94, 140, 97)
KHAKI = (140, 123, 107)
INK = (31, 42, 55)
RED = (200, 70, 61)
BOX = (176, 125, 79)
BOX_D = (140, 96, 58)
PAPER = (252, 251, 247)


def s(v):
    return int(round(v * SS))


def box(x0, y0, x1, y1):
    return [s(x0), s(y0), s(x1), s(y1)]


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def line(d, p0, p1, color, width):
    d.line([s(p0[0]), s(p0[1]), s(p1[0]), s(p1[1])], fill=color, width=s(width))
    r = width / 2
    for (x, y) in (p0, p1):
        d.ellipse(box(x - r, y - r, x + r, y + r), fill=color)


# ---------- cenário ----------
def background(d):
    d.rectangle(box(0, 0, W, 430), fill=WALL)
    d.rectangle(box(0, 430, W, H), fill=FLOOR)
    d.rectangle(box(0, 424, W, 434), fill=(214, 204, 186))
    # janela
    d.rounded_rectangle(box(80, 80, 300, 260), radius=s(8), fill=(207, 227, 241), outline=(190, 176, 150), width=s(8))
    d.line(box(190, 80, 190, 260), fill=(190, 176, 150), width=s(6))
    d.line(box(80, 170, 300, 170), fill=(190, 176, 150), width=s(6))
    # prateleira com caixas
    d.rectangle(box(420, 200, 640, 212), fill=WOOD_D)
    d.rounded_rectangle(box(435, 150, 495, 200), radius=s(6), fill=(230, 196, 120))
    d.rounded_rectangle(box(505, 160, 560, 200), radius=s(6), fill=(158, 196, 221))
    d.rounded_rectangle(box(570, 140, 625, 200), radius=s(6), fill=(214, 150, 140))
    # tapete
    d.ellipse(box(170, 560, 780, 715), fill=RUG)
    # mesa com folha
    d.rectangle(box(950, 430, 1190, 448), fill=WOOD)
    d.rectangle(box(965, 448, 980, 560), fill=WOOD_D)
    d.rectangle(box(1160, 448, 1175, 560), fill=WOOD_D)
    d.polygon([(s(1030), s(430)), (s(1110), s(430)), (s(1100), s(418)), (s(1040), s(418))], fill=PAPER)
    for k in range(3):
        d.line(box(1048, 421 + k * 3, 1092, 421 + k * 3), fill=(180, 180, 190), width=s(1))
    # cadeirinha
    d.rectangle(box(1040, 470, 1110, 482), fill=(158, 196, 221))
    d.rectangle(box(1045, 482, 1055, 560), fill=(120, 160, 190))
    d.rectangle(box(1095, 482, 1105, 560), fill=(120, 160, 190))
    d.rectangle(box(1040, 400, 1052, 470), fill=(120, 160, 190))


def toy_box(d, open_lid):
    x, y = 820, 610
    d.rounded_rectangle(box(x - 60, y - 40, x + 60, y + 30), radius=s(6), fill=BOX)
    d.rectangle(box(x - 60, y - 10, x + 60, y - 4), fill=BOX_D)
    if open_lid:
        d.polygon([(s(x - 60), s(y - 40)), (s(x + 60), s(y - 40)), (s(x + 70), s(y - 75)), (s(x - 50), s(y - 75))], fill=BOX_D)
    else:
        d.rounded_rectangle(box(x - 64, y - 48, x + 64, y - 38), radius=s(4), fill=BOX_D)


def tracks(d, cx, cy, k, train_angle, show_train=True):
    if k <= 0.02:
        return
    rx, ry = 150 * k, 40 * k
    d.ellipse(box(cx - rx, cy - ry, cx + rx, cy + ry), outline=WOOD, width=s(12 * k + 1))
    for i in range(28):
        a = 2 * math.pi * i / 28
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        nx, ny = math.cos(a) * 9 * k, math.sin(a) * 9 * k
        d.line(box(x - nx, y - ny, x + nx, y + ny), fill=WOOD_D, width=s(3 * k + 1))
    if show_train:
        x, y = cx + rx * math.cos(train_angle), cy + ry * math.sin(train_angle)
        w, h = 36 * k, 22 * k
        d.rounded_rectangle(box(x - w / 2, y - h, x + w / 2, y), radius=s(4 * k), fill=RED)
        d.rectangle(box(x + w * 0.05, y - h * 1.5, x + w * 0.45, y - h), fill=(150, 45, 40))
        for wx in (-w * 0.3, w * 0.3):
            d.ellipse(box(x + wx - 5 * k, y - 4 * k, x + wx + 5 * k, y + 6 * k), fill=INK)


# ---------- personagens ----------
def therapist(d, cx, base, arm="rest", talk=False, target=None):
    d.ellipse(box(cx - 72, base - 32, cx + 72, base + 10), fill=KHAKI)
    d.rounded_rectangle(box(cx - 50, base - 150, cx + 50, base - 22), radius=s(24), fill=CARDIGAN)
    d.rectangle(box(cx - 13, base - 148, cx + 13, base - 24), fill=(236, 230, 214))
    hx, hy = cx, base - 188
    d.ellipse(box(cx + 26, hy - 30, cx + 60, hy + 4), fill=HAIR_T)  # rabo de cavalo
    d.ellipse(box(hx - 38, hy - 38, hx + 38, hy + 38), fill=SKIN_T)
    d.pieslice(box(hx - 41, hy - 43, hx + 41, hy + 30), 180, 360, fill=HAIR_T)
    d.ellipse(box(hx - 15, hy - 2, hx - 8, hy + 5), fill=INK)
    d.ellipse(box(hx + 8, hy - 2, hx + 15, hy + 5), fill=INK)
    if talk:
        d.ellipse(box(hx - 8, hy + 14, hx + 8, hy + 24), fill=(150, 70, 60))
    else:
        d.arc(box(hx - 11, hy + 8, hx + 11, hy + 22), 20, 160, fill=INK, width=s(3))
    use_left = target is not None and arm != "rest" and target[0] < cx
    use_right = target is not None and arm != "rest" and not use_left
    for side, active in ((-1, use_left), (1, use_right)):
        sx, sy = cx + 46 * side, base - 132
        if active:
            tx, ty = target
            line(d, (sx, sy), (tx, ty), CARDIGAN, 22)
            d.ellipse(box(tx - 11, ty - 11, tx + 11, ty + 11), fill=SKIN_T)
        else:
            line(d, (sx, base - 135), (cx + 50 * side, base - 45), CARDIGAN, 22)
            d.ellipse(box(cx + 50 * side - 10, base - 56, cx + 50 * side + 10, base - 36), fill=SKIN_T)


def child_sitting(d, cx, base, look=0, smile=True):
    d.ellipse(box(cx - 66, base - 30, cx + 66, base + 10), fill=PANTS)
    d.rounded_rectangle(box(cx - 42, base - 122, cx + 42, base - 20), radius=s(20), fill=SHIRT)
    hx, hy = cx, base - 156
    d.ellipse(box(hx - 35, hy - 35, hx + 35, hy + 35), fill=SKIN_C)
    d.pieslice(box(hx - 38, hy - 42, hx + 38, hy + 28), 180, 360, fill=HAIR_C)
    d.polygon([(s(hx - 36), s(hy - 8)), (s(hx - 10), s(hy - 14)), (s(hx - 30), s(hy - 26))], fill=HAIR_C)
    ex = look * 4
    d.ellipse(box(hx - 14 + ex, hy, hx - 7 + ex, hy + 7), fill=INK)
    d.ellipse(box(hx + 7 + ex, hy, hx + 14 + ex, hy + 7), fill=INK)
    if smile:
        d.arc(box(hx - 10, hy + 8, hx + 10, hy + 22), 20, 160, fill=INK, width=s(3))
    else:
        d.line(box(hx - 7, hy + 17, hx + 7, hy + 17), fill=INK, width=s(3))
    line(d, (cx - 38, base - 108), (cx - 58, base - 32), SHIRT, 18)
    d.ellipse(box(cx - 68, base - 42, cx - 48, base - 22), fill=SKIN_C)
    line(d, (cx + 38, base - 108), (cx + 62, base - 36), SHIRT, 18)
    d.ellipse(box(cx + 52, base - 46, cx + 72, base - 26), fill=SKIN_C)


def child_lying(d, t, kicking=True):
    hx, hy = 300, 618
    w = 2 * math.pi * 2.2
    a1 = -18 + (26 * math.sin(w * t) if kicking else 0)
    a2 = -18 + (26 * math.sin(w * t + math.pi) if kicking else 4)
    for ang, yy in ((a1, 608), (a2, 630)):
        rad = math.radians(ang)
        hip = (440, yy)
        knee = (hip[0] + 55 * math.cos(rad), hip[1] + 55 * math.sin(rad))
        foot = (knee[0] + 50 * math.cos(rad * 0.4), knee[1] + 50 * math.sin(rad * 0.4))
        line(d, hip, knee, PANTS, 24)
        line(d, knee, foot, PANTS, 22)
        d.ellipse(box(foot[0] - 13, foot[1] - 11, foot[0] + 15, foot[1] + 11), fill=INK)
    d.rounded_rectangle(box(330, 596, 450, 642), radius=s(20), fill=SHIRT)
    arm_osc = 10 * math.sin(w * t * 0.8) if kicking else 0
    line(d, (350, 600), (372, 560 + arm_osc), SHIRT, 18)
    d.ellipse(box(362, 548 + arm_osc, 384, 570 + arm_osc), fill=SKIN_C)
    line(d, (350, 640), (380, 668), SHIRT, 18)
    d.ellipse(box(372, 660, 392, 680), fill=SKIN_C)
    d.ellipse(box(hx - 35, hy - 35, hx + 35, hy + 35), fill=SKIN_C)
    d.pieslice(box(hx - 42, hy - 38, hx + 28, hy + 38), 90, 270, fill=HAIR_C)
    if kicking:
        d.arc(box(hx + 2, hy - 18, hx + 14, hy - 8), 180, 360, fill=INK, width=s(3))
        d.arc(box(hx + 2, hy + 8, hx + 14, hy + 18), 180, 360, fill=INK, width=s(3))
        d.ellipse(box(hx + 16, hy - 9, hx + 30, hy + 9), fill=(150, 70, 60))
        for i in range(3):
            r = 52 + i * 16
            alpha_on = (math.sin(w * t * 0.9 - i) + 1) / 2 > 0.35
            if alpha_on:
                d.arc(box(hx - r, hy - r, hx + r, hy + r), 300, 345, fill=(170, 120, 90), width=s(4))
    else:
        d.ellipse(box(hx + 4, hy - 14, hx + 11, hy - 7), fill=INK)
        d.ellipse(box(hx + 4, hy + 7, hx + 11, hy + 14), fill=INK)
        d.line(box(hx + 22, hy - 6, hx + 22, hy + 6), fill=INK, width=s(3))


def bubble(d, text, x, y, alpha_on=True):
    if not alpha_on:
        return
    f = font(24, "SemiBold")
    tw = d.textlength(text, font=f) / SS
    pad = 18
    d.rounded_rectangle(box(x, y, x + tw + 2 * pad, y + 56), radius=s(18), fill=PAPER, outline=(190, 196, 205), width=s(2))
    d.polygon([(s(x + 30), s(y + 56)), (s(x + 54), s(y + 56)), (s(x + 24), s(y + 78))], fill=PAPER)
    d.text((s(x + pad), s(y + 13)), text, font=f, fill=INK)


def label(d):
    f = font(18, "SemiBold")
    txt = "Animação · exemplo fictício"
    tw = d.textlength(txt, font=f) / SS
    d.rounded_rectangle(box(24, 22, 24 + tw + 28, 56), radius=s(17), fill=(31, 42, 55))
    d.text((s(38), s(29)), txt, font=f, fill=(247, 246, 242))


# ---------- cenas ----------
TRACK_C = (470, 662)
BOX_C = (820, 600)


def scene_play(t):
    img = Image.new("RGB", (W * SS, H * SS)); d = ImageDraw.Draw(img)
    background(d); toy_box(d, open_lid=False)
    child_sitting(d, 420, 600, look=0.6)
    therapist(d, 680, 600)
    tracks(d, *TRACK_C, 1.0, t * 1.4)
    label(d)
    return img


def scene_remove(t):
    img = Image.new("RGB", (W * SS, H * SS)); d = ImageDraw.Draw(img)
    background(d)
    k = 1 - ease((t - 1.2) / 1.6)
    cx = TRACK_C[0] + (BOX_C[0] - TRACK_C[0]) * (1 - k)
    cy = TRACK_C[1] + (BOX_C[1] - TRACK_C[1]) * (1 - k)
    toy_box(d, open_lid=0.8 < t < 3.2)
    look = 1 if t > 1.0 else 0.6
    child_sitting(d, 420, 600, look=look, smile=t < 1.2)
    if t < 3.0:
        tgt = (cx + 40, cy - 10) if 0.8 < t else None
        therapist(d, 680, 600, arm="reach" if tgt else "rest", target=tgt, talk=False)
    else:
        therapist(d, 680, 600, arm="point", target=(840, 400), talk=3.4 < t < 5.6 and int(t * 6) % 2 == 0)
    tracks(d, cx, cy, k, 4.2, show_train=k > 0.3)
    bubble(d, "Agora acabou. Vamos para a mesa.", 640, 300, alpha_on=t > 3.3)
    label(d)
    return img


def scene_behavior(t):
    img = Image.new("RGB", (W * SS, H * SS)); d = ImageDraw.Draw(img)
    background(d); toy_box(d, open_lid=False)
    therapist(d, 700, 600)
    child_lying(d, t, kicking=True)
    label(d)
    return img


def scene_return(t):
    def render(child_mode):
        img = Image.new("RGB", (W * SS, H * SS)); d = ImageDraw.Draw(img)
        background(d)
        k = ease((t - 0.8) / 1.6)
        cx = BOX_C[0] + (TRACK_C[0] - BOX_C[0]) * k
        cy = BOX_C[1] + (TRACK_C[1] - BOX_C[1]) * k
        toy_box(d, open_lid=0.4 < t < 2.6)
        reaching = 0.6 < t < 2.6
        therapist(d, 700, 600, arm="reach" if reaching else "rest", target=(cx + 60, cy - 6) if reaching else None)
        if child_mode == "lying":
            child_lying(d, t, kicking=False)
        else:
            child_sitting(d, 420, 600, look=0.6)
        tracks(d, cx, cy, k, t * 1.4, show_train=k > 0.6)
        label(d)
        return img
    if t < 2.4:
        return render("lying")
    if t > 3.0:
        return render("sitting")
    return Image.blend(render("lying"), render("sitting"), (t - 2.4) / 0.6)


def card(lines_spec, bg=(31, 42, 55)):
    img = Image.new("RGB", (W * SS, H * SS), bg); d = ImageDraw.Draw(img)
    y = None
    total = sum(sz * 1.5 for _, sz, _, _ in lines_spec)
    y = (H - total) / 2
    for text, sz, weight, color in lines_spec:
        f = font(sz, weight)
        tw = d.textlength(text, font=f) / SS
        d.text((s((W - tw) / 2), s(y)), text, font=f, fill=color)
        y += sz * 1.5
    return img


TITLE = card([
    ("Theo: uma sessão", 64, "Bold", (247, 246, 242)),
    ("Observem: o que acontece antes · o que ele faz · o que acontece depois", 28, "Regular", (201, 211, 222)),
    ("", 20, "Regular", (0, 0, 0)),
    ("Animação · exemplo fictício · não representa uma criança real", 24, "SemiBold", (232, 180, 143)),
])
END = card([
    ("Isto foi um episódio.", 56, "Bold", (247, 246, 242)),
    ("Agora vejam o que a equipe registrou em quatro semanas.", 32, "Regular", (201, 211, 222)),
    ("", 20, "Regular", (0, 0, 0)),
    ("Animação · exemplo fictício · não representa uma criança real", 24, "SemiBold", (232, 180, 143)),
])

TIMELINE = [  # (duração em s, função)
    (3.5, lambda t: TITLE),
    (6.0, scene_play),
    (6.5, scene_remove),
    (7.5, scene_behavior),
    (6.5, scene_return),
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
                nxt = TIMELINE[i + 1][1](0.0)
                img = Image.blend(img, nxt, (t - (dur - FADE)) / FADE)
            return img.resize((W, H), Image.LANCZOS)
        acc += dur


def main():
    out = sys.argv[1]
    total = sum(d for d, _ in TIMELINE)
    n = int(total * FPS)
    if "--preview" in sys.argv:
        folder = sys.argv[sys.argv.index("--preview") + 1]
        for T in (2.0, 5.0, 8.0, 11.0, 14.0, 17.5, 20.0, 25.0, 28.5, 31.0):
            frame_at(T).save(f"{folder}/p_{T:05.1f}.png")
        return
    proc = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
        "-movflags", "+faststart", out,
    ], stdin=subprocess.PIPE)
    for i in range(n):
        proc.stdin.write(frame_at(i / FPS).tobytes())
    proc.stdin.close()
    proc.wait()
    print("ok", n, "quadros", total, "s")


if __name__ == "__main__":
    main()
