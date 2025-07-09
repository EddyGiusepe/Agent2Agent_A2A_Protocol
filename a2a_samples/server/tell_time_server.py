#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Run
---
uv run tell_time_server.py
"""
# Importar a classe Flask e funções utilitárias do pacote flask.
# Flask é um framework web leve usado para construir APIs HTTP e servidores web em Python.
from flask import Flask, request, jsonify
# Importar a classe datetime do módulo built-in datetime do Python.
# Usaremos isso para obter a data e hora atual.
from datetime import datetime
# Criar uma nova instância do aplicativo Flask.
# Isso inicializa nossa aplicação de servidor para que possamos definir endpoints nela.
app = Flask(__name__)
# ------------------------------------------
# Endpoint: Agent Card (Discovery Phase)
# ------------------------------------------
# Define o HTTP GET route para o well-known agent discovery path.
# De acordo com a especificação A2A, clientes descobrem um agente chamando `/.well-known/agent.json`
@app.route("/.well-known/agent.json", methods=["GET"])
def agent_card():
    # Retornar metadados sobre este agente em formato JSON.
    # Isso inclui o nome do agente, descrição, URL base, versão e capacidades.
    return jsonify({
        "name": "TellTimeAgent",      # Nome legível por humanos do agente
        "description": "Informa a hora atual quando solicitado.",  # Resumo curto do agente
        "url": "http://localhost:5000",  # Onde este agente está hospedado (usado por clientes)
        "version": "1.0",              # Informações de versão para o agente
        "capabilities": {
            "streaming": False,        # Indica que este agente não suporta streaming
            "pushNotifications": False  # Indica que o agente não envia notificações push
        }
    })

# ------------------------------------------
# Endpoint: Task Handling (tasks/send)
# ------------------------------------------

# Define um HTTP POST route para /tasks/send.
# Este é o endpoint principal que os clientes A2A usam para enviar uma tarefa para o agente.
@app.route("/tasks/send", methods=["POST"])
def handle_task():
    try:
        # Analisar o payload JSON recebido em um dicionário Python.
        task = request.get_json()
        
        # Extrair o ID da tarefa do payload.
        # Isso identifica de forma única a tarefa no protocolo A2A.
        task_id = task.get("id")
        
        # Extrair o texto da mensagem do usuário da primeira parte da mensagem.
        # A2A representa mensagens como uma lista de "partes", onde a primeira parte geralmente contém texto.
        user_message = task["message"]["parts"][0]["text"]
        
    # Se a requisição não corresponder à estrutura esperada, retornar um erro 400.
    except (KeyError, IndexError, TypeError):
        return jsonify({"error": "Formato de tarefa inválido"}), 400

    # ------------------------------------------
    # Gerar uma resposta para a mensagem do usuário
    # ------------------------------------------

    # Obter a hora atual do sistema como uma string formatada.
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Construir o texto da mensagem de resposta do agente.
    reply_text = f"A hora atual é {current_time}."

    # Retornar uma resposta A2A formatada corretamente.
    # Isso inclui a mensagem original e uma nova mensagem do agente.
    return jsonify({
        "id": task_id, # Reutilizar o mesmo ID da tarefa na resposta
        "status": {"state": "completed"}, # Marcar a tarefa como concluída
        "messages": [
            task["message"], # Incluir a mensagem original do usuário para contexto
            {
                "role": "agent", # Esta mensagem é do agente
                "parts": [{"text": reply_text}] # Conteúdo da resposta no formato
            } 
        ]
    })

# ------------------------------------------
# Executar o servidor Flask
# ------------------------------------------

# Este bloco executa o aplicativo Flask apenas se este script for executado diretamente.
# Inicia um servidor de desenvolvimento local na porta 5000.
if __name__ == "__main__":
    app.run(debug=True, port=5000)
