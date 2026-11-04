# ⚔️ RPG em Python - Programação Orientada a Objetos (POO)

Projeto acadêmico desenvolvido para a disciplina de **Programação Orientada a Objetos (POO)**. Trata-se de um jogo de RPG em turnos com exploração de mapa em grid, múltiplos arquétipos de personagens e mecânicas de combate baseadas em rolagens de dados (D6).

---

## 🎮 Modos de Jogo

O projeto conta com duas implementações complementares que utilizam o mesmo motor de regras de POO:

1. **Versão Terminal (CLI) — [`main.py`](./main.py)**:
   - Renderização do tabuleiro e molduras em texto (ASCII).
   - Menu textual interativo para seleção de ações de combate.
2. **Versão Interface Gráfica (GUI) — [`main2.py`](./main2.py)**:
   - Interface visual desenvolvida com a biblioteca nativa `tkinter`.
   - Grid interativo em Canvas com posicionamento do herói e inimigos.
   - Movimentação responsiva via teclado (`W`, `A`, `S`, `D`) e painel de combate com botões dinâmicos.

---

## 🏛️ Pilares de POO Aplicados

O design do projeto foi concebido para demonstrar na prática os fundamentos de Orientação a Objetos:

### 1. Abstração e Classes Abstratas
* A classe base **`Personagem`** (em [`classes.py`](./classes.py)) herda de `abc.ABC`, servindo como modelo primordial para qualquer entidade viva do jogo.
* Define os atributos essenciais (`_nome`, `_vida`, `ataque`, `defesa`, coordenadas `posicao_x` e `posicao_y`) e comportamentos universais (`receber_dano`, `receber_cura`, `mover`, `tentar_fugir`).

### 2. Encapsulamento
* Os atributos sensíveis como `_nome` e `_vida` são protegidos, sendo manipulados e consultados exclusivamente por métodos específicos (`get_nome()`, `get_vida()`, `receber_dano()`, `receber_cura()`).
* Regras de negócio como "vida máxima de 100%" ou "não receber dano negativo" são tratadas internamente nos métodos da classe.

### 3. Herança
* Classes especializadas derivam de `Personagem`, reaproveitando toda a lógica estrutural e chamando o construtor pai via `super().__init__(...)`:
  * **`Guerreiro`**: Foco em alta defesa física (10) e poder ofensivo (15).
  * **`Mago`**: Atributo adicional de gerenciamento de recursos (`mana = 100`).
  * **`Sacerdote`**: Equilíbrio defensivo e manipulação de cura divina via `mana`.
  * **`Inimigo`**: Criaturas hostis distribuídas no mapa com atributos configuráveis.

### 4. Polimorfismo e Especialização
* Cada arquétipo de personagem sobrescreve ou introduz habilidades exclusivas:
  * `Guerreiro.golpe_pesado(alvo)`: Dano massivo com probabilidade de acerto crítico (dano triplicado).
  * `Mago.magia_fogo(alvo)`: Escalonamento de dano mágico baseado na rolagem do dado (D6) consumindo mana.
  * `Sacerdote.curar(alvo)`: Capacidade de regeneração vital com rolagem crítica.

### 5. Associação e Composição de Ambiente
* A classe **`Tabuleiro`** gerencia o estado espacial do jogo:
  * Dicionário de entidades mapeado por coordenadas `(x, y)`.
  * Validação de limites do grid e detecção de colisões/encontros com inimigos.

---

## 🕹️ Como Executar

### Pré-requisitos
* Python 3.8 ou superior instalado.
* Nenhuma biblioteca externa é necessária (utiliza bibliotecas padrão `tkinter`, `random`, `abc`).

### Executando a Versão Terminal:
```bash
python main.py
```

### Executando a Versão Gráfica:
```bash
python main2.py
```

### Controles:
* **W**: Mover para Cima
* **S**: Mover para Baixo
* **A**: Mover para a Esquerda
* **D**: Mover para a Direita

---

## 📂 Estrutura de Arquivos

```text
POO - Jogo RPG/
├── classes.py      # Definição das classes, regras de POO, tabuleiro e combate
├── main.py         # Loop principal do jogo na versão Terminal
├── main2.py        # Interface gráfica com Tkinter e painéis interativos
└── README.md       # Documentação do projeto
```

---

## 📈 Histórico de Avaliações e Melhorias (Feedbacks do Professor)

| Semana / Data | Feedback / Proposta de Melhoria | Status |
|---|---|---|
| **Semana 1** | Versionar o projeto no GitHub e organizar a estrutura | ✅ Concluído |
| **Próximas** | _Acompanhamento contínuo das orientações em aula_ | ⏳ Em andamento |
