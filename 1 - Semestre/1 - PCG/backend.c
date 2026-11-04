// backend.c - Lógica do sistema (back-end)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <direct.h>
#include "backend.h"

// Função auxiliar para limpar o buffer do teclado
void limparBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

// Cadastro de novo usuário com validações
void cadastrarUsuario() {
    char usuario[50], senha[50], nomeArquivo[60];
    FILE *f;

    // Loop para garantir nome de usuário válido e não existente
    while (1) {
        printf("Digite o nome de usuario (minimo 3 caracteres): ");
        fgets(usuario, sizeof(usuario), stdin);
        usuario[strcspn(usuario, "\n")] = 0;

        if (strlen(usuario) < 3) {
            printf("O nome de usuario deve ter no minimo 3 caracteres.\n");
            continue;
        }

        sprintf(nomeArquivo, "banco_de_dados/%s.txt", usuario);
        f = fopen(nomeArquivo, "r");
        if (f) {
            fclose(f);
            printf("Usuario ja existe. Tente outro nome.\n");
            continue;
        }

        break; // Usuário válido e disponível
    }

    // Loop para garantir senha válida
    while (1) {
        printf("Digite a senha (minimo 6 caracteres): ");
        fgets(senha, sizeof(senha), stdin);
        senha[strcspn(senha, "\n")] = 0;

        if (strlen(senha) < 6) {
            system("color 04"); // Alerta visual (vermelho)
            printf("A senha deve ter no minimo 6 caracteres.\n");
            continue;
        }

        break;
    }

    // Criação do arquivo do usuário e escrita da senha
    f = fopen(nomeArquivo, "w");
    if (f) {
        fprintf(f, "senha: %s\n", senha);
        fclose(f);
        printf("Cadastro realizado com sucesso!\n");
        menuPrincipal(usuario);
    } else {
        printf("Erro ao criar arquivo do usuario.\n");
    }
}

// Função para autenticar login do usuário com até 3 tentativas
int loginUsuario(char usuario[]) {
    char senha[50], senhaSalva[50];
    int tentativa = 3;
    FILE *f;
    char nomeArquivo[60];

    // Solicita o nome de usuário até que seja encontrado
    while (1) {
        printf("Digite o nome de usuario: ");
        fgets(usuario, 50, stdin);
        usuario[strcspn(usuario, "\n")] = 0;

        sprintf(nomeArquivo, "banco_de_dados/%s.txt", usuario);

        f = fopen(nomeArquivo, "r");
        if (!f) {
            printf("Usuario nao encontrado.\n");
        } else {
            break; // usuário encontrado, sai do loop
        }
    }

    // Lê a linha da senha do arquivo
    fgets(senhaSalva, sizeof(senhaSalva), f);
    senhaSalva[strcspn(senhaSalva, "\n")] = 0;
    fclose(f);

    // Loop de tentativa de senha
    while (tentativa > 0) {
        printf("Digite a senha: ");
        fgets(senha, sizeof(senha), stdin);
        senha[strcspn(senha, "\n")] = 0;

        // Verifica se a senha corresponde
        if (strstr(senhaSalva, senha) != NULL) {
            return 1; // Login bem-sucedido
        } else {
            tentativa--;
            printf("Senha incorreta. Tentativas restantes: %d\n", tentativa);
        }
    }

    return 0; // Falhou nas tentativas
}


// Função para adicionar nova tarefa ao arquivo do usuário
void adicionarTarefa(char *usuario) {
    char nomeArquivo[60];
    sprintf(nomeArquivo, "banco_de_dados/%s.txt", usuario);
    FILE *file = fopen(nomeArquivo, "a");
    if (!file) {
        printf("Erro ao abrir o arquivo do usuario.\n");
        return;
    }

    Tarefa t;
    limparBuffer();
    printf("Nome da tarefa: ");
    fgets(t.nome, sizeof(t.nome), stdin);
    t.nome[strcspn(t.nome, "\n")] = 0;

    printf("Descricao: ");
    fgets(t.descricao, sizeof(t.descricao), stdin);
    t.descricao[strcspn(t.descricao, "\n")] = 0;

    printf("Data (DD/MM/AAAA): ");
    scanf("%s", t.data);

    fprintf(file, "Tarefa: %s | Descricao: %s | Data: %s\n", t.nome, t.descricao, t.data);
    fclose(file);
}

