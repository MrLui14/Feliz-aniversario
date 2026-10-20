import random
import time
import tkinter
import tkinter.font as tkfont
import turtle

LARGURA, ALTURA = 900, 700
FUNDO = "#0b0a1f"

TEXTO = "FELIZ ANIVERSÁRIO!"
CORES_TEXTO = ["#ff69b4", "#ffd700", "#00bfff", "#7cfc00", "#ffffff", "#ff8c00"]
CORES_CONFETE = ["#ff69b4", "#ffd700", "#00bfff", "#7cfc00", "#ffffff", "#ff4500"]

# (largura, altura, y_base, cor)
ANDARES = [
    (400, 90, -200, "#3E2723"),
    (300, 80, -110, "#F4C9D6"),
    (200, 70, -30, "#F5F0E6"),
]
CANDLE_XS = [-50, 0, 50]
CANDLE_BASE_Y = 40
CANDLE_ALTURA = 60


def retangulo(t, x_centro, y_base, largura, altura, cor, borda="black"):
    t.penup()
    t.goto(x_centro - largura / 2, y_base)
    t.setheading(0)
    t.color(borda, cor)
    t.pendown()
    t.begin_fill()
    for _ in range(2):
        t.forward(largura)
        t.left(90)
        t.forward(altura)
        t.left(90)
    t.end_fill()
    t.penup()


def crescer(tela, t, x_centro, y_base, largura, altura, cor, passo=6, pausa=0.012):
    """Desenha o retângulo 'subindo' do chão até a altura final."""
    h = passo
    while h < altura:
        retangulo(t, x_centro, y_base, largura, h, cor)
        tela.update()
        time.sleep(pausa)
        h += passo
    retangulo(t, x_centro, y_base, largura, altura, cor)
    tela.update()


def glace(tela, t, largura, y_topo):
    """Bolinhas cinzas na borda de cima, como cobertura."""
    x = -largura / 2 + 12
    while x < largura / 2:
        t.goto(x, y_topo)
        t.dot(22, "pink")
        tela.update()
        time.sleep(0.01)
        x += 20


def confeitos(tela, t, largura, altura, y_base, quantidade):
    for _ in range(quantidade):
        x = random.uniform(-largura / 2 + 10, largura / 2 - 10)
        y = random.uniform(y_base + 8, y_base + altura - 26)
        t.goto(x, y)
        t.dot(random.randint(5, 8), random.choice(CORES_CONFETE))
    tela.update()


def medir_texto(texto, fonte):
    try:
        f = tkfont.Font(family=fonte[0], size=fonte[1], weight=fonte[2])
        return f.measure(texto)
    except Exception:
        return len(texto) * fonte[1] * 0.75


def criar_chama(cor, tamanho):
    chama = turtle.Turtle()
    chama.hideturtle()
    chama.shape("circle")
    chama.color(cor)
    chama.shapesize(tamanho * 1.4, tamanho * 0.8)
    chama.penup()
    return chama


def principal():
    tela = turtle.Screen()
    tela.setup(LARGURA, ALTURA)
    tela.bgcolor(FUNDO)
    tela.title("FELIZ ANIVERSÁRIO! 🎂")
    tela.tracer(0)

    nome = "Lyu Lyu do Papai"

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.pensize(2)
    pen.penup()

    escritor = turtle.Turtle()
    escritor.hideturtle()
    escritor.penup()

    # 1) Prato
    crescer(tela, pen, 0, -215, 460, 15, "#cfd8dc", passo=5)

    # 2) Andares (de baixo para cima), com cobertura e confeitos
    for largura, altura, y_base, cor in ANDARES:
        crescer(tela, pen, 0, y_base, largura, altura, cor)
        pen.pensize(1)
        glace(tela, pen, largura, y_base + altura)
        confeitos(tela, pen, largura, altura, y_base, quantidade=int(largura / 12))
        pen.pensize(2)

    # 3) Velas
    for i, x in enumerate(CANDLE_XS):
        cor = "#ffffff" if i % 2 == 0 else "#ff6384"
        crescer(tela, pen, x, CANDLE_BASE_Y, 12, CANDLE_ALTURA, cor, passo=6, pausa=0.02)

    # 4) Chamas
    topo_vela = CANDLE_BASE_Y + CANDLE_ALTURA
    chamas = []
    for x in CANDLE_XS:
        externa = criar_chama("#ff8c00", 1.0)
        interna = criar_chama("#ffe066", 0.55)
        externa.goto(x, topo_vela + 18)
        interna.goto(x, topo_vela + 14)
        externa.showturtle()
        interna.showturtle()
        chamas.append((x, externa, interna))
        tela.update()
        time.sleep(0.25)

    # 5) Texto aparecendo letra por letra
    fonte = ("Georgia", 48, "bold")
    largura_texto = medir_texto(TEXTO, fonte)
    x_inicio = -largura_texto / 2
    y_texto = 190

    escritor.color(CORES_TEXTO[0])
    for i in range(1, len(TEXTO) + 1):
        escritor.clear()
        escritor.goto(x_inicio, y_texto)
        escritor.write(TEXTO[:i], align="left", font=fonte)
        tela.update()
        time.sleep(0.12)

    nome_writer = None
    if nome:
        nome_writer = turtle.Turtle()
        nome_writer.hideturtle()
        nome_writer.penup()
        nome_writer.color("white")
        nome_writer.goto(0, 135)
        nome_writer.write(nome, align="center", font=("Georgia", 26, "normal"))

    # 6) Loop final: chamas tremendo, texto mudando de cor, confete caindo
    confetes = []
    frame = 0
    while True:
        frame += 1

        for x, externa, interna in chamas:
            tam = random.uniform(0.85, 1.25)
            externa.shapesize(tam * 1.4, tam * 0.8)
            interna.shapesize(tam * 0.75, tam * 0.45)
            dx = random.uniform(-1.5, 1.5)
            externa.goto(x + dx, topo_vela + 18)
            interna.goto(x + dx, topo_vela + 14)

        if frame % 10 == 0:
            escritor.clear()
            escritor.color(random.choice(CORES_TEXTO))
            escritor.goto(x_inicio, y_texto)
            escritor.write(TEXTO, align="left", font=fonte)

        if frame % 3 == 0 and len(confetes) < 70:
            c = turtle.Turtle()
            c.hideturtle()
            c.shape("square")
            c.shapesize(random.uniform(0.3, 0.6))
            c.color(random.choice(CORES_CONFETE))
            c.penup()
            c.goto(random.uniform(-LARGURA / 2, LARGURA / 2), ALTURA / 2 + 10)
            c.showturtle()
            confetes.append([c, random.uniform(1.5, 4), random.uniform(-0.8, 0.8)])

        for item in confetes:
            c, vy, vx = item
            c.goto(c.xcor() + vx, c.ycor() - vy)
            c.setheading(c.heading() + 7)
            if c.ycor() < -ALTURA / 2 - 10:
                c.goto(random.uniform(-LARGURA / 2, LARGURA / 2), ALTURA / 2 + 10)

        tela.update()
        time.sleep(0.03)


if __name__ == "__main__":
    try:
        principal()
    except (turtle.Terminator, tkinter.TclError):
        pass  # janela fechada pelo usuário