import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from classes import *


TAMANHO_CELULA = 30
LARGURA = 15
ALTURA = 15

mapa = Tabuleiro(LARGURA, ALTURA)

heroi = None
em_combate = False
inimigo_atual = None



janela = ctk.CTk()
janela.title("RPG - Aventura")
janela.resizable(False, False)



canvas = ctk.CTkCanvas(
    janela,
    width=LARGURA * TAMANHO_CELULA,
    height=ALTURA * TAMANHO_CELULA,
    bg="white"
)
canvas.pack(padx=10, pady=10)




informacoes = ctk.CTkLabel(
    janela,
    text="",
    font=("Arial", 12)
)
informacoes.pack()

mensagem = ctk.CTkLabel(
    janela,
    text="Use W, A, S, D para movimentar",
    font=("Arial", 11)
)
mensagem.pack(pady=5)



painel_combate = ctk.CTkFrame(janela)

titulo_combate = ctk.CTkLabel(
    painel_combate,
    text="COMBATE",
    font=("Arial", 16, "bold")
)
titulo_combate.pack(pady=5)

status_combate = ctk.CTkLabel(
    painel_combate,
    text="",
    font=("Arial", 11)
)
status_combate.pack(pady=5)

botoes = ctk.CTkFrame(painel_combate)
botoes.pack(pady=5)



def desenhar_tabuleiro():

    canvas.delete("all")

    for y in range(ALTURA):
        for x in range(LARGURA):

            x1 = x * TAMANHO_CELULA
            y1 = y * TAMANHO_CELULA
            x2 = x1 + TAMANHO_CELULA
            y2 = y1 + TAMANHO_CELULA

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="#e8e8e8",
                outline="black"
            )

            lista = mapa.entidades.get((x, y), [])

            inimigos = [
                p for p in lista
                if isinstance(p, Inimigo) and p.get_vida() > 0
            ]

            jogador = heroi is not None and (
                heroi.posicao_x == x and
                heroi.posicao_y == y and
                heroi.get_vida() > 0
            )

            if jogador and inimigos:
                simbolo = "⚔"
                cor = "purple"

            elif jogador:
                simbolo = "J"
                cor = "blue"

            else:
                continue

            canvas.create_text(
                x1 + TAMANHO_CELULA // 2,
                y1 + TAMANHO_CELULA // 2,
                text=simbolo,
                fill=cor,
                font=("Arial", 18, "bold")
            )



def atualizar_status():

    if heroi is None:
        return

    texto = (
        f"{heroi.get_nome()} | "
        f"Vida: {heroi.get_vida()}% | "
        f"Posição: ({heroi.posicao_x}, {heroi.posicao_y})"
    )

    if hasattr(heroi, "mana"):
        texto += f" | Mana: {heroi.mana}"

    informacoes.configure(text=texto)



def mover_heroi(event):

    global em_combate, inimigo_atual

    if em_combate or heroi is None:
        return

    tecla = event.keysym.upper()

    if tecla not in ["W", "A", "S", "D"]:
        return

    resultado = heroi.mover(tecla, mapa)

    if resultado == "morto":
        mensagem.configure(text="Você está morto!")
        return

    if resultado == "parede":
        mensagem.configure(text="Você encontrou uma parede!")
        return

    mensagem.configure(
        text=f"Você se moveu para ({heroi.posicao_x}, {heroi.posicao_y})"
    )

    desenhar_tabuleiro()
    atualizar_status()

    
    inimigos = mapa.inimigos_na_posicao(heroi)

    if inimigos:
        iniciar_combate(inimigos[0])



def iniciar_combate(inimigo):

    global em_combate, inimigo_atual

    em_combate = True
    inimigo_atual = inimigo

    mensagem.configure(
        text=f"Você encontrou {inimigo.get_nome()}!"
    )

    painel_combate.pack(pady=10)

    atualizar_combate()
    desenhar_tabuleiro()



def atualizar_combate():

    if inimigo_atual is None:
        return

    status_combate.configure(
        text=(
            f"Sua vida: {heroi.get_vida()}% | "
            f"Vida do inimigo: {inimigo_atual.get_vida()}%"
        )
    )



def finalizar_combate():

    global em_combate, inimigo_atual

    em_combate = False
    inimigo_atual = None

    painel_combate.pack_forget()

    atualizar_status()
    desenhar_tabuleiro()



