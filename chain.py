#author khangnh
import chainlit as cl
from chainlit.server import app
from chainlit.types import ThreadDict
from llama_index.core.callbacks import CallbackManager

from src.api.llm_service import AssistantService
from src.callbacks.langfuse_callback import langfuse_callback_handler


@cl.cache
def create_assistant_serivce():
    return AssistantService()

assistant_service = create_assistant_serivce()

@cl.action_callback("next_question")
async def next_question(action):
    message = cl.Message(content=action.value, author="User")
    await message.send()
    await assistant_service.aon_message(message)

@cl.on_chat_start
async def on_chat_start():
    await assistant_service.aon_start()

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    await assistant_service.aon_resume(thread)

@cl.on_message
async def on_message(message: cl.Message):
    await assistant_service.aon_message(message)