// Função auxiliar para ordenação de tarefas por data
int compararTarefas(const void *a, const void *b) {
    const Tarefa *ta = (const Tarefa *)a;
    const Tarefa *tb = (const Tarefa *)b;
    return strcmp(ta->data, tb->data);
}

// Lê as tarefas do arquivo para um vetor em memória
int carregarTarefas(char *usuario, Tarefa tarefas[]) {
    char nomeArquivo[60], linha[MAX_LINHA];
    int count = 0;
    sprintf(nomeArquivo, "banco_de_dados/%s.txt", usuario);

    FILE *file = fopen(nomeArquivo, "r");
    if (!file) return 0;

    fgets(linha, MAX_LINHA, file); // pula a linha da senha

    while (fgets(linha, MAX_LINHA, file)) {
        sscanf(linha, "Tarefa: %[^\n|] | Descricao: %[^\n|] | Data: %[^\n]", tarefas[count].nome, tarefas[count].descricao, tarefas[count].data);
        count++;
    }

    fclose(file);
    return count;
}

// Salva todas as tarefas sobrescrevendo o arquivo (mantém senha)
void salvarTarefas(char *usuario, Tarefa tarefas[], int n) {
    char nomeArquivo[60];
    sprintf(nomeArquivo, "banco_de_dados/%s.txt", usuario);

    FILE *file = fopen(nomeArquivo, "r");
    if (!file) {
        printf("Erro ao abrir o arquivo original.\n");
        return;
    }

    char senhaLinha[MAX_LINHA];
    fgets(senhaLinha, MAX_LINHA, file);
    fclose(file);

    file = fopen("banco_de_dados/temp.txt", "w");
    if (!file) {
        printf("Erro ao criar arquivo temporário.\n");
        return;
    }

    fputs(senhaLinha, file);
    for (int i = 0; i < n; i++) {
        fprintf(file, "Tarefa: %s | Descricao: %s | Data: %s\n", tarefas[i].nome, tarefas[i].descricao, tarefas[i].data);
    }
    fclose(file);

    remove(nomeArquivo);
    rename("banco_de_dados/temp.txt", nomeArquivo);
}

// Exibe todas as tarefas ordenadas por data
void visualizarTarefas(char *usuario) {
    Tarefa tarefas[MAX_TAREFAS];
    int n = carregarTarefas(usuario, tarefas);
    qsort(tarefas, n, sizeof(Tarefa), compararTarefas);
    for (int i = 0; i < n; i++) {
        printf("%d. Tarefa: %s | Descricao: %s | Data: %s\n", i + 1, tarefas[i].nome, tarefas[i].descricao, tarefas[i].data);
    }
}

// Permite editar uma tarefa existente
void editarTarefa(char *usuario) {
    Tarefa tarefas[MAX_TAREFAS];
    int n = carregarTarefas(usuario, tarefas);
    visualizarTarefas(usuario);

    printf("Digite o numero da tarefa que deseja editar: ");
    int op;
    scanf("%d", &op);
    limparBuffer();

    if (op < 1 || op > n) {
        printf("Opcao invalida.\n");
        return;
    }

    printf("Novo nome da tarefa: ");
    fgets(tarefas[op - 1].nome, sizeof(tarefas[op - 1].nome), stdin);
    tarefas[op - 1].nome[strcspn(tarefas[op - 1].nome, "\n")] = 0;

    printf("Nova descricao: ");
    fgets(tarefas[op - 1].descricao, sizeof(tarefas[op - 1].descricao), stdin);
    tarefas[op - 1].descricao[strcspn(tarefas[op - 1].descricao, "\n")] = 0;

    printf("Nova data: ");
    scanf("%s", tarefas[op - 1].data);

    salvarTarefas(usuario, tarefas, n);
}

// Remove uma tarefa selecionada pelo usuário
void removerTarefa(char *usuario) {
    Tarefa tarefas[MAX_TAREFAS];
    int n = carregarTarefas(usuario, tarefas);
    visualizarTarefas(usuario);

    printf("Digite o numero da tarefa que deseja remover: ");
    int op;
    scanf("%d", &op);

    if (op < 1 || op > n) {
        printf("Opcao invalida.\n");
        return;
    }

    for (int i = op - 1; i < n - 1; i++) {
        tarefas[i] = tarefas[i + 1];
    }

    salvarTarefas(usuario, tarefas, n - 1);
}
