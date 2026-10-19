"""Gera os slides (visual v2: Montserrat, fundo branco, conteúdo centralizado).

Lê as notas (<aside>) dos slides atuais e reescreve cada project/slides/<id>.html.
Uso: python3 gerar_slides.py <pasta do deck>
"""
import os
import re
import sys

DECK = sys.argv[1]
SL = os.path.join(DECK, "project/slides")

NAVY = "#1B2F4B"
TEXT = "#2E3A4A"
TEAL = "#0F7C86"
MUTED = "#66717F"
BG = "#FCFCFB"
BG_ACT = "#EEF4F5"
FONT = "font-family:'Montserrat', Arial, sans-serif"


def notes(sid):
    p = os.path.join(SL, sid + ".html")
    if not os.path.exists(p):
        return ""
    m = re.search(r"<aside>(.*?)</aside>", open(p, encoding="utf-8").read(), re.S)
    return m.group(1).strip() if m else ""


LABEL = {"s34v": "34a", "s35b": "35b", "r1": "R1", "r2": "R2"}


def num(sid):
    if sid in LABEL:
        return LABEL[sid]
    if sid.startswith("a"):
        return sid.upper()
    return str(int(sid[1:]))


# ---------- blocos ----------
def title(t, size=66):
    return f'<h2 style="font-size:{size}px;font-weight:700;line-height:1.15;color:{NAVY}">{t}</h2>'


def para(t, size=40, color=TEXT, weight=400):
    return f'<p style="font-size:{size}px;font-weight:{weight};line-height:1.4;color:{color}">{t}</p>'


def hl(t, size=44):
    return f'<p style="font-size:{size}px;font-weight:700;line-height:1.3;color:{TEAL}">{t}</p>'


def note(t, size=30):
    return f'<p style="font-size:{size}px;font-style:italic;line-height:1.4;color:{MUTED}">{t}</p>'


def ul(items, size=40):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<ul style="font-size:{size}px;line-height:1.5;color:{TEXT}">{li}</ul>'


def ol(items, size=40):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<ol style="font-size:{size}px;line-height:1.5;color:{TEXT}">{li}</ol>'


def cols(items, head_size=42, size=36, gap=96):
    out = f'<div style="display:flex;gap:{gap}px">'
    for h, t in items:
        out += (f'<div style="flex:1;display:flex;flex-direction:column;gap:14px">'
                f'<h3 style="font-size:{head_size}px;font-weight:700;line-height:1.2;color:{TEAL}">{h}</h3>'
                f'<p style="font-size:{size}px;line-height:1.4;color:{TEXT}">{t}</p></div>')
    return out + "</div>"


def bignums(items):
    out = '<div style="display:flex;gap:96px">'
    for n, t in items:
        out += (f'<div style="flex:1;display:flex;flex-direction:column;gap:10px">'
                f'<p style="font-size:120px;font-weight:800;line-height:1.05;color:{TEAL}">{n}</p>'
                f'<p style="font-size:34px;line-height:1.4;color:{TEXT}">{t}</p></div>')
    return out + "</div>"


def table(rows, widths, size=34):
    head, *body = rows
    out = f'<table style="font-size:{size}px;color:{TEXT};width:1576px">'
    out += f'<tr style="background:{NAVY}">' + "".join(
        f'<th style="width:{w}%;color:#FFFFFF;text-align:left;padding:18px">{h}</th>' for h, w in zip(head, widths)) + "</tr>"
    for i, r in enumerate(body):
        bg = "#FFFFFF" if i % 2 == 0 else "#F1F4F6"
        out += f'<tr style="background:{bg}">' + "".join(f'<td style="padding:18px">{c}</td>' for c in r) + "</tr>"
    return out + "</table>"


def content(sid, blocks, cite=None, bg=BG, gap=52):
    foot = ""
    if cite:
        foot += f'<p style="position:absolute;left:184px;bottom:52px;width:1400px;font-size:24px;color:{MUTED}">{cite}</p>'
    foot += f'<p style="position:absolute;right:96px;bottom:52px;width:120px;font-size:24px;color:{MUTED};text-align:right">{num(sid)}</p>'
    return (f'<section id="{sid}" style="background:{bg};color:{TEXT};{FONT};padding:110px 160px 140px 184px;'
            f'display:flex;flex-direction:column;justify-content:center;gap:{gap}px">'
            f'<div style="position:absolute;left:0px;top:0px;width:28px;height:1080px;background:{TEAL}"></div>'
            + "".join(blocks) + foot + f"<aside>{notes(sid)}</aside></section>\n")


