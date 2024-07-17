# author: khangnh
import os
import time
import logging
import traceback
from typing import Optional
from dotenv import load_dotenv


import chainlit as cl
from chainlit.types import ThreadDict
from starlette.responses import StreamingResponse, Response

from llama_index.core import Settings
from llama_index.core.agent import ReActAgent
from llama_index.core.callbacks import CallbackManager
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.query_engine import TransformQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core import (
    VectorStoreIndex,
)
from src.constants import cfg, prompt_template, refine_template, rerank_postprocessor, logger, TEXT_EMBEDDING_MODEL
from src.utils.chat_utils import setup_history, handle_generate_actions
from src.http_message.message import HTTP_STATUS
from src.api.ingest_data_service import IngestionService
from src.llms import MODEL_TABLE
from src.callbacks.langfuse_callback import langfuse_callback_handler

from langfuse.decorators import langfuse_context, observe

Settings.callback_manager = CallbackManager([langfuse_callback_handler])
load_dotenv(override=True)

class AssistantService:
        
    def __init__(self, callback_manager: Optional[CallbackManager] = None):
        # self.callback_list = callback_list
        self.rerank_processor = rerank_postprocessor
        self.prompt_tmpl = prompt_template
        self.refine_tmpl = refine_template
        self.ingestion_service = IngestionService()
        self.query_index = self.ingestion_service.query_index
                    
        if cfg.LLM_RECOMMEND_MODEL.ENABLE_QUESTION_RECOMMENDER:
            from src.tasks.question_recommend_task import QuestionRecommender
            qr_llm = self.load_model(cfg.LLM_RECOMMEND_MODEL.QR_SERVICE, cfg.LLM_RECOMMEND_MODEL.QR_MODEL_ID)
            self.question_recommender = QuestionRecommender.from_defaults(llm=qr_llm)

        self.llm = self.load_model(cfg.LLM_MODEL.SERVICE, cfg.LLM_MODEL.LLM_MODEL_ID)
        Settings.llm = self.llm
        Settings.embed_model = TEXT_EMBEDDING_MODEL
        self.query_engine = self.create_query_engine(self.query_index, self.rerank_processor, self.prompt_tmpl, self.refine_tmpl)

    def load_tool(self):
        '''
        load tool funtions
        '''
        query_engine = self.create_query_engine(self.query_index, self.rerank_processor, self.prompt_tmpl, self.refine_tmpl)
        query_engine_tools = [
            QueryEngineTool(
                query_engine=query_engine,
                metadata=ToolMetadata(
                    name="general_engine",
                    description=(
                        "Provide general search capabilities for information of dayone company"
                        "Use a detailed plain text question as input to the tool."
                    ),
                ),
            )
        ]
        return query_engine_tools
    
    def create_agent(self):
        query_engine_tools = self.load_tool()
        agent = ReActAgent.from_tools(
            query_engine_tools,
            llm=self.llm,
            verbose=True,
            callback_manager=self.callback_manager
        )
        return agent

    def create_query_engine(self, query_index, rerank_postprocessor, prompt_template, refine_template):
        """
        Creates and configures a query engine for routing queries to the appropriate tools.
        
        This method initializes and configures a query engine for routing queries to specialized tools based on the query type.
        It loads a language model, along with specific tools for tasks such as code search and paper search.
        
        Returns:
            AgentRunner: An instance of AgentRunner configured with the necessary tools and settings.
        """
        
        # if cfg.MODEL.SERVICE != "openai":
        query_engine = query_index.as_query_engine(
            similarity_top_k=cfg.VECTOR_DATABASE.SIMILARITY_TOP_K,
            vector_store_query_mode="hybrid",
            llm=self.llm,
            streaming=True,
            text_qa_template=prompt_template,
            refine_template=refine_template,
            node_postprocessors=[rerank_postprocessor],
            verbose=True,
            embed_model=Settings.embed_model
        )
        hyde = HyDEQueryTransform(include_original=True)
        hyde_query_engine = TransformQueryEngine(query_engine, hyde, callback_manager=Settings.callback_manager)

        return hyde_query_engine

    def load_model(self, service, model_id):
        """
        Select a model for text generation using multiple services.
        Args:
            service (str): Service name indicating the type of model to load.
            model_id (str): Identifier of the model to load from HuggingFace's model hub.
        Returns:
            LLM: llama-index LLM for text generation
        Raises:
            ValueError: If an unsupported model or device type is provided.
        """
        logging.info(f"Loading Model using server: {service} and model id is: {model_id}")
        logging.info("This action can take a few minutes!")
        service = service.lower()
        assert service in ["ollama", "groq", "openai"], "The implementation for other types of LLMs are not ready yet!"
        try:
            return MODEL_TABLE[service](model_id)
        except Exception as e:
            raise NotImplementedError("The implementation for other types of LLMs are not ready yet!")

    def predict(self, prompt):
        """
        Predicts the next sequence of text given a prompt using the loaded language model.

        Args:
            prompt (str): The input prompt for text generation.

        Returns:
            str: The generated text based on the prompt.
        """
        # Assuming query_engine is already created or accessible
        if cfg.LLM_MODEL.STREAM:
            streaming_response = self.query_engine.query(prompt)
            return StreamingResponse(streaming_response.response_gen, media_type="application/text; charset=utf-8")
        else:
            return Response(self.query_engine.chat(prompt).response, media_type="application/text; charset=utf-8")
    
    async def aon_start(self):
        cl.user_session.set("history", [])
        cl.user_session.set("query_engine", self.query_engine)
        cl.user_session.set("assistant_service", self)
        await cl.Message(
            author="Assistant", content="Chào bạn, vui lòng đợi 1 xí nha!", disable_feedback=True
        ).send()
    
    async def aon_resume(self, thread: ThreadDict):
        history = setup_history(thread)
        cl.user_session.set("query_engine", self.query_engine)
        cl.user_session.set("history", history)
        
    
    async def aon_message(self, message: cl.Message):
        logger.llm_logger.info(f'----Start request----')
        query_engine = cl.user_session.get("query_engine")

        history = cl.user_session.get("history")
        history.append({"role": "user", "content": message.content})

        try:
            msg = cl.Message(content="", author="Assistant")

            langfuse_callback_handler.set_trace_params(
                session_id=msg.id
            )
            start = time.time()
            res = await cl.make_async(query_engine.query)(message.content)
            logger.llm_logger.info(f'User: {message.content}')
            full_resp = ''
            for token in res.response_gen:
                await msg.stream_token(token)
                full_resp+=token
                
            # get response reference document
            refs_resource = res.source_nodes
            url_refs = []
            for ref in refs_resource:
                ref.metadata.keys()
                ref = ref.metadata["file_name"]
                if ref not in url_refs:
                    url_refs.append(ref)
            url_refs = "\n".join(["- "+i for i in url_refs])
            response_ref = f'\n\nDưới đây là các tài liệu tôi đã sử dụng để đưa ra câu trả lời, có thể một số sẽ không hữu dụng, mong bạn bỏ qua nhé!\n{url_refs}'
            for token in response_ref:
                await msg.stream_token(token)
            await msg.send()

            end = time.time()
            
            assistant_response = full_resp.replace("\n", "\t") + "\t" + response_ref.replace("\n", "\t")
            logger.llm_logger.info(f'Assistant: {(assistant_response)}')
            logger.llm_logger.debug(f'status_code: {HTTP_STATUS[200].status_code}')
            logger.llm_logger.info(f'processing time: {end-start}')
        except Exception as e:
            await cl.Message(content=HTTP_STATUS[407].body.decode("utf-8"), author="Assistant").send()
            logger.llm_logger.debug(f'status_code: {HTTP_STATUS[407].status_code}')
            logger.llm_logger.error(traceback.format_exc())
        logger.llm_logger.info(f'----End request----')

        if cfg.LLM_RECOMMEND_MODEL.ENABLE_QUESTION_RECOMMENDER:
            from src.utils.chat_utils import handle_next_question_generation
            history.append({"role": "assistant", "content": res.response})
            
            next_questions = handle_next_question_generation(tools=self.tools, query_str=message.content, llm_response=res.response)
            handle_generate_actions(next_questions)
            
            actions = [
                cl.Action(name=question, value=question, description=question) for question in next_questions
            ]
            msg.actions = actions
            await msg.update()
