# author Khangnh

import json
import traceback

import chainlit.data as cl_data
from langfuse import Langfuse
from langfuse.decorators import langfuse_context, observe

from src.constants import logger

langfuse = Langfuse()

class UserFeedback(cl_data.BaseDataLayer):
    '''
    UserFeedback datalayer to collect and store user feedback
    '''
    @observe()
    async def upsert_feedback(self, feedback: cl_data.Feedback) -> str:
        try:
            feedback_comment = feedback.comment
            feedback_value = feedback.value
            feedback_id = feedback.forId
            langfuse_context.update_current_observation(
                session_id=feedback_id
            )
            langfuse_context.score_current_observation(
                name="user_feedbacks",
                value=feedback_value,
                comment=feedback_comment,
                id=feedback_id
            )
        except Exception as e:
            logger.llm_logger.debug(f'Cant push feedback score to langfuse due to this error {e}')
            logger.llm_logger.error(traceback.format_exc())