def statement(sid, main, sub=None, small=None, bg=NAVY, main_size=84, sub_color="#9FD3D8"):
    parts = ""
    if sub:
        parts += f'<p style="font-size:40px;line-height:1.4;color:#D8E1EA;text-align:center">{sub}</p>'
    parts += f'<h1 style="font-size:{main_size}px;font-weight:800;line-height:1.15;color:#FFFFFF;text-align:center">{main}</h1>'
    if small:
        parts += f'<p style="font-size:30px;font-style:italic;line-height:1.4;color:{sub_color};text-align:center">{small}</p>'
    return (f'<section id="{sid}" style="background:{bg};color:#FFFFFF;{FONT};padding:140px 200px;display:flex;'
            f'flex-direction:column;justify-content:center;align-items:center;gap:44px">{parts}'
            f'<p style="position:absolute;right:96px;bottom:52px;width:120px;font-size:24px;color:#B8C4D2;text-align:right">{num(sid)}</p>'
            f"<aside>{notes(sid)}</aside></section>\n")


S = {}

S["s01"] = (f'<section id="s01" style="background:{NAVY};color:#FFFFFF;{FONT};padding:140px 160px;display:flex;flex-direction:column;justify-content:center;gap:28px">'
            f'<div style="position:absolute;left:0px;bottom:0px;width:1920px;height:28px;background:{TEAL}"></div>'
            f'<p style="font-size:32px;font-weight:500;color:#9FD3D8">Liga Acadêmica Cognitivo-Comportamental (LACC)</p>'
            f'<h1 style="font-size:140px;font-weight:800;line-height:1.0;color:#FFFFFF">ABA e TEA</h1>'
            f'<p style="font-size:56px;font-weight:400;line-height:1.2;color:#E6ECF2">da análise funcional à decisão clínica</p>'
            f'<div style="height:60px"></div>'
            f'<p style="font-size:42px;font-weight:700;color:#FFFFFF">Betina Binatti</p>'
            f'<p style="font-size:32px;color:#C9D3DE">24 de outubro de 2026, PUCRS</p>'
            f"<aside>{notes('s01')}</aside></section>\n")

S["s02"] = content("s02", [title("Quem conduz o workshop"), para("Betina Binatti", 52, NAVY, 700), ul([
    "Psicóloga formada pela PUCRS",
    "Pós-graduada em ABA e Estratégias Naturalistas (Instituto Singular)",
    "Pós-graduanda em Neuropsicologia (Comportamente)",
    "7 anos de experiência em neurodivergência",
    "2 anos e 6 meses como coordenadora de caso e supervisora clínica"], 38)], gap=40)

S["s03"] = content("s03", [title("Ao final, vocês vão conseguir"), ol([
    "Explicar por que o TEA é heterogêneo",
    "<b>Diferenciar topografia e função</b>",
    "<b>Identificar antecedentes, consequências e contexto</b>",
    "<b>Justificar por que avaliar vem antes de intervir</b>",
    "Reconhecer estratégias baseadas em evidências e ligá-las à função",
    "Analisar uma vinheta e justificar decisões",
    "Reconhecer limites de atuação e a importância da supervisão"], 36)], gap=40)

S["s04"] = content("s04", [title("Este workshop não forma aplicadores"), cols([
    ("O que é", "Uma introdução ao raciocínio analítico-comportamental aplicado ao TEA."),
    ("O que não é", "Um curso de formação em ABA. Ele não habilita ninguém a avaliar ou intervir sem formação e supervisão.")], size=40)])

S["s05"] = content("s05", [title("Combinados"), ul([
    "Perguntas são bem-vindas a qualquer momento",
    "Todos os casos são fictícios",
    "Não vamos discutir casos reais",
    "Vamos usar “pessoa autista”, respeitando preferências individuais"])], cite="Bottema-Beutel et al. (2021)")

S["s06"] = statement("s06", "Por quê?", sub="Uma criança grita e se joga no chão quando a atividade muda.", small="Exemplo fictício", main_size=140)

