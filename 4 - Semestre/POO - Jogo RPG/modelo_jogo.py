from abc import ABC, ABCMeta, abstractmethod
import random
from random import randint

class Tabuleiro:

    def __init__(self, largura: int = 15, altura: int = 15):
        self.largura = largura
        self.altura = altura
        self.entidades = {}

    def posicionar_personagem(self, personagem, x: int, y: int) -> bool:
        if 0 <= x < self.largura and 0 <= y < self.altura:

            for pos, lista in list(self.entidades.items()):
                if personagem in lista:
                    lista.remove(personagem)
                    if not lista:
                        del self.entidades[pos]

            if (x, y) not in self.entidades:
                self.entidades[(x, y)] = []
            self.entidades[(x, y)].append(personagem)

            personagem.posicao_x = x
            personagem.posicao_y = y
            return True
        return False

    def inimigos_na_posicao(self, jogador) -> list:
        """Retorna a lista de inimigos vivos na mesma casa do jogador."""
        pos = (jogador.posicao_x, jogador.posicao_y)
        lista = self.entidades.get(pos, [])
        return [p for p in lista if isinstance(p, Inimigo) and p.get_vida() > 0]

    def remover_personagem(self, personagem):
        """Remove o personagem do tabuleiro (ex.: inimigo derrotado)."""
        pos = (personagem.posicao_x, personagem.posicao_y)
        lista = self.entidades.get(pos, [])
        if personagem in lista:
            lista.remove(personagem)
            if not lista:
                del self.entidades[pos]


class Personagem(ABC):
    _nome: str
    _vida: int
    ataque: int
    defesa: int
    posicao_x: int
    posicao_y: int

    def __init__(self, nome: str, vida: int, ataque: int, defesa: int):
        self._nome = nome
        self._vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.posicao_x = 0
        self.posicao_y = 0

    def get_nome(self):
        return self._nome

    def get_subclasse(self):
        return type(self).__name__

    def get_vida(self):
        return self._vida

    def receber_dano(self, dano) -> int:
        """Aplica o dano e retorna o dano real sofrido (após a defesa)."""
        if self._vida == 0:
            raise Exception(f"{self._nome} morto.")
        dano_real = max(0, dano - self.defesa)
        self._vida -= dano_real
        return dano_real

    def atacar(self, alvo) -> int:
        """Ataca o alvo e retorna o dano real causado."""
        dado = random.randint(1, 6)
        dano_total = self.ataque + dado
        return alvo.receber_dano(dano_total)

    def receber_cura(self, cura) -> int:
        """Aplica a cura (máximo 100 de vida) e retorna o valor da cura."""
        if self._vida == 0:
            raise Exception(f"{self._nome} morto.")
        self._vida += cura
        if self._vida > 100:
            self._vida = 100
        return cura

    def tentar_fugir(self) -> bool:
        """Rola um dado; com 4 ou mais o personagem consegue fugir."""
        return random.randint(1, 6) >= 4

    def __str__(self):
        return f'{self._nome} : {self._vida}%\n'

    def mover(self, direcao: str, tabuleiro: Tabuleiro) -> str:
        """Move o personagem (W=cima, S=baixo, A=esquerda, D=direita).
        Retorna "morto", "parede" ou "ok"."""
        if self.get_vida() <= 0:
            return "morto"

        novo_x, novo_y = self.posicao_x, self.posicao_y

        if direcao.upper() == 'W':
            novo_y -= 1
        elif direcao.upper() == 'S':
            novo_y += 1
        elif direcao.upper() == 'D':
            novo_x += 1
        elif direcao.upper() == 'A':
            novo_x -= 1

        if 0 <= novo_x < tabuleiro.largura and 0 <= novo_y < tabuleiro.altura:
            tabuleiro.posicionar_personagem(self, novo_x, novo_y)
            return "ok"
        return "parede"


class Guerreiro(Personagem):

    def __init__(self, nome):
        super().__init__(nome=nome, vida=100, ataque=15, defesa=10)

    def golpe_pesado(self, alvo):
        dado = random.randint(1, 6)
        critico = dado == 6

        if critico:
            dano_extra = self.ataque * 3
        else:
            dano_extra = self.ataque * 1.5

        dano_real = alvo.receber_dano(int(dano_extra))
        return dano_real, critico

    def atacar(self, alvo):
        return super().atacar(alvo)


class Mago(Personagem):

    def __init__(self, nome):
        super().__init__(nome=nome, vida=100, ataque=10, defesa=5)
        self.mana = 100

    def magia_fogo(self, alvo):
        """Retorna (dano_real, critico)."""
        if self.mana >= 5:
            dado = random.randint(1, 6)
            critico = False

            if dado <= 2:
                dano_extra = self.ataque * 2
                self.mana -= 5
            elif 2 < dado <= 4:
                dano_extra = self.ataque * 3
                self.mana -= 3
            else:
                dano_extra = self.ataque * 4
                self.mana -= 2
                critico = True

            dano_real = alvo.receber_dano(int(dano_extra))
            return dano_real, critico
        else:
            raise Exception("Você não tem mana o suficiente.")

    def atacar(self, alvo):
        return super().atacar(alvo)


class Sacerdote(Personagem):

    def __init__(self, nome):
        super().__init__(nome, vida=100, ataque=5, defesa=5)
        self.mana = 100

    def curar(self, alvo):
        """Retorna (cura, critico)."""
        if self.mana >= 5:
            dado = random.randint(1, 6)
            critico = False

            if dado <= 2:
                cura = 5 * 2
                self.mana -= 5
            elif 2 < dado <= 4:
                cura = 5 * 3
                self.mana -= 5
            else:
                cura = 5 * 5
                self.mana -= 5
                critico = True

            alvo.receber_cura(int(cura))
            return cura, critico
        else:
            raise Exception("Você não tem mana o suficiente.")

    def atacar(self, alvo):
        return super().atacar(alvo)


class Inimigo(Personagem):

    def __init__(self, nome, vida=100, ataque=10, defesa=15):
        super().__init__(nome, vida, ataque, defesa)

    def atacar(self, alvo):
        return super().atacar(alvo)

DIFICULDADES = {
    "1": ("Fácil", 1),
    "2": ("Médio", 3),
    "3": ("Difícil", 5),
}


def criar_partida(nome: str, classe: str, dificuldade: str = "1"):
    classes = {
        "1": Guerreiro,
        "2": Mago,
        "3": Sacerdote,
    }
    classe_selecionada = classes.get(str(classe).strip())

    if classe_selecionada is None:
        raise ValueError("Classe inválida.")

    config = DIFICULDADES.get(str(dificuldade).strip())
    if config is None:
        raise ValueError("Dificuldade inválida.")
    _, qtd_inimigos = config
 
    mapa = Tabuleiro()
    heroi = classe_selecionada(nome)
    mapa.posicionar_personagem(heroi, 0, 0)
 
    casas_livres = [
        (x, y)
        for x in range(mapa.largura)
        for y in range(mapa.altura)
        if (x, y) != (0, 0)
    ]
    posicoes = random.sample(casas_livres, qtd_inimigos)
 
    inimigos = []
    for numero, (x, y) in enumerate(posicoes, start=1):
        inimigo = Inimigo(f"Orc {numero}")
        mapa.posicionar_personagem(inimigo, x, y)
        inimigos.append(inimigo)
 
    return mapa, heroi, inimigos