def turno_inimigo():

    if heroi.get_vida() <= 0:
        game_over()
        return

    dano = inimigo_atual.atacar(heroi)

    mensagem.configure(
        text=f"O inimigo causou {dano} de dano!"
    )

    if heroi.get_vida() <= 0:
        atualizar_status()
        game_over()
        return

    atualizar_combate()
    atualizar_status()



def verificar_vitoria():

    if inimigo_atual.get_vida() <= 0:

        nome = inimigo_atual.get_nome()

        mapa.remover_personagem(inimigo_atual)

        CTkMessagebox(
            title="Vitória!",
            message=f"Você derrotou {nome}!",
            icon="check"
        )

        finalizar_combate()
        return True

    return False



def ataque_basico():

    if not em_combate:
        return

    dano = heroi.atacar(inimigo_atual)

    mensagem.configure(
        text=f"Você causou {dano} de dano!"
    )

    if verificar_vitoria():
        return

    turno_inimigo()
    desenhar_tabuleiro()



def habilidade_especial():

    if not em_combate:
        return

    try:

        if hasattr(heroi, "golpe_pesado"):

            dano, critico = heroi.golpe_pesado(inimigo_atual)

            nome_habilidade = "Golpe Pesado"

        elif hasattr(heroi, "magia_fogo"):

            dano, critico = heroi.magia_fogo(inimigo_atual)

            nome_habilidade = "Magia de Fogo"

        elif hasattr(heroi, "curar"):

            cura, critico = heroi.curar(heroi)

            mensagem.configure(
                text=f"Você recuperou {cura} de vida!"
            )

            atualizar_status()
            atualizar_combate()

            turno_inimigo()
            return

        else:
            return

        texto = f"{nome_habilidade}: {dano} de dano!"

        if critico:
            texto += " ACERTO CRÍTICO!"

        mensagem.configure(text=texto)

        if verificar_vitoria():
            return

        turno_inimigo()
        desenhar_tabuleiro()

    except Exception as erro:

        CTkMessagebox(
            title="Erro",
            message=str(erro),
            icon="warning"
        )



def fugir():

    if not em_combate:
        return

    if heroi.tentar_fugir():

        mensagem.configure(text="Você conseguiu fugir!")

        finalizar_combate()

    else:

        mensagem.configure(text="Você não conseguiu fugir!")

        turno_inimigo()



def game_over():

    global em_combate

    em_combate = True

    CTkMessagebox(
        title="GAME OVER",
        message=f"{heroi.get_nome()} foi derrotado!",
        icon="warning"
    )

    janela.destroy()



ctk.CTkButton(
    botoes,
    text="Ataque Básico",
    width=15,
    command=ataque_basico
).grid(row=0, column=0, padx=5)


ctk.CTkButton(
    botoes,
    text="Habilidade Especial",
    width=18,
    command=habilidade_especial
).grid(row=0, column=1, padx=5)

ctk.CTkButton(
    botoes,
    text="Fugir",
    width=10,
    command=fugir
).grid(row=0, column=2, padx=5)



def criar_personagem():

    global heroi

    heroi = None

    nome = ctk.CTkInputDialog(
        title="Personagem",
        text="Digite o nome do seu personagem:"
    ).get_input()


    if not nome:
        janela.destroy()
        return
    
    classe = ctk.CTkInputDialog(
        title="Classe",
        text="Escolha sua classe:\n\n"
        "1 - Guerreiro\n"
        "2 - Mago\n"
        "3 - Sacerdote"
    ).get_input()
    
    
    if classe == "1":
        heroi = Guerreiro(nome)

    elif classe == "2":
        heroi = Mago(nome)

    elif classe == "3":
        heroi = Sacerdote(nome)

    else:
        janela.destroy()
        return

    
    mapa.posicionar_personagem(heroi, 0, 0)

    
    orc = Inimigo("Orc")
    mapa.posicionar_personagem(orc, 1, 1)

    atualizar_status()
    desenhar_tabuleiro()

    mensagem.configure(
        text="Use W, A, S, D para movimentar seu personagem!"
    )



janela.bind("<KeyPress>", mover_heroi)


criar_personagem()

janela.mainloop()
