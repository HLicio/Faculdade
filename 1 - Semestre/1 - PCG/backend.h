#ifndef BACKEND_H
#define BACKEND_H

#define MAX_TAREFAS 100
#define MAX_LINHA 256

typedef struct {
    char nome[100];
    char descricao[200];
    char data[20];
} Tarefa;

void limparBuffer();
void cadastrarUsuario();
int loginUsuario(char usuario[]);
void adicionarTarefa(char *usuario);
void visualizarTarefas(char *usuario);
void editarTarefa(char *usuario);
void removerTarefa(char *usuario);
void menuPrincipal();
void menu();

#endif
