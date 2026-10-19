"""Cria os slides de respostas (mostrados depois das perguntas) e insere no deck.

Reusa os helpers de gerar_slides.py (mesmo visual). Uso: python3 slides_respostas.py <pasta do deck>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "gerar_slides.py"), encoding="utf-8").read()
ns = {"__name__": "helpers", "sys": sys}
exec(compile(src[: src.index("S = {}")], "gerar_slides_helpers", "exec"), ns)
DECK = sys.argv[1]
SL = os.path.join(DECK, "project/slides")
title, para, hl, note, ul, ol, cols, table, content = (ns[k] for k in (
    "title", "para", "hl", "note", "ul", "ol", "cols", "table", "content"))
ns["LABEL"].update({"s12r": "12b", "s21r": "21b", "s26r": "26b", "s34r": "34b", "s36a": "36a", "s36b": "36b",
                    "s36c": "36c", "s36d": "36d", "s36e": "36e", "r1r": "R1b", "r2r": "R2b"})
RB = "#FFFFFF"
NOTA = "Slide de respostas: mostrar depois que a turma responder."


def resp(sid, blocks, gap=40):
    html = content(sid, blocks, bg=RB, gap=gap)
    return html.replace("<aside></aside>", f"<aside>{NOTA}</aside>")


N = {}

N["s12r"] = resp("s12r", [title("Respostas: o que justifica intervir"), table([
    ["Ganho para a pessoa", "Exemplo"],
    ["<b>Comunicação</b>", "Ter formas eficazes de pedir, recusar e se expressar"],
    ["<b>Aprendizagem e participação</b>", "Na escola, em casa e na comunidade"],
    ["<b>Autonomia</b>", "Fazer mais por si, com menos ajuda"],
    ["<b>Segurança</b>", "Quando o comportamento machuca a pessoa ou outras pessoas"],
    ["<b>Qualidade de vida</b>", "Bem-estar, interesses e relações"]], [38, 62], 32),
    hl("Características autistas inofensivas não são alvo por si só.", 38),
    note("Objetivos definidos com a família e, sempre que possível, com a própria pessoa.")], gap=34)

N["s21r"] = resp("s21r", [title("Respostas do desafio: a mesma estratégia, efeitos opostos"), table([
    ["Estratégia", "Onde pode ajudar", "Onde pode piorar"],
    ["Dar um tempo fora da atividade, <b>sem atenção</b>", "Situação 1: o comportamento deixa de produzir atenção",
     "Situação 2: a criança escapa da tarefa, que era o que mantinha o comportamento"],
    ["Devolver o tablet “para acalmar”", "Na hora, o choro para", "Situação 3: o comportamento fica mais forte nas próximas vezes"]],
    [30, 33, 37], 31),
    hl("Por isso, avaliar a função vem antes de escolher a estratégia.", 40)])

N["s26r"] = resp("s26r", [title("Respostas: o que cada abordagem perguntaria primeiro"), cols([
    ("Análise do comportamento", "Em que situações ela evita o grupo? O que acontece logo depois? O que mantém esse comportamento?"),
    ("TCC", "Que pensamentos e crenças ela tem sobre falar em grupo (“vou falar algo errado”)? Como eles influenciam a ansiedade e a esquiva?")], size=36),
    hl("As duas leituras ajudam a entender o caso, mas não são equivalentes.", 38)])

N["s34r"] = resp("s34r", [title("Respostas do vídeo"), cols([
    ("Antes", "A terapeuta guarda os trilhos e aponta a mesa: “Agora acabou. Vamos para a mesa.”"),
    ("O que ele faz", "Grita, se joga no chão e chuta o ar."),
    ("Depois", "A terapeuta não sabe o que fazer e devolve os trilhos. Ele volta a brincar.")], head_size=40, size=34, gap=64),
    para("<b>E a terapeuta?</b> Devolver os trilhos faz o grito parar e alivia quem está com ele. Esse alívio também pode reforçar o comportamento do adulto, e o ciclo continua.", 34),
    note("Vocês viram um episódio. Os registros de quatro semanas, na vinheta, mudam essa leitura.")], gap=40)

N["s36a"] = resp("s36a", [title("Respostas P1 a P3: o que aconteceu"), cols([
    ("P1. Comportamento", "Grita, se joga no chão e chuta o ar, por 3 a 8 minutos, em 11 de 12 sessões. Sem “birra” ou “crise”: são interpretações."),
    ("P2. Antes", "“Agora acabou, vamos para a mesa”; trilhos guardados; atividade de mesa. Contexto: sono ruim, troca de terapeuta."),
    ("P3. Depois", "Às vezes os trilhos voltam, às vezes a mesa é adiada, às vezes a mesa é mantida.")], head_size=36, size=31, gap=56),
    hl("Sono e troca de terapeuta são contexto, não função.", 38)])

N["s36b"] = resp("s36b", [title("Respostas P4: hipóteses, com dados a favor e contra", 58), table([
    ["Hipótese", "A favor", "Contra ou falta saber"],
    ["<b>H1</b> Acesso aos trilhos", "Acontece quando os trilhos são guardados; às vezes eles voltam; em casa, ao desligar a TV",
     "No lanche os trilhos também foram guardados, e não houve episódio"],
    ["<b>H2</b> Fuga da mesa", "Não acontece quando o próximo é o lanche; às vezes a mesa é adiada", "Em casa, o antecedente é o banho"],
    ["<b>H3</b> As duas juntas", "Os dois antecedentes acontecem ao mesmo tempo", "Precisa de avaliação"],
    ["<b>H4</b> Atenção", "Possível atenção durante o episódio", "Nenhum dado mostra isso"]], [22, 42, 36], 27),
    hl("O lanche é a pista: enfraquece H1 e fortalece H2 ou H3.", 36)], gap=30)

N["s36c"] = resp("s36c", [title("Respostas P5: como distinguir as hipóteses"), table([
    ["Se fizermos…", "Se for H1 (trilhos)", "Se for H2 (mesa)"],
    ["Apresentar a mesa <b>sem guardar os trilhos</b>", "Comportamento raro", "Comportamento continua"],
    ["Guardar os trilhos e ir para <b>outra atividade preferida</b>", "Comportamento continua", "Comportamento raro"],
    ["Mudar a <b>dificuldade</b> da tarefa de mesa", "Pouca mudança", "Mais episódios com tarefas difíceis"]], [44, 28, 28], 31),
    para("Se os dois cenários provocarem o comportamento, ganha força <b>H3</b>.", 34),
    note("Quem testa: a equipe, com profissional qualificado e supervisão.")], gap=34)

N["s36d"] = resp("s36d", [title("Respostas P6: e se a hipótese estiver errada?"), table([
    ["Estratégia pensada para…", "Se a função real for outra"],
    ["<b>H1:</b> “primeiro mesa, depois trem”; ensinar a pedir “mais trem” e a esperar", "Se for H2, pouco efeito: a mesa continua difícil"],
    ["<b>H2:</b> tarefa mais curta, com tema de trens; ensinar a pedir “pausa”", "Se for H1, o comportamento na hora de guardar os trilhos continua"],
    ["Adiar a mesa quando ele grita, “para acalmar”", "<b>Fortalece</b> o comportamento: o grito continua funcionando"]], [52, 48], 30),
    hl("Errar a hipótese pode ensinar o contrário do que queremos.", 40)])

N["s36e"] = resp("s36e", [title("Respostas P7: tirar os trilhos de vez?"), ul([
    "<b>O interesse não é o problema:</b> o problema é a transição e o que o comportamento consegue",
    "<b>Tirar não ensina nada novo:</b> Theo continuaria sem saber pedir “mais” ou “pausa”",
    "<b>Pode não resolver:</b> se a função for fugir da mesa, o comportamento continua",
    "<b>Os trens podem ser recurso:</b> tarefas com tema de trem, trilhos combinados para depois"], 34),
    hl("Acolher a família e decidir junto, com plano para casa e supervisão.", 38)])

N["r1r"] = resp("r1r", [title("Respostas: Lara"), table([
    ["Pergunta", "Resposta"],
    ["Comportamento", "Coloca o capuz, abaixa a cabeça e sai da sala sem avisar, nos trabalhos em grupo"],
    ["Hipótese principal", "Fuga ou esquiva do barulho e da interação; ir para a biblioteca pode reforçar a saída"],
    ["ABA × TCC", "ABA: em que condições ela sai e o que isso produz. TCC: que pensamentos e crenças ela tem sobre falar em grupo"],
    ["Proposta da escola", "Alivia agora, mas pode reforçar a esquiva; só como adaptação temporária, combinada com Lara"],
    ["Alternativas", "Lugar mais silencioso ou protetor auricular (se ela quiser), grupos menores, papel definido, forma combinada de pedir pausa"]],
    [26, 74], 28),
    note("O capuz, em si, não é alvo de intervenção.", 28)], gap=30)

N["r2r"] = resp("r2r", [title("Respostas: o dado novo"), cols([
    ("O que muda", "Enfraquece H2: a mesa sozinha quase não provocou o comportamento. Fortalece H1 ou H3: guardar os trilhos parece importante."),
    ("O que não muda", "Ainda não dá para concluir a função: são só 4 sessões, sem controle de sono, terapeuta ou tipo de tarefa.")], size=36),
    hl("É mais um indício. O próximo passo é avaliação sistemática, com supervisão.", 38)])

for sid, html in N.items():
    open(os.path.join(SL, sid + ".html"), "w", encoding="utf-8").write(html)

p = os.path.join(DECK, "project/deck.json")
d = json.load(open(p, encoding="utf-8"))
order = [x for x in d["order"] if x not in N]
AFTER = {"s12": ["s12r"], "s21": ["s21r"], "s26": ["s26r"], "s34v": ["s34r"],
         "s36": ["s36a", "s36b", "s36c", "s36d", "s36e"], "r1": ["r1r"], "r2": ["r2r"]}
new = []
for x in order:
    new.append(x)
    new.extend(AFTER.get(x, []))
d["order"] = new
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(N), "slides de respostas;", len(new), "slides no total")