S["s07"] = content("s07", [title("O diagnóstico de TEA se apoia em dois domínios"), cols([
    ("Comunicação e interação social", "Diferenças persistentes, em vários contextos."),
    ("Padrões restritos e repetitivos", "De comportamento, interesses ou atividades, incluindo respostas sensoriais.")], size=38),
    para("Os sinais aparecem no início do desenvolvimento e têm impacto significativo no funcionamento.", 36)],
    cite="American Psychiatric Association (2022), DSM-5-TR")

S["s08"] = content("s08", [title("Especificadores e níveis de gravidade"),
    para("<b>Especificadores:</b> com ou sem deficiência intelectual, com ou sem comprometimento de linguagem, condições associadas.", 34),
    table([["Nível", "Necessidade de apoio"], ["1", "Exige apoio"], ["2", "Exige apoio substancial"], ["3", "Exige apoio muito substancial"]], [20, 80]),
    note("Os níveis são definidos para cada domínio e descrevem necessidade de apoio, não “grau de autismo”.")],
    cite="American Psychiatric Association (2022), DSM-5-TR", gap=40)

S["s09"] = content("s09", [title("O diagnóstico não define o plano"),
    para("Duas pessoas autistas podem ser muito diferentes em linguagem, capacidade intelectual, necessidade de apoio, condições coocorrentes, interesses e contexto familiar."),
    hl("O plano nasce da avaliação da pessoa, não do rótulo.", 48)], cite="Lord et al. (2020); Lord et al. (2022)")

S["s10"] = content("s10", [title("Prevalência depende de onde e como se mede"), bignums([
    ("≈ 1%", "Estimativa global (mediana de 100 por 10.000 em estudos de vários países)"),
    ("1 em 31", "Crianças de 8 anos em 16 regiões dos EUA, em 2022")]),
    para("Parte da variação reflete práticas de identificação e acesso a avaliação.", 36)],
    cite="Zeidan et al. (2022); Shaw et al. (2025)")

S["s11"] = content("s11", [title("Neurodiversidade: diferença não é algo a “curar”"), ul([
    "O autismo como parte da variação humana",
    "Reconhecer dificuldades e respeitar a identidade não são opostos",
    "A linguagem importa: “pessoa autista”, “interesses focados”"])], cite="Kapp et al. (2013); Bottema-Beutel et al. (2021)")

S["s12"] = statement("s12", "Se o objetivo não é “tirar o autismo”, o que justifica uma intervenção?", main_size=76)

S["s13"] = content("s13", [title("ABA é uma ciência aplicada, não um pacote de técnicas"),
    para("Sete dimensões definem a Análise do Comportamento Aplicada:"),
    f'<div style="display:flex;gap:96px">{ul(["Aplicada", "Comportamental", "Analítica", "Tecnológica"])}{ul(["Conceitualmente sistemática", "Efetiva", "Generalidade"])}</div>'],
    cite="Baer, Wolf &amp; Risley (1968)", gap=40)

S["s14"] = content("s14", [title("Topografia descreve. Função explica."), cols([
    ("Topografia", "A forma do comportamento: o que se vê e se ouve."),
    ("Função", "A relação com as consequências que mantêm o comportamento.")], size=38),
    hl("A mesma forma pode ter funções diferentes, e formas diferentes podem ter a mesma função.", 38),
    note("Exemplo fictício: bater na mesa pode produzir atenção para uma criança e a retirada da tarefa para outra.")],
    cite="Cooper, Heron &amp; Heward (2020); Iwata et al. (1982/1994)", gap=44)

S["s15"] = content("s15", [title("O comportamento acontece entre um antes e um depois"), cols([
    ("A. Antecedente", "O que acontece imediatamente antes"),
    ("B. Comportamento", "O que a pessoa faz, descrito de forma observável"),
    ("C. Consequência", "O que acontece imediatamente depois")], head_size=38, size=34, gap=64),
    note("Exemplo fictício: a terapeuta guarda o tablet (A), a criança grita e joga o copo no chão (B), o tablet é devolvido (C).")],
    cite="Cooper, Heron &amp; Heward (2020)")

S["s16"] = content("s16", [title("O contexto muda o valor das consequências"), cols([
    ("Variáveis contextuais", "Sono, dor, fome, rotina, ambiente sensorial."),
    ("Operação motivadora", "Altera por um tempo o valor de uma consequência e a frequência dos comportamentos ligados a ela.")], size=38),
    note("Exemplo fictício: depois de uma noite mal dormida, uma tarefa difícil fica mais aversiva, e escapar dela passa a “valer mais”.")],
    cite="Laraway et al. (2003)")

