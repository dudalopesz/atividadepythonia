"""Módulo com lógica de respostas simuladas focadas em assuntos de TI.
Função pública: get_response(message: str) -> str
"""
import time
import random
import re
from difflib import get_close_matches


_KB = {
    "python": (
        "Parece que você está falando de Python. Dicas rápidas:\n"
        "- Instalar pacotes: `pip install <pacote>`\n"
        "- Ambientes virtuais: `python -m venv venv` e `venv\\Scripts\\activate` (Windows) / `source venv/bin/activate` (Linux)\n"
        "- Frameworks: use `django` para aplicações completas, `flask` para microserviços.\n"
        "Se tiver um erro, cole o traceback que eu ajudo a interpretar."
    ),
    "git": (
        "Git — comandos essenciais:\n"
        "- `git status` : ver mudanças\n"
        "- `git add .` e `git commit -m 'mensagem'` : salvar alterações\n"
        "- `git push` e `git pull` : sincronizar com remoto\n"
        "Se tiver conflito, leia o arquivo marcado e resolva, depois `git add` + `git commit`."
    ),
    "linux": (
        "Linux / terminal — dicas:\n"
        "- Navegação: `ls`, `cd`, `pwd`\n"
        "- Procurar: `grep -R 'texto' .`\n"
        "- Pacotes (Debian/Ubuntu): `sudo apt update && sudo apt install <pacote>`\n"
        "Se precisar de um comando específico, diga o que quer fazer."
    ),
    "network": (
        "Rede — diagnóstico básico:\n"
        "- Windows: `ipconfig /all` ; Linux: `ip addr`\n"
        "- Teste de latência: `ping <host>`\n"
        "- DNS: `nslookup <host>` ou `dig <host>`\n"
        "Forneça saídas de `ping`/`ipconfig` se quiser uma análise."
    ),
    "docker": (
        "Docker básico:\n"
        "- `docker build -t minha-app .`\n"
        "- `docker run -p 80:80 minha-app`\n"
        "- Para ver containers: `docker ps -a`\n"
        "Se quiser um Dockerfile de exemplo, diga qual tecnologia (Python, Node, etc.)."
    ),
    "debug": (
        "Debugging:\n"
        "- Isole o menor caso reproduzível\n"
        "- Leia o traceback (o primeiro erro útil geralmente aparece no final)\n"
        "- Use prints/logging ou um depurador (pdb para Python)\n"
    ),
}


