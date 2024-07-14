# author khangnh

# normal config from config file
from configs.config import get_config

cfg = get_config('configs/config.yaml')

# PROMPT CONFIG
from llama_index.core import ChatPromptTemplate, PromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole

SYSTEM_PROMPT_QUERY_ENGINE = """
Bạn là chatbot được phát triển bởi Khangnh.
Bạn được đưa nội dung từ một số văn bản và công việc của bạn là trả lời câu hỏi của user về nội dung đã được cung cấp.

Một số quy luật cần tuân theo
    1. Tuyệt đối không dùng những cụm như:
        - 'Dựa vào ...'
        - 'Based on ...'
        - 'Here is the refined answer: ...'
        - 'Câu trả lời đã được tinh chỉnh:...'
        hay tất cả những cụm tương tự
    2. Hãy sử dụng tiếng Việt trong câu trả lời.
    3. Bạn không cần phải diễn giải gì thêm, chỉ cần trả lời đúng câu hỏi trọng tâm
    4. Nếu cuối cùng bạn vẫn không thể tìm ra câu trả lời đáng tin cậy thì bạn hãy nói "tôi không đủ dữ kiện để trả lời" và không hồi đáp gì thêm
"""

USER_PROMPT_QUERY_ENGINE = """
Ngữ cảnh được cung cấp như sau
---------------------
{context_str}
---------------------
Dựa trên nội dung được cung cấp. Hãy trả lời câu hỏi từ người dùng và kết thúc câu trả lời một cách đầy đủ.
Nếu nội dung được cung cấp không hề liên quan hoặc không đủ để bạn đưa ra câu trả lời. Hãy nói rằng bạn "Tôi không có đủ thông tin để trả lời".

Hãy sử dụng tiếng Việt trong câu trả lời.

Nếu bạn ghi nhớ và làm đúng những gì tôi đã dặn dò, tôi sẽ tip cho bạn 100.000 VND vào cuối ngày
Câu hỏi của người dùng: {query_str}
Câu trả lời của AI:

"""

REFINE_PROMPT_QUERY_ENGINE = """
Câu hỏi gốc như sau: {query_str}
Chúng ta có một câu trả lời có sẵn: {existing_answer}
Chúng ta có cơ hội tinh chỉnh câu trả lời hiện có (chỉ khi cần) với một số ngữ cảnh khác bên dưới.
------------
{context_msg}
------------
Với bối cảnh mới, hãy tinh chỉnh câu trả lời ban đầu để trả lời truy vấn tốt hơn. Nếu ngữ cảnh không hữu ích, hoặc bạn nghi ngờ, hãy trả lại câu trả lời ban đầu.
Bạn không được nói bạn đã làm hoặc các bước tinh chỉnh như thế nào, chỉ trả về kết quả cuối cùng sau

Hãy sử dụng tiếng Việt trong câu trả lời.
Câu trả lời đã được tinh chỉnh (bạn không cần phải trả về term mô tả này ở trong câu trả lời cuối cùng của mình):

"""

message_template = [
    ChatMessage(content=SYSTEM_PROMPT_QUERY_ENGINE, role=MessageRole.SYSTEM),
    ChatMessage(content=USER_PROMPT_QUERY_ENGINE, role=MessageRole.USER)
]

refine_message_template = [
    ChatMessage(content=SYSTEM_PROMPT_QUERY_ENGINE, role=MessageRole.SYSTEM),
    ChatMessage(content=REFINE_PROMPT_QUERY_ENGINE, role=MessageRole.USER),
]
prompt_template = ChatPromptTemplate(message_template)
refine_template = ChatPromptTemplate(refine_message_template)

# DEFAULT_SYSTEM_PROMPT_AGENT = """
# Bạn là chatbot được phát triển bởi Khangnh, và được thiết kế để có thể hỗ trợ được nhiều tác vụ, từ trả lời câu hỏi, tìm kiếm, đưa ra tóm tắt và nhiều loại phân tích khác

# ## Công cụ

# Bạn có quyền truy cập nhiều loại công cụ khác nhau và nhiệm vụ của bạn là sử dụng các công cụ này để có thể hoàn thành các công việc, bạn có thể chia nhỏ công việc ra thành nhiều phần nhỏ hơn và sử dụng nhiều loại công cụ khác nhau để hoàn thành mỗi phần.

# Bạn có quyền truy cập vào các công cụ sau:
# {tool_desc}

# ## Định dạng đầu ra
# Hãy trả lời với ngôn ngữ tiếng Việt với định dạng sau đây:
# ```
# Thought: Ngôn ngữ đang được sử dụng là: (ngôn ngữ của người dùng nhập vào). Tôi cần sử dụng một công cụ để giúp tôi trả lời câu hỏi.
# Action: tên công cụ (một trong số {tool_names}) nếu sử dụng một công cụ.
# Action Input: dữ liệu đầu vào cho công cụ (nhớ luôn sử dụng tiếng Việt), ở định dạng JSON đại diện cho các tham số (ví dụ: {{"input": "hello world", "num_beams": 5}})
# ```

# Vui lòng luôn bắt đầu bằng Thought.

# Vui lòng sử dụng định dạng JSON hợp lệ cho Action Input. KHÔNG ĐƯỢC làm như sau {{'input': 'hello world', 'num_beams': 5}}.

# Nếu định dạng này được sử dụng, người dùng sẽ trả lời theo định dạng sau:

# ```
# Observation: kết quả từ công cụ
# ```

# Bạn nên lặp lại định dạng trên cho đến khi bạn có đủ thông tin để trả lời câu hỏi mà không cần sử dụng thêm bất kỳ công cụ nào. Lúc đó, bạn PHẢI trả lời bằng một trong hai định dạng sau:
# ```
# Thought: Tôi nghĩ mình có thể trả lời mà không cần sử dụng thêm bất kỳ công cụ nào.
# Answer: [câu trả lời của bạn ở đây]
# ```

# ```
# Thought: Tôi nghĩ mình không thể trả lời câu hỏi với các công cụ được cung cấp.
# Answer: Xin lỗi, tôi không thể trả lời câu hỏi của bạn.
# ```

# ## Cuộc trò chuyện hiện tại
# Dưới đây là cuộc trò chuyện luân phiên hiện tại giữa người dùng với bạn.

# """
# DEFAULT_SYSTEM_PROMPT_AGENT = PromptTemplate(DEFAULT_SYSTEM_PROMPT_AGENT) # just support for agent



# LOADING MODEL
# Embedding model
import torch
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

device_type = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
if cfg.EMBEDDING_MODEL.EMBEDDING_SERVICE == "hf":
    TEXT_EMBEDDING_MODEL = HuggingFaceEmbedding(model_name=cfg.EMBEDDING_MODEL.EMBEDDING_MODEL_NAME, 
                                                cache_folder="./models", 
                                                device=device_type,
                                                max_length=cfg.EMBEDDING_MODEL.MAX_LENGTH,
                                                embed_batch_size=cfg.EMBEDDING_MODEL.EMBEDD_BATCH_SIZE)
else:
    raise NotImplementedError()   

# reranking_model
from llama_index.core.postprocessor import SentenceTransformerRerank
rerank_postprocessor = SentenceTransformerRerank(
    model=cfg.RERANK_MODEL.MODEL_NAME,
    top_n=cfg.RERANK_MODEL.RERANK_TOP_N,
    keep_retrieval_score=True
)

# logging
import logging
from src.log_module.logging_default import BaseLogger
logger = BaseLogger(log_dir='logs', log_level=logging.DEBUG)
