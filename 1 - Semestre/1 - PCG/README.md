# 📚 Sistema de Gerenciamento de Tarefas em C

Bem-vindo ao projeto de **Gerenciamento de Tarefas** desenvolvido em C!  
Aqui você encontra um sistema simples, didático e modular, ideal para quem está aprendendo lógica de programação, manipulação de arquivos e boas práticas em C.

---

## 🗂 Estrutura dos Arquivos

| Arquivo         | Função Principal                                         |
|-----------------|---------------------------------------------------------|
| `main.c`        | 🚦 Ponto de entrada, menus iniciais e fluxo principal   |
| `backend.c/h`   | ⚙️ Lógica do sistema: cadastro, login e tarefas         |
| `frontend.c/h`  | 🎨 Visual dos menus, formatação e feedback ao usuário   |

---

## 💻 Como Funciona

O programa simula um gerenciador de tarefas pessoal, onde cada usuário possui seu próprio arquivo de dados.

### 🔐 Cadastro & Login

- 👤 Crie sua conta com nome único (min. 3 letras) e senha (min. 6 letras)
- 🔑 Faça login com até 3 tentativas
- 🗄 Dados salvos em arquivos na pasta `banco_de_dados/`

### 🏠 Menu Principal

Após o login, você terá as seguintes opções:

- ➕ **Adicionar Tarefa**: registre uma tarefa com nome, descrição e data 📅
- 👀 **Visualizar Tarefas**: veja todas suas tarefas organizadas por data
- ✏️ **Editar Tarefa**: altere nome, descrição ou data da tarefa
- 🗑 **Remover Tarefa**: exclua tarefas que não precisa mais
- 🚪 **Sair**: encerre seu acesso ao sistema

---

## 🧩 Organização dos Arquivos

### `main.c`
- Inclui headers do front e back-end
- Garante que a pasta `banco_de_dados` exista
- Mostra menus de cadastro/login e chama o menu principal após login

### `backend.c / backend.h`
- Define a struct `Tarefa` (nome, descrição, data)
- Funções:
  - 👤 Cadastro e login de usuário
  - ➕ Adicionar tarefa
  - 👀 Visualizar tarefas
  - ✏️ Editar tarefa
  - 🗑 Remover tarefa
- Todas as operações são feitas via arquivos `.txt` individuais por usuário

### `frontend.c / frontend.h`
- Telas e menus com arte em ASCII e cores no terminal (Windows)
- Mensagens de boas-vindas e feedback visual para cada ação

---

## ⚙️ Como Compilar e Executar

No Windows, usando GCC (MinGW):

```sh
gcc main.c backend.c frontend.c -o gerenciador.exe
./gerenciador.exe
```

---

## ℹ️ Observações

- Sistema simples; utiliza arquivos texto
- Projeto para fins didáticos do PCG do 1º semestre de Ciências da Computação (PCG)
- Uso de `system("color")` e `system("cls")` para efeitos visuais no terminal do Windows

---

## 👨‍💻 Feito por

Rhuan Miguel, Yasmin Vitória, Miguel Dantas, Francisco Coutinho, Eduarda Gonçalves, João Matheus

---
