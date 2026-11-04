// main.c - Arquivo principal (front-end)
#include <stdio.h>
#include <direct.h> // Para criar diretório no Windows
#include "backend.h" // Inclui os protótipos e a struct
#include "frontend.h"

int main() {
    int opcao;
    char usuario[50];


    // Cria a pasta 'banco_de_dados' se ela não existir
    _mkdir("banco_de_dados");

    // Menu inicial: Cadastrar, Login ou Sair

    bemvindo();

    do {

        printf("\n1. Cadastrar\n2. Login\n3. Sair\nEscolha: ");
        scanf("%d", &opcao);
        limparBuffer(); // Evita problemas com o buffer do teclado

        switch (opcao) {
            case 1:
                cadastro_formatado();
                cadastrarUsuario(); // Cria novo usuário
                break;
            case 2:
                login_formatado();
                if (loginUsuario(usuario)) { // Se login for bem-sucedido
                    menuPrincipal(usuario);  // Mostra o menu principal
                }
                break;
            case 3:
                printf("Encerrando programa.\n");
                break;
            default:
                printf("Opcao invalida.\n");
        }
    } while (opcao != 3);

    return 0;
}


void menuPrincipal(char *usuario) {
    int opcao;
    do {
            void menu_formatado();
        printf("\nMenu Principal:\n");
        printf("1. Adicionar Tarefa\n");
        printf("2. Visualizar Tarefas\n");
        printf("3. Editar Tarefa\n");
        printf("4. Remover Tarefa\n");
        printf("5. Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1: adicionar_tarefas_formatado (); adicionarTarefa(usuario); break;
            case 2: visualizartarefas_formatado(); visualizarTarefas(usuario);  break;
            case 3: editartarefa_formatado(); editarTarefa(usuario); break;
            case 4: removertarefa_formatado(); removerTarefa(usuario); break;
            case 5: printf("Saindo...\n"); break;
            default: printf("Opcao invalida.\n");
        }
    } while (opcao != 5);
}