S["s17"] = content("s17", [title("Reforçamento se define pelo efeito, não pela intenção"),
    para("Reforçamento é quando a consequência aumenta a chance de o comportamento voltar a acontecer."),
    cols([("Positivo", "Algo é acrescentado. Ex.: a criança recebe atenção."),
          ("Negativo", "Algo é retirado ou adiado. Ex.: a tarefa sai.")], size=38),
    hl("“Negativo” não é punição.", 42)], cite="Cooper, Heron &amp; Heward (2020)", gap=44)

S["s18"] = content("s18", [title("Quatro hipóteses funcionais frequentes"), ol([
    "Acesso a atenção",
    "Acesso a itens ou atividades",
    "Fuga ou esquiva de demandas ou estímulos",
    "Reforçamento automático: o próprio comportamento produz a consequência"]),
    hl("São hipóteses a testar, não rótulos. Podem ser múltiplas ou combinadas.", 38)],
    cite="Iwata et al. (1982/1994); Hanley, Iwata &amp; McCord (2003); Hanley et al. (2014)")

S["s19"] = content("s19", [title("Mini-exercício em duplas (5 min)"),
    para("Nas três situações a seguir, o comportamento é o mesmo: <b>a criança joga os materiais no chão e chora.</b>"),
    ol(["O que acontece logo depois?", "Que hipótese funcional isso sugere?", "O que vocês precisariam observar mais?"]),
    para("<b>Desafio:</b> pensem em uma estratégia que ajudaria em uma situação e pioraria outra. Por quê?", 36, TEAL)],
    bg=BG_ACT, gap=40)

S["s20"] = content("s20", [title("Três situações"), ol([
    "A terapeuta se levanta para atender a mãe na porta. A criança joga os materiais e chora. A terapeuta volta, senta ao lado e conversa até ela se acalmar.",
    "A terapeuta apresenta uma folha de escrita. A criança joga os materiais e chora. A terapeuta guarda a folha: “fazemos depois”.",
    "A terapeuta guarda o tablet. A criança joga os materiais e chora. Minutos depois, ela devolve o tablet “só mais um pouquinho”."], 34),
    note("Exemplo fictício")], bg=BG_ACT, gap=40)

S["s21"] = content("s21", [title("Mesma topografia, três hipóteses"),
    table([["Situação", "O que acontece depois", "Hipótese"], ["1", "A atenção volta", "<b>Acesso a atenção</b>"],
           ["2", "A tarefa sai", "<b>Fuga da demanda</b>"], ["3", "O tablet volta", "<b>Acesso a item</b>"]], [16, 42, 42], 36),
    para("Um episódio não basta: hipóteses se sustentam em <b>padrões que se repetem</b>.", 36)],
    cite="Hanley (2012)", gap=44)

S["s22"] = statement("s22", "Avaliar vem antes de intervir.", sub="Cada resposta do início era uma hipótese funcional diferente.",
                     small="Só a avaliação permite escolher entre elas.", main_size=96)

S["s23"] = content("s23", [title("ABA e TCC compartilham compromissos empíricos"), ul([
    "Avaliação de resultados com dados",
    "Alvos definidos de forma operacional",
    "Formulação individualizada do caso",
    "Procedimentos baseados em princípios de aprendizagem, como reforçamento, exposição, modelação e treino de habilidades"]),
    note("Aproximação não é equivalência.")])

S["s24"] = content("s24", [title("ABA e TCC partem de pressupostos diferentes"),
    table([["", "ABA", "TCC (modelo de Beck)"], ["<b>Base</b>", "Behaviorismo radical", "Modelo cognitivo"],
           ["<b>Pensamentos e sentimentos</b>", "Comportamentos a explicar", "Mediadores e alvo central"],
           ["<b>Análise</b>", "Relação comportamento–ambiente", "Situação, pensamento, emoção e comportamento"],
           ["<b>Formulação</b>", "Análise funcional", "Conceituação cognitiva"]], [28, 36, 36], 32)],
    cite="Skinner (1953); Beck (2021)")

S["s25"] = content("s25", [title("No TEA, cada abordagem tem evidências em áreas diferentes"), cols([
    ("Práticas de base comportamental", "Têm critério de evidência: FCT, intervenções antecedentes, reforçamento diferencial, intervenção naturalística, entre outras."),
    ("TCC adaptada para autismo", "Tem evidência de ensaio clínico para ansiedade em crianças autistas de 7 a 13 anos.")], size=36)],
    cite="Hume et al. (2021); Wood et al. (2020)")