_DEFS = {
    "hardware": "Hardware são os componentes físicos de um computador ou dispositivo, como CPU, memória RAM, disco rígido, placa-mãe, etc.",
    "software": "Software são os programas, sistemas e aplicativos que rodam em um computador, incluindo sistema operacional e aplicações.",
    "ram": "RAM (Random Access Memory) é a memória principal do computador, usada para armazenar dados temporários durante a execução de programas.",
    "cpu": "CPU (Unidade Central de Processamento) é o 'cérebro' do computador, responsável por executar instruções e cálculos.",
    "gpu": "GPU (Unidade de Processamento Gráfico) é um processador especializado em renderizar gráficos e fazer cálculos paralelos.",
    "ssd": "SSD (Solid State Drive) é um tipo de armazenamento mais rápido que HD tradicional, sem partes móveis.",
    "rede": "Rede de computadores é um conjunto de dispositivos conectados que podem trocar dados entre si, como a Internet.",
    "internet": "Internet é uma rede global de computadores interconectados usando protocolos padrão como TCP/IP.",
    "wifi": "Wi-Fi é uma tecnologia de rede sem fio que permite conectar dispositivos à Internet usando ondas de rádio.",
    "bluetooth": "Bluetooth é uma tecnologia de comunicação sem fio para troca de dados entre dispositivos próximos.",
    "linux": "Linux é um kernel de sistema operacional livre usado em muitas distribuições como Ubuntu, Red Hat e Android.",
    "windows": "Windows é um sistema operacional da Microsoft, conhecido por sua interface gráfica e compatibilidade com softwares.",
    "mac": "macOS é o sistema operacional da Apple para computadores Mac, conhecido por design e integração com iOS.",
    "android": "Android é um sistema operacional móvel baseado em Linux, usado na maioria dos smartphones.",
    "ios": "iOS é o sistema operacional móvel da Apple, usado em iPhones e iPads.",
    "git": "Git é um sistema de controle de versão que permite rastrear mudanças em código e colaborar em projetos.",
    "github": "GitHub é uma plataforma de hospedagem de código que usa Git, permitindo colaboração em projetos de software.",
    "api": "API (Interface de Programação de Aplicações) é um conjunto de regras que permite diferentes softwares se comunicarem.",
    "rest": "REST é um estilo de arquitetura para APIs web que usa HTTP para comunicação entre sistemas.",
    "http": "HTTP é o protocolo usado para transferir dados na web, como quando você acessa um site.",
    "https": "HTTPS é a versão segura do HTTP, que criptografa dados entre seu navegador e o site.",
    "dns": "DNS converte nomes de domínio (como google.com) em endereços IP que computadores usam para se comunicar.",
    "ip": "IP (Protocolo de Internet) é o endereço único que identifica dispositivos em uma rede.",
    "servidor": "Servidor é um computador ou sistema que fornece recursos, dados ou serviços para outros computadores na rede.",
    "cliente": "Cliente é um programa ou dispositivo que acessa recursos ou serviços fornecidos por um servidor.",
    "database": "Banco de Dados é um sistema organizado para armazenar, gerenciar e recuperar informações.",
    "sql": "SQL é a linguagem padrão para manipular bancos de dados relacionais, usada para consultas e atualizações.",
    "nosql": "NoSQL são bancos de dados não relacionais, flexíveis para dados não estruturados como MongoDB e Redis.",
    "frontend": "Frontend é a parte visual de um software ou site, com a qual os usuários interagem diretamente.",
    "backend": "Backend é a parte do sistema que processa dados nos servidores, invisível aos usuários.",
    "fullstack": "Full Stack é o desenvolvimento que abrange tanto frontend quanto backend de aplicações.",
    "bug": "Bug é um erro ou falha em um programa que faz ele funcionar incorretamente ou travar.",
    "debug": "Debug é o processo de encontrar e corrigir bugs (erros) em um programa.",
    "algoritmo": "Algoritmo é uma sequência de passos lógicos para resolver um problema ou realizar uma tarefa.",
    "codigo": "Código ou código-fonte são as instruções escritas em linguagem de programação para criar programas.",
    "compilador": "Compilador traduz código escrito em linguagem de programação para linguagem de máquina executável.",
    "ide": "IDE (Ambiente de Desenvolvimento) é um software que ajuda a escrever e testar código, como VS Code.",
    "javascript": "JavaScript é uma linguagem de programação principalmente usada para criar sites interativos.",
    "python": "Python é uma linguagem de programação popular, fácil de aprender e versátil.",
    "java": "Java é uma linguagem de programação versátil usada em Android, servidores e aplicações empresariais.",
    "docker": "Docker permite empacotar aplicações e dependências em containers para fácil distribuição.",
    "container": "Container é um pacote de software que inclui tudo necessário para executar uma aplicação.",
    "cloud": "Cloud Computing é o fornecimento de serviços de computação pela Internet (servidores, armazenamento, etc).",
    "aws": "AWS (Amazon Web Services) é uma plataforma de serviços em nuvem líder no mercado.",
    "devops": "DevOps é uma cultura que une desenvolvimento de software com operações de TI.",
    "agile": "Agile é uma abordagem de desenvolvimento de software que prioriza entregas incrementais e adaptação.",
    "scrum": "Scrum é um framework ágil para gerenciar projetos complexos, comum em desenvolvimento de software.",
    "seguranca": "Segurança em TI envolve proteger sistemas, redes e dados contra ameaças e acessos não autorizados.",
    "firewall": "Firewall é uma barreira de segurança que controla o tráfego de rede, bloqueando acessos suspeitos.",
    "backup": "Backup é uma cópia de segurança de dados para prevenir perdas em caso de falhas.",
    "virus": "Vírus é um programa malicioso que pode danificar sistemas e roubar dados.",
    "criptografia": "Criptografia é a técnica de proteger informações convertendo-as em código secreto.",
    "blockchain": "Blockchain é uma tecnologia de registro distribuído, base de criptomoedas como Bitcoin.",
    "programacao": "Programação é a arte de criar instruções para computadores executarem tarefas.",
    "programar": "Programar é criar instruções (código) para fazer computadores realizarem tarefas.",
    "computador": "Computador é uma máquina eletrônica que processa dados seguindo instruções programadas.",
    "tecnologia": "Tecnologia da Informação (TI) é a área que lida com computadores, redes e processamento de dados.",
    "desenvolvedor": "Desenvolvedor ou programador é um profissional que cria software e aplicações.",
    "programador": "Programador é quem escreve código para criar programas de computador.",
    "computacao": "Computação é a ciência que estuda processamento de informações usando computadores.",
    "informatica": "Informática é o estudo e uso de computadores e tecnologias digitais.",
    "linguagem": "Linguagem de programação é um conjunto de regras para escrever instruções que o computador entende.",
    "html": "HTML é a linguagem de marcação usada para estruturar conteúdo em páginas web.",
    "css": "CSS é a linguagem de estilos usada para definir a aparência (layout, cores, fontes) de páginas web."
}


