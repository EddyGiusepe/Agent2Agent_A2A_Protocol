#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro
"""
# Importar a biblioteca requests para enviar requisições HTTP GET e POST.
# Isso permite que o cliente converse com o servidor via HTTP.
import requests
# Importar o módulo uuid para gerar IDs de tarefas únicas.
# Cada tarefa A2A deve ter um ID único.
import uuid
# ------------------------------------------
# Step 1 - Descobrir o Agente
# ------------------------------------------
# Definir a URL base onde o agente servidor está hospedado.
# Neste caso, ele é executado localmente na porta 5000.
base_url = "http://localhost:5000"

# Usar HTTP GET para buscar o card do agente a partir da endpoint de descoberta well-known
res = requests.get(f"{base_url}/.well-known/agent.json")

# Se a requisição falhar (não status code 200), gerar um erro.
if res.status_code != 200:
    raise Exception("Falha ao descobrir o agente.")

# Analisar o JSON da resposta em um dicionário Python.
agent_info = res.json()
# Exibir algumas informações básicas sobre o agente descoberto.
print(f"Conectado a: {agent_info['name']} - {agent_info['description']}")

# ------------------------------------------
# Step 2 - Preparar uma Tarefa
# ------------------------------------------

# Generate a unique ID for this task using uuid4 (random UUID).
task_id = str(uuid.uuid4())

# Construct the A2A task payload as a Python dictionary.
# According to A2A spec, we need to include:
# - "id": the unique task ID
# - "message": an object with "role" and a list of "parts" (in this case, just one part)
task_payload = {
    "id": task_id,
    "message": {
        "role": "user", # Indicates that the message is coming from the user 
        "parts": [
            {"text": "Que horas são?"}
        ]
    }
}

# ------------------------------------------
# Step 3 - Enviar a Tarefa para o Agente
# ------------------------------------------

# Enviar uma requisição HTTP POST para o endpoint /tasks/send do agente.
# Usamos o parâmetro `json=` para que requests serialize nosso dicionário como JSON.
response = requests.post(f"{base_url}/tasks/send", json=task_payload)

# Se o servidor não retornar um status 200 OK, gerar um erro.
if response.status_code != 200:
    raise Exception(f"Tarefa falhou: {response.text}")

# Analisar a resposta JSON do agente em um dicionário Python.
response_data = response.json()

# ------------------------------------------
# Passo 4 - Exibir a Resposta do Agente
# ------------------------------------------

# Extract the list of messages returned in the response.
# This typically includes both the user's message and the agent's reply.
messages = response_data.get("messages", [])

# If there are messages, extract and print the last one (agent's response).
if messages:
    final_reply = messages[-1]["parts"][0]["text"]  
    print("Agent says:", final_reply)
else:
    # If no messages were received, notify the user.
    print("No response received.")
    