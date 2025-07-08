#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script test_client.py
=====================
Este script é responsável por testar o cliente A2A.

Run
---
uv run test_client.py

ou

uv run --active test_client.py
"""
import uuid
import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    TextPart,
)

PUBLIC_AGENT_CARD_PATH = "/.well-known/agent.json"
BASE_URL = "http://localhost:9999"


async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:
        # Inicializa o A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL,
        )

        final_agent_card_to_use: AgentCard | None = None

        try:
            print(
                f"Obtendo cartão público do agente de: {BASE_URL}{PUBLIC_AGENT_CARD_PATH}"
            )
            _public_card = await resolver.get_agent_card()
            print("Cartão público do agente obtido com sucesso")
            print(_public_card.model_dump_json(indent=2))

            final_agent_card_to_use = _public_card

        except Exception as e:
            print(f"Erro ao obter cartão público do agente: {e}")
            raise RuntimeError("Falha ao obter cartão público do agente")

        client = A2AClient(
            httpx_client=httpx_client, agent_card=final_agent_card_to_use
        )
        print("A2AClient inicializado com sucesso")

        #message_payload = Message(
        #    role=Role.user,
        #    messageId=str(uuid.uuid4()),
        #    parts=[Part(root=TextPart(text="Olá, como você está?"))],
        #)
        #request = SendMessageRequest(
        #    id=str(uuid.uuid4()),
        #    params=MessageSendParams(
        #        message=message_payload,
        #    ),
        #)
        #print("Enviando mensagem")

        #response = await client.send_message(request)
        #print("Resposta:")
        #print(response.model_dump_json(indent=2))


#if __name__ == "__main__":
#    import asyncio

#    asyncio.run(main())


        print("Conversa iniciada (digite 'sair' para encerrar)")
        while True:
            user_input = input("Você: ")
            
            if user_input.lower() == "sair":
                print("Encerrando conversa...")
                break

            message_payload = Message(
                role=Role.user,
                messageId=str(uuid.uuid4()),
                parts=[Part(root=TextPart(text=user_input))],
            )
            request = SendMessageRequest(
                id=str(uuid.uuid4()),
                params=MessageSendParams(
                    message=message_payload,
                ),
            )
            print("Enviando mensagem...")

            response = await client.send_message(request)
            
            # Debug para entender a estrutura
            print("Atributos disponíveis:", dir(response))
            print("JSON da resposta:")
            print(response.model_dump_json(indent=2))
            
            # Tentamos extrair o texto de forma segura:
            try:
                # Convertemos para dicionário para acessar de forma mais segura
                response_dict = response.model_dump()
                if "result" in response_dict and "parts" in response_dict["result"]:
                    text = response_dict["result"]["parts"][0]["text"]
                    print("Agente:", text)
                else:
                    print("Estrutura da resposta não contém o texto esperado")
            except Exception as e:
                print(f"Erro ao extrair texto: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
