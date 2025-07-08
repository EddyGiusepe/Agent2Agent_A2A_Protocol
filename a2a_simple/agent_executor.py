#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script agent_executor.py
========================

"""
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message
from pydantic import BaseModel


class GreetingAgent(BaseModel):
    """Agnet de Saudação que retorna uma saudação"""

    async def invoke(self) -> str:
        return "Olá Estudante! Certifique-se de curtir o vídeo e se inscrever!"


class GreetingAgentExecutor(AgentExecutor):

    def __init__(self):
        self.agent = GreetingAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        result = await self.agent.invoke()
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        raise Exception("Cancelamento não suportado")
    