import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from pathlib import Path
from PIL import Image, ImageTk

from modelo_jogo import Guerreiro, Inimigo, Mago, Sacerdote, Tabuleiro


class RPGApp(ctk.CTk):
    TAMANHO_CELULA = 30
    LARGURA = 15
    ALTURA = 15

    def __init__(self):
        super().__init__()

        self.title("RPG - Aventura")
        self.resizable(False, False)

        self.mapa = Tabuleiro(self.LARGURA, self.ALTURA)
        self.heroi = None
        self.em_combate = False
        self.inimigo_atual = None
        self.icones = self.carregar_icones()

        self.criar_widgets()
        self.bind("<KeyPress>", self.mover_heroi)
        self.after(0, self.criar_personagem)

    def carregar_icones(self):
        pasta_assets = Path(__file__).parent / "assets"
        tamanho = self.TAMANHO_CELULA - 4
        nomes = {
            "Guerreiro": "guerreiro.png",
            "Mago": "mago.png",
            "Sacerdote": "sarcedote.png",
            "Inimigo": "ORC.png",
        }
        icones = {}

        for tipo, nome in nomes.items():
            imagem = Image.open(pasta_assets / nome).convert("RGBA")
            imagem = imagem.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
            icones[tipo] = ImageTk.PhotoImage(imagem, master=self)

        return icones

    def criar_widgets(self):
        self.canvas = ctk.CTkCanvas(
            self,
            width=self.LARGURA * self.TAMANHO_CELULA,
            height=self.ALTURA * self.TAMANHO_CELULA,
            bg="white",
        )
        self.canvas.pack(padx=10, pady=10)

        self.informacoes = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.informacoes.pack()

        self.mensagem = ctk.CTkLabel(
            self,
            text="Use W, A, S, D para movimentar",
            font=("Arial", 11),
        )
        self.mensagem.pack(pady=5)

        self.painel_combate = ctk.CTkFrame(self)
        ctk.CTkLabel(
            self.painel_combate,
            text="COMBATE",
            font=("Arial", 16, "bold"),
        ).pack(pady=5)

        self.status_combate = ctk.CTkLabel(
            self.painel_combate,
            text="",
            font=("Arial", 11),
        )
        self.status_combate.pack(pady=5)

        botoes = ctk.CTkFrame(self.painel_combate)
        botoes.pack(pady=5)

        ctk.CTkButton(
            botoes,
            text="Ataque Básico",
            width=15,
            command=self.ataque_basico,
        ).grid(row=0, column=0, padx=5)
        ctk.CTkButton(
            botoes,
            text="Habilidade Especial",
            width=18,
            command=self.habilidade_especial,
        ).grid(row=0, column=1, padx=5)
        ctk.CTkButton(
            botoes,
            text="Fugir",
            width=10,
            command=self.fugir,
        ).grid(row=0, column=2, padx=5)

    def desenhar_tabuleiro(self):
        self.canvas.delete("all")

        for y in range(self.ALTURA):
            for x in range(self.LARGURA):
                x1 = x * self.TAMANHO_CELULA
                y1 = y * self.TAMANHO_CELULA
                x2 = x1 + self.TAMANHO_CELULA
                y2 = y1 + self.TAMANHO_CELULA

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="#e8e8e8", outline="black"
                )

                personagens = [
                    personagem
                    for personagem in self.mapa.entidades.get((x, y), [])
                    if personagem.get_vida() > 0
                ]

                for indice, personagem in enumerate(personagens):
                    tipo = self.tipo_icone(personagem)
                    if tipo is None:
                        continue

                    deslocamento = 0
                    if len(personagens) > 1:
                        deslocamento = -8 if indice == 0 else 8

                    self.canvas.create_image(
                        x1 + self.TAMANHO_CELULA // 2 + deslocamento,
                        y1 + self.TAMANHO_CELULA // 2,
                        image=self.icones[tipo],
                    )

    def tipo_icone(self, personagem):
        if isinstance(personagem, Inimigo):
            return "Inimigo"
        if isinstance(personagem, Guerreiro):
            return "Guerreiro"
        if isinstance(personagem, Mago):
            return "Mago"
        if isinstance(personagem, Sacerdote):
            return "Sacerdote"
        return None

    def atualizar_status(self):
        if self.heroi is None:
            return

        texto = (
            f"{self.heroi.get_nome()} | "
            f"Vida: {self.heroi.get_vida()}% | "
            f"Posição: ({self.heroi.posicao_x}, {self.heroi.posicao_y})"
        )
        if hasattr(self.heroi, "mana"):
            texto += f" | Mana: {self.heroi.mana}"
        self.informacoes.configure(text=texto)

    def mover_heroi(self, event):
        if self.em_combate or self.heroi is None:
            return

        tecla = event.keysym.upper()
        if tecla not in ["W", "A", "S", "D"]:
            return

        resultado = self.heroi.mover(tecla, self.mapa)
        if resultado == "morto":
            self.mensagem.configure(text="Você está morto!")
            return
        if resultado == "parede":
            self.mensagem.configure(text="Você encontrou uma parede!")
            return

        self.mensagem.configure(
            text=f"Você se moveu para ({self.heroi.posicao_x}, {self.heroi.posicao_y})"
        )
        self.desenhar_tabuleiro()
        self.atualizar_status()

        inimigos = self.mapa.inimigos_na_posicao(self.heroi)
        if inimigos:
            self.iniciar_combate(inimigos[0])

    def iniciar_combate(self, inimigo):
        self.em_combate = True
        self.inimigo_atual = inimigo
        self.mensagem.configure(text=f"Você encontrou {inimigo.get_nome()}!")
        self.painel_combate.pack(pady=10)
        self.atualizar_combate()
        self.desenhar_tabuleiro()

    def atualizar_combate(self):
        if self.inimigo_atual is None:
            return
        self.status_combate.configure(
            text=(
                f"Sua vida: {self.heroi.get_vida()}% | "
                f"Vida do inimigo: {self.inimigo_atual.get_vida()}%"
            )
        )

    def finalizar_combate(self):
        self.em_combate = False
        self.inimigo_atual = None
        self.painel_combate.pack_forget()
        self.atualizar_status()
        self.desenhar_tabuleiro()

    def turno_inimigo(self):
        if self.heroi.get_vida() <= 0:
            self.game_over()
            return

        dano = self.inimigo_atual.atacar(self.heroi)
        self.mensagem.configure(text=f"O inimigo causou {dano} de dano!")

        if self.heroi.get_vida() <= 0:
            self.atualizar_status()
            self.game_over()
            return

        self.atualizar_combate()
        self.atualizar_status()

    def verificar_vitoria(self):
        if self.inimigo_atual.get_vida() > 0:
            return False

        nome = self.inimigo_atual.get_nome()
        self.mapa.remover_personagem(self.inimigo_atual)
        CTkMessagebox(
            master=self,
            title="Vitória!",
            message=f"Você derrotou {nome}!",
            icon="check",
        )
        self.finalizar_combate()
        return True

    def ataque_basico(self):
        if not self.em_combate:
            return

        dano = self.heroi.atacar(self.inimigo_atual)
        self.mensagem.configure(text=f"Você causou {dano} de dano!")
        if self.verificar_vitoria():
            return
        self.turno_inimigo()
        self.desenhar_tabuleiro()

    def habilidade_especial(self):
        if not self.em_combate:
            return

        try:
            if hasattr(self.heroi, "golpe_pesado"):
                dano, critico = self.heroi.golpe_pesado(self.inimigo_atual)
                nome_habilidade = "Golpe Pesado"
            elif hasattr(self.heroi, "magia_fogo"):
                dano, critico = self.heroi.magia_fogo(self.inimigo_atual)
                nome_habilidade = "Magia de Fogo"
            elif hasattr(self.heroi, "curar"):
                cura, critico = self.heroi.curar(self.heroi)
                self.mensagem.configure(text=f"Você recuperou {cura} de vida!")
                self.atualizar_status()
                self.atualizar_combate()
                self.turno_inimigo()
                return
            else:
                return

            texto = f"{nome_habilidade}: {dano} de dano!"
            if critico:
                texto += " ACERTO CRÍTICO!"
            self.mensagem.configure(text=texto)

            if self.verificar_vitoria():
                return
            self.turno_inimigo()
            self.desenhar_tabuleiro()
        except Exception as erro:
            CTkMessagebox(
                master=self,
                title="Erro",
                message=str(erro),
                icon="warning",
            )

    def fugir(self):
        if not self.em_combate:
            return

        if self.heroi.tentar_fugir():
            self.mensagem.configure(text="Você conseguiu fugir!")
            self.finalizar_combate()
        else:
            self.mensagem.configure(text="Você não conseguiu fugir!")
            self.turno_inimigo()

    def game_over(self):
        self.em_combate = True
        CTkMessagebox(
            master=self,
            title="GAME OVER",
            message=f"{self.heroi.get_nome()} foi derrotado!",
            icon="warning",
        )
        self.destroy()

    def criar_personagem(self):
        self.heroi = None
        nome = ctk.CTkInputDialog(
            title="Personagem",
            text="Digite o nome do seu personagem:",
        ).get_input()
        if not nome:
            self.destroy()
            return

        classe = ctk.CTkInputDialog(
            title="Classe",
            text=(
                "Escolha sua classe:\n\n"
                "1 - Guerreiro\n"
                "2 - Mago\n"
                "3 - Sacerdote"
            ),
        ).get_input()

        classes = {
            "1": Guerreiro,
            "2": Mago,
            "3": Sacerdote,
        }
        classe_selecionada = classes.get(classe)
        if classe_selecionada is None:
            self.destroy()
            return

        self.heroi = classe_selecionada(nome)
        self.mapa.posicionar_personagem(self.heroi, 0, 0)
        self.mapa.posicionar_personagem(Inimigo("Orc"), 1, 1)
        self.atualizar_status()
        self.desenhar_tabuleiro()
        self.mensagem.configure(
            text="Use W, A, S, D para movimentar seu personagem!"
        )




