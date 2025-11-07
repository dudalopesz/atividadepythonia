# ChatTI — Simulador de Chatbot (Tkinter)

Aplicativo desktop em Python que simula um chatbot inteligente focado em assuntos de TI.

Funcionalidades
- Tela de login (credenciais definidas no código).
- Chat com exibição de nome e ícone (avatar) do usuário e do bot.
- Alternar tema: claro / escuro.
- Mensagens formatadas e atraso simulado nas respostas.

Como executar
1. Certifique-se de ter Python 3 instalado.
2. No terminal, execute:

```powershell
python app.py
```

Credenciais de exemplo (definidas em `app.py`):
- usuário: `aluno` / senha: `senha123`
- usuário: `usuario` / senha: `1234`

Dependências
- Este projeto usa apenas a biblioteca padrão do Python (Tkinter). Em alguns sistemas é necessário instalar o pacote `python3-tk`.

Observações
- O motor de respostas é simulado em `chatbot.py` e foca em tópicos de TI. Você pode integrar uma API real substituindo a função `get_response`.