_DEFS.update({
    "javascript": "JavaScript é uma linguagem de programação que roda principalmente em navegadores e também no servidor (Node.js); é usada para tornar páginas web interativas.",
    "js": "JavaScript (JS) é a linguagem usada para programação web no cliente e também no servidor via Node.js.",
    "html": "HTML é a linguagem de marcação usada para estruturar conteúdo em páginas web.",
    "css": "CSS é a linguagem de estilos usada para definir a aparência (layout, cores, fontes) de páginas web.",
    "sql": "SQL é uma linguagem para consultar e manipular bancos de dados relacionais (ex: SELECT, INSERT, UPDATE).",
    "database": "Database (banco de dados) é um local estruturado para armazenar e consultar dados; pode ser relacional (Postgres, MySQL) ou NoSQL (MongoDB).",
    "node": "Node.js é um ambiente de execução JavaScript para construir aplicações de servidor e ferramentas de linha de comando.",
    "nodejs": "Node.js permite executar JavaScript fora do navegador, muito usado em backends e ferramentas de desenvolvimento.",
})

def _find_best_topic(tokens):
    
    for t in tokens:
        if t in _KB:
            return t

    
    joined = " ".join(tokens)
    choices = list(_KB.keys())
    close = get_close_matches(joined, choices, n=1, cutoff=0.6)
    if close:
        return close[0]

    
    for t in tokens:
        close = get_close_matches(t, choices, n=1, cutoff=0.7)
        if close:
            return close[0]

    return None


def get_response(message: str) -> str:
    """Gera uma resposta mais robusta sobre tópicos de TI usando regras e correspondência aproximada.

    Regras:
    - Tokeniza a mensagem
    - Tenta mapear para um tópico conhecido em _KB
    - Se não encontrar, busca por padrões (ex.: erros, comandos, perguntas abertas)
    - Caso indefinido, pede clarificação
    """
    msg = (message or "").strip()
    if not msg:
        return "Não recebi uma pergunta — diga algo sobre TI ou descreva o problema que você tem."

    low = msg.lower()
    
    tokens = re.findall(r"[a-zA-Z0-9_+-]+", low)

    
    if "traceback" in low or "exception" in low or "erro" in low or "error" in low:
        return (
            "Parece um problema de execução. Cole aqui o traceback ou descreva o erro completo.\n"
            "Enquanto isso, verifique a linha apontada no traceback e as importações/versões dos pacotes."
        )


    if re.search(r"como (instalar|faço|faco|usar)", low):
        
        topic = _find_best_topic(tokens)
        if topic and topic in _KB:
            return _KB[topic]
        return "Você quer instruções de instalação para qual tecnologia? (ex: Python, Docker, Node)"

    if re.search(r"o que é|oque é|o que e|definição|significa", low):
        
        m = re.search(r"(?:o que|oque)\s+(?:e|é)\s+(?:o|a|um|uma)?\s*([a-zA-Z0-9_+\-]+)", low)
        if m:
            key = m.group(1).strip().lower()
            
            key = re.sub(r"[^a-z0-9]", "", key)
          
            if key in _DEFS:
                return _DEFS[key]
            close = get_close_matches(key, list(_DEFS.keys()), n=1, cutoff=0.7)
            if close:
                return _DEFS[close[0]]
          
            topic = _find_best_topic(tokens)
            if topic and topic in _KB:
                return _KB[topic].split("\n")[0]
        return "Sobre qual conceito você quer a definição? (ex: Docker, Kubernetes, Git, VM, container, JavaScript)"

    topic = _find_best_topic(tokens)
    if topic:
        return _KB[topic]

    if any(k in low for k in ("ping", "ipconfig", "nslookup", "dig", "tracert", "traceroute")):
        return (
            "Para diagnóstico de rede, rode o comando apropriado e cole a saída aqui. Exemplos:\n"
            "- Windows: `ipconfig /all`\n"
            "- Ping: `ping 8.8.8.8`\n"
            "- DNS: `nslookup exemplo.com`\n"
        )

    generic = [
        "Explique em mais detalhes: qual sistema operacional, linguagem e o que você já tentou?",
        "Dê um exemplo do comando/erro que você está vendo, assim eu posso sugerir uma correção precisa.",
        "Posso ajudar com comandos passo a passo, exemplos de código ou diagnósticos — qual você prefere?",
    ]
    return random.choice(generic)