S["s26"] = statement("s26", "O que um analista do comportamento perguntaria primeiro? E um terapeuta cognitivo-comportamental?",
                     sub="Uma adolescente autista, com boa linguagem, evita trabalhos em grupo e diz ter medo de “falar algo errado”.",
                     small="Exemplo fictício", main_size=64)

S["s27"] = statement("s27", "Intervalo", sub="Voltamos às 10h45.", small="Ao voltar, formem grupos de 4 a 6 pessoas.",
                     bg=TEAL, main_size=140, sub_color="#E6F4F5")

S["s28"] = content("s28", [title("Três formas de avaliar a função, com limites diferentes"),
    table([["Avaliação", "Como", "Limite"], ["<b>Indireta</b>", "Entrevistas, escalas", "Depende do relato de outras pessoas"],
           ["<b>Descritiva</b>", "Observação direta A–B–C", "Mostra associação, não causa"],
           ["<b>Análise funcional</b>", "Teste sistemático de condições", "Exige profissional qualificado, supervisão e segurança"]], [24, 34, 42], 32)],
    cite="Hanley, Iwata &amp; McCord (2003); Hanley (2012); BACB (2020)")

S["s29"] = content("s29", [title("Prevenir é mudar o contexto, não só reagir"),
    para("Estratégias antecedentes, escolhidas a partir da hipótese:"), ul([
    "<b>Previsibilidade:</b> aviso de transição, apoio visual",
    "<b>Ajuste da demanda:</b> duração, dificuldade, interesse",
    "<b>Escolhas</b> reais",
    "<b>Acesso planejado</b> a pausas e itens preferidos"])],
    cite="Cooper, Heron &amp; Heward (2020); Laraway et al. (2003); Hume et al. (2021)", gap=40)

S["s30"] = content("s30", [title("FCT: ensinar a pedir o que o comportamento conseguia"), ol([
    "Identificar a função",
    "Ensinar uma forma de comunicação que produza a mesma consequência (“pausa”, “ajuda”, “mais”)",
    "Responder a essa comunicação de forma consistente",
    "Ensinar, aos poucos, a esperar e a tolerar um “agora não”"], 36),
    note("Exemplo fictício: se a hipótese é fuga da tarefa, ensinar a pedir “pausa”, por palavra, gesto, figura ou outro sistema de comunicação.", 28)],
    cite="Carr &amp; Durand (1985); Tiger, Hanley &amp; Bruzek (2008); Hanley et al. (2014)", gap=40)

S["s31"] = content("s31", [title("Ensinar no contexto natural, a partir do interesse da criança"),
    para("Intervenções Naturalísticas Desenvolvimentais Comportamentais (NDBI):", 36), ul([
    "Contextos naturais, como o brincar e as rotinas",
    "Controle compartilhado entre criança e adulto",
    "Consequências naturais",
    "Integração entre ciência comportamental e ciência do desenvolvimento"], 36)],
    cite="Schreibman et al. (2015); Sandbank et al. (2020)", gap=40)

S["s32"] = content("s32", [title("Generalização precisa ser planejada"),
    para("Aprender na clínica não garante usar em casa, na escola ou com outras pessoas."),
    hl("Planejar desde o início: várias pessoas, lugares e materiais, com a família envolvida.", 40),
    note("Exemplo fictício: a criança aprende a pedir “pausa” com a terapeuta, e o plano inclui ensinar a família a responder ao mesmo pedido em casa.")],
    cite="Stokes &amp; Baer (1977)", gap=44)

S["s33"] = content("s33", [title("Decidir bem é decidir com ética"), ul([
    "Objetivos com sentido para a vida da pessoa, definidos com a família e com a pessoa",
    "<b>Assentimento:</b> observar sinais de concordância e de recusa",
    "Não ter como alvo características autistas inofensivas",
    "Revisar por dados, incluindo possíveis efeitos adversos",
    "Supervisão e limites de atuação"], 36)],
    cite="Breaux &amp; Smith (2023); Sandbank et al. (2023); CFP (2005); BACB (2020)")

