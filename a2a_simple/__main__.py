#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script __main__.py
==================
Este script é responsável por executar nosso servidor, que ficará
aguardando o recebimento da solicitação. Quando receber a solicitação,
ele a passará para o Agente e, na verdade, a captura rápida não a 
passará diretamente para o Agente, mas sim para o Agente Executor, que
é um dos outros conceitos principais que devemos saber.

Siga os seguintes passos para EXECUTAR o servidor:

1. Em um terminal, execute o comando:

uv run .   ou   uv run __main__.py

2. Em um novo terminal, execute o comando:

uv run --active test_client.py     ou     uv run test_client.py


NOTA: O script agent_executor.py é responsável por executar o agente.
      Ou seja, é o responsável por executar a função invoke() do agente.
"""
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent_executor import GreetingAgentExecutor


def main():
    skill = AgentSkill(
        id="hello_world",
        name="Saudar",
        description="Retornar uma saudação",
        tags=["saudacao", "ola", "saudar"],
        examples=["Olá", "Oi", "E aí"],
    )

    agent_card = AgentCard(
        name="Agent de Saudação",
        description="Um agente simples que retorna uma saudação",
        url="http://localhost:9999/",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        skills=[skill],
        version="1.0.0",
        capabilities=AgentCapabilities(),
    )

    request_handler = DefaultRequestHandler(
        agent_executor=GreetingAgentExecutor(),
        task_store=InMemoryTaskStore(), # Só funciona emquanto o servidor estiver em execução
    )

    server = A2AStarletteApplication(
        http_handler=request_handler,
        agent_card=agent_card,
    )

    uvicorn.run(server.build(), host="0.0.0.0", port=9999)


if __name__ == "__main__":
    main()
    