
import re
from llama_index.core.schema import TransformComponent


class NodeFileNameToURL(TransformComponent):
    '''
    File name is the URL replace "/" with "_" like https:__www.example.com_path_to_file.txt
    So we must convert it back to normal URL like https://www.example.com/path/to/file.txt to help return
    the url reference when calling query bot
    '''
    def __call__(self, nodes, **kwargs):
        for node in nodes:
            node.metadata["file_name"] = node.metadata["file_name"].replace('_', "/").replace('.txt', '').replace("http//", "http://").replace("https//", "https://")
        return nodes