S["s34"] = content("s34", [title("Atividade em grupos de 4 a 6 pessoas (10 min)"), cols([
    ("Todos os grupos", "Perguntas 1 a 4"),
    ("Cada grupo, mais uma", "Grupo 1: P5. Grupo 2: P6. Grupo 3: P7. Grupo 4: P5, e assim por diante.")], size=38),
    para("Escolham quem anota e quem apresenta.", 36),
    hl("A vinheta permite levantar hipóteses, não concluir a função.", 40)], bg=BG_ACT, gap=44)

S["s34v"] = content("s34v", [title("Vídeo: Theo, uma sessão"),
    para("Enquanto assistem (cerca de 30 segundos), observem:"),
    ol(["O que acontece imediatamente antes?", "O que exatamente ele faz?", "O que acontece imediatamente depois?"]),
    note("Animação, exemplo fictício. Não representa uma criança real. O vídeo mostra um episódio; o padrão está na vinheta a seguir.", 28)],
    bg=BG_ACT, gap=40)

S["s35"] = content("s35", [title("Vinheta: Theo", 58),
    para("Theo tem 6 anos e é autista. Comunica-se principalmente por palavras isoladas e por gestos (puxa o adulto pela mão, aponta). Gosta muito de montar trilhos de trem. Frequenta atendimento clínico três vezes por semana. Nas últimas quatro semanas, a equipe registrou:", 32),
    ul(["Quando a terapeuta diz “agora acabou, vamos para a mesa”, Theo <b>grita, se joga no chão e chuta o ar</b>, por cerca de 3 a 8 minutos. Isso aconteceu em <b>11 de 12 sessões</b>, quase sempre na passagem dos trilhos para a atividade de mesa (traçar letras e encaixes).",
        "Em <b>duas sessões</b> em que a terapeuta também guardou os trilhos, mas a atividade seguinte foi o <b>lanche</b>, Theo <b>não</b> apresentou o comportamento."], 32),
    note("Exemplo fictício, parte 1 de 2", 26)], bg="#FFFFFF", gap=30)

S["s35b"] = content("s35b", [title("Vinheta: Theo (continuação)", 58), ul([
    "As reações dos adultos variaram: em algumas sessões, a terapeuta esperou e depois <b>devolveu os trilhos “por mais cinco minutos”</b>; em outras, <b>adiou a atividade de mesa</b> para o fim da sessão; em outras, <b>manteve a atividade</b> e conduziu Theo até a mesa.",
    "A mãe relata que, em casa, Theo reage de forma parecida quando precisa <b>desligar a televisão para tomar banho</b>.",
    "A mãe também conta que, nas semanas em que os episódios foram <b>mais longos</b>, Theo <b>dormiu mal</b> e houve <b>troca da terapeuta</b> que o atendia.",
    "Nas sessões em que a terapeuta <b>mostrou um cartão “primeiro trilhos, depois mesa” e avisou dois minutos antes</b>, os episódios foram <b>mais curtos</b> (registro em 3 sessões)."], 32),
    note("Exemplo fictício, parte 2 de 2", 26)], bg="#FFFFFF", gap=30)

S["s36"] = content("s36", [title("Roteiro de perguntas", 56),
    para("Todos os grupos (cerca de 6 min)", 32, TEAL, 700), ol([
    "Descrevam o comportamento de forma que dois observadores concordariam. Que palavras evitaram, e por quê?",
    "O que acontece antes? <i>(rápida)</i>",
    "E depois? <i>(rápida)</i>",
    "Duas hipóteses funcionais, com <b>um dado a favor e um contra</b> cada uma"], 29),
    para("Rodízio, uma por grupo (cerca de 4 min)", 32, TEAL, 700),
    para("<b>5.</b> Como distinguir H1 de H2? <b>O que esperariam ver</b> em cada uma?", 29),
    para("<b>6.</b> Uma estratégia para uma hipótese. <b>E se a hipótese estiver errada?</b>", 29),
    para("<b>7.</b> <b>Dilema:</b> a mãe pergunta se não é melhor <b>tirar os trilhos de vez</b>. O que responder?", 29)],
    bg=BG_ACT, gap=20)

S["s37"] = content("s37", [title("Plenária: do comportamento à decisão"),
    hl("Topografia → Contexto → Hipóteses → Como distinguir → Estratégias → Ética", 40),
    para("Uma vinheta <b>não permite concluir a função</b>. Ela permite levantar hipóteses que exigem avaliação adequada.", 38)],
    cite="Hanley et al. (2014)")

