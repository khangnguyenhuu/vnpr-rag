import json
import chainlit.data as cl_data

from langfuse import Langfuse
from langfuse.decorators import langfuse_context, observe
langfuse = Langfuse()
class UserFeedback(cl_data.BaseDataLayer):
    @observe()
    async def upsert_feedback(self, feedback: cl_data.Feedback) -> str:
        feedback_comment = feedback.comment
        feedback_value = feedback.value
        feedback_id = feedback.forId
        langfuse_context.update_current_observation(
            session_id=feedback_id
        )
        # langfuse_context.score_current_observation(
        #     name="usr_feedbacks",
        #     value=feedback_value,
        #     comment=feedback_comment,
        # )
        langfuse.score(
            id=feedback_id, # optional, can be used as an indempotency key to update the score subsequently
            name="thumbs",
            trace_id=feedback_id,
            value=feedback_value, # 0 or 1
            data_type="BOOLEAN", # required, numeric values without data type would be inferred as NUMERIC
            comment=feedback_comment # optional
        )