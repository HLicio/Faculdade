from modelo_jogo import Inimigo, criar_partida


def posicionar(mapa, personagem, x, y):
    if not mapa.posicionar_personagem(personagem, x, y):
        print("Posição fora dos limites do mapa!")


def desenhar_tabuleiro(mapa):
    """Exibe o tabuleiro com moldura e ícones customizados."""
    print("\n" + "═" * (mapa.largura * 3 + 3))
    for y in range(mapa.altura):
        linha = "║ "
        for x in range(mapa.largura):
            lista = mapa.entidades.get((x, y), [])
            jogadores_visiveis = [p for p in lista if not isinstance(p, Inimigo)]

            if jogadores_visiveis:
                linha += f"{jogadores_visiveis[0].get_nome()[0]} "
            else:
                linha += "· "
        linha += "║"
        print(linha)
    print("═" * (mapa.largura * 3 + 3) + "\n")


def mostrar_dano(alvo, dano_real):
    if alvo.get_vida() <= 0:
        print("Morreu")
    else:
        print(f"{alvo.get_nome()} recebeu {dano_real} de dano. Vida restante: {alvo.get_vida()}% ")


def iniciar_combate(jogador, inimigo, mapa):
    """Combate em turnos acionado pelas escolhas do jogador."""
    print(f"\n" + "⚔️ " * 15)
    print(f"   COMBATE INICIADO: {jogador.get_nome()} VS {inimigo.get_nome()}")
    print("⚔️ " * 15)

    while jogador.get_vida() > 0 and inimigo.get_vida() > 0:
        print(f"\n--- SEU TURNO ---")
        print(f"Sua Vida: {jogador.get_vida()}%")
        if hasattr(jogador, 'mana'):
            print(f"Sua Mana: {jogador.mana}")
        print(f"Vida do {inimigo.get_nome()}: {inimigo.get_vida()}%")

        print("\nEscolha sua ação:")
        print("1 - Ataque Básico")

        if hasattr(jogador, 'golpe_pesado'):
            print("2 - Usar Golpe Pesado")
        elif hasattr(jogador, 'magia_fogo'):
            print("2 - Usar Magia de Fogo (Custo: 5 Mana)")
        elif hasattr(jogador, 'curar'):
            print("2 - Usar Curar (Custo: 5 Mana)")

        print("3 - Tentar Fugir")

        opcao = input("Digite o número da sua ação: ").strip()

        if opcao == "1":
            dano_real = jogador.atacar(inimigo)
            mostrar_dano(inimigo, dano_real)

        elif opcao == "2":
            try:
                if hasattr(jogador, 'golpe_pesado'):
                    dano_real, critico = jogador.golpe_pesado(inimigo)
                    print(f"{jogador.get_nome()} usa golpe pesado no {inimigo.get_nome()}.")
                    if critico:
                        print("Dano Critico")
                    mostrar_dano(inimigo, dano_real)

                elif hasattr(jogador, 'magia_fogo'):
                    dano_real, critico = jogador.magia_fogo(inimigo)
                    print(f"{jogador.get_nome()} magia de fogo no {inimigo.get_nome()}.")
                    if critico:
                        print("Acerto Critico")
                    mostrar_dano(inimigo, dano_real)

                elif hasattr(jogador, 'curar'):
                    cura, critico = jogador.curar(jogador)
                    print(f"{jogador.get_nome()} usa cura em {jogador.get_nome()}.")
                    if critico:
                        print("Acerto Critico")
                    print(f"{jogador.get_nome()} foi curado em {cura} pontos. Vida atual: {jogador.get_vida()}%")
            except Exception as erro:
                # ex.: mana insuficiente — avisa e deixa o jogador escolher de novo
                print(erro)
                continue

        elif opcao == "3":
            if jogador.tentar_fugir():
                print(f"\n🏃 {jogador.get_nome()} conseguiu fugir do combate!")
                return
            else:
                print(f"\n❌ Falha ao fugir!")
        else:
            print("\nOpção inválida! Você perdeu a vez.")

        if inimigo.get_vida() > 0:
            print(f"\n--- TURNO DO INIMIGO ---")
            dano_real = inimigo.atacar(jogador)
            mostrar_dano(jogador, dano_real)

    if jogador.get_vida() <= 0:
        print(f"\n☠️ GAME OVER! {jogador.get_nome()} foi derrotado...")
    else:
        print(f"\n🏆 VI TÓ RIA! Você derrotou {inimigo.get_nome()}!")
        mapa.remover_personagem(inimigo)


def mover_heroi(heroi, comando, mapa):
    """Move o herói, exibe o resultado e inicia combate se houver encontro."""
    resultado = heroi.mover(comando, mapa)

    if resultado == "morto":
        print(f"{heroi.get_nome()} está morto e não pode andar.")
    elif resultado == "parede":
        print("Movimento inválido! Parede do mapa.")
    else:
        print(f"{heroi.get_nome()} moveu para ({heroi.posicao_x}, {heroi.posicao_y}).")

        for inimigo in mapa.inimigos_na_posicao(heroi):
            print(f"\n⚠️ ENCONTRO! {heroi.get_nome()} caiu na mesma casa que {inimigo.get_nome()}!")
            iniciar_combate(heroi, inimigo, mapa)
            if heroi.get_vida() <= 0:
                break


def rodar_jogo():

    print("--- CRIAÇÃO DE PERSONAGEM ---")

    subclasse = input("Digite (1) para Guerreiro, (2) para Mago e (3) para Sacerdote: ")
    nome = input("Digite o nome do seu Personagem: ")
    try:
        mapa, heroi, _ = criar_partida(nome, subclasse)
    except ValueError as erro:
        print(erro)
        return

    while heroi.get_vida() > 0:
        desenhar_tabuleiro(mapa)

        print(f"Posição Atual: ({heroi.posicao_x}, {heroi.posicao_y})")
        print("Comandos de Movimento: [W]Cima | [S]Baixo | [A]Esquerda | [D]Direita | [Q]Sair")
        comando = input("Para onde deseja ir? ").strip().upper()

        if comando in ['W', 'S', 'A', 'D']:
            mover_heroi(heroi, comando, mapa)
        elif comando == 'Q':
            print("Saindo do jogo...")
            break
        else:
            print("Comando inválido! Use W, S, A ou D.")


if __name__ == "__main__":
    rodar_jogo()