S["s38"] = content("s38", [title("Cinco mensagens para levar"), ol([
    "TEA é heterogêneo: <b>o diagnóstico não define o plano</b>",
    "<b>Topografia descreve; função explica</b>",
    "<b>Avaliar vem antes de intervir</b>",
    "Bons objetivos ampliam comunicação, participação, autonomia e qualidade de vida",
    "Raciocínio clínico exige <b>evidência, individualização, ética e supervisão</b>"], 38)], gap=44)

S["s39"] = statement("s39", "Perguntas?", main_size=150)

S["s40"] = content("s40", [title("Para aprofundar"),
    table([["Leitura", "Tema"], ["Baer, Wolf &amp; Risley (1968)", "O que define a ABA"], ["Hanley (2012)", "Avaliação funcional na prática"],
           ["Tiger, Hanley &amp; Bruzek (2008)", "Treino de Comunicação Funcional"], ["Schreibman et al. (2015)", "Intervenções naturalísticas (NDBI)"],
           ["Sandbank et al. (2020)", "Qualidade da evidência em intervenção precoce"], ["Breaux &amp; Smith (2023)", "Assentimento"]], [48, 52], 30)],
    cite="Referências completas nos slides finais")

S["s41"] = statement("s41", "Obrigada!", sub="Betina Binatti", small="Workshop ABA e TEA, LACC, PUCRS, 24 de outubro de 2026", main_size=150)

S["r1"] = content("r1", [title("Reserva: vinheta da Lara", 54),
    para("Lara tem 14 anos, é autista e se comunica oralmente com fluência. Gosta de desenho e de astronomia. Na escola, nos últimos dois meses, quando a professora propõe <b>trabalhos em grupo</b> na sala (que costuma ficar barulhenta), Lara <b>coloca o capuz, abaixa a cabeça e, às vezes, sai da sala</b> sem avisar. Quando sai, é encaminhada à coordenação e passa o restante da aula na biblioteca. Em atividades individuais, participa e tira boas notas. Contou à psicóloga escolar que “o barulho é demais” e que “sempre fala alguma coisa errada nos grupos”.", 28),
    ol(["Descrevam o comportamento de forma observável. Quais são os antecedentes, o contexto e as hipóteses funcionais?",
        "O que um analista do comportamento e um terapeuta cognitivo-comportamental perguntariam primeiro?",
        "A escola propõe que Lara faça todos os trabalhos sozinha, na biblioteca. Que efeito isso teria a curto e a longo prazo? Que alternativa aumentaria a participação sem ensinar que sair sem avisar é a única forma de conseguir uma pausa?"], 26),
    note("Exemplo fictício", 24)], bg=BG_ACT, gap=24)

S["r2"] = content("r2", [title("Reserva: um dado novo sobre Theo"),
    para("Na semana seguinte, em 4 sessões, a terapeuta apresentou a atividade de mesa <b>sem guardar os trilhos</b> (ficaram ao lado, e Theo poderia voltar a eles ao terminar). Em <b>3 dessas sessões</b>, Theo não gritou nem se jogou no chão.", 38),
    hl("Como esse dado muda a força de cada hipótese? Ele permite concluir a função?", 40), note("Exemplo fictício")],
    bg=BG_ACT, gap=44)


def refs(sid, head, items):
    blocks = [title(head, 52)] + [f'<p style="font-size:24px;line-height:1.4;color:{TEXT}">{i}</p>' for i in items]
    return content(sid, blocks, gap=18)


def old_refs(sid):
    s = open(os.path.join(SL, sid + ".html"), encoding="utf-8").read()
    ps = re.findall(r'<p style="font-size:24px;line-height:1.35;color:#1F2A37">(.*?)</p>', s, re.S)
    return ps


for sid, head in (("a1", "Referências: TEA e neurodiversidade"), ("a2", "Referências: ABA e análise funcional"),
                  ("a3", "Referências: ABA, TCC e intervenção"), ("a4", "Referências: estratégias naturalistas e evidência"),
                  ("a5", "Referências: ética e assentimento")):
    items = old_refs(sid)
    if not items:
        raise SystemExit(f"referências não encontradas em {sid}")
    S[sid] = refs(sid, head, items)

for sid, html in S.items():
    open(os.path.join(SL, sid + ".html"), "w", encoding="utf-8").write(html)
print(len(S), "slides gerados")
