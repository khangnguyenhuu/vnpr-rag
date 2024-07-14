from llama_index.core.node_parser import HTMLNodeParser
from llama_index.readers.file import HTMLTagReader
import os


parser = HTMLNodeParser()  # optional list of tags
dst_folder = "database/raw_db_txt"
os.makedirs(dst_folder, exist_ok=True)
filename_fn = lambda filename: {"file_name": filename}

import re
def has_text(line):
    """
    Checks if a given line of text contains any non-whitespace characters.
    
    Args:
        line (str): The input line of text to be checked.
    
    Returns:
        bool: True if the line contains any text, False otherwise.
    """
    return bool(line.strip())
def replace_multiple_newlines(text):
    """
    Replaces all occurrences of more than one consecutive newline character (\n)
    with a single newline character.
    
    Args:
        text (str): The input text to be processed.
    
    Returns:
        str: The processed text with consecutive newline characters replaced.
    """
    return re.sub(r'\n\n+', '\n', text)

def remove_leading_whitespace(text):
    """
    Removes all leading whitespace characters from the given text.
    
    Args:
        text (str): The input text to be processed.
    
    Returns:
        str: The text with all leading whitespace characters removed.
    """
    return text.lstrip()

def is_single_dash_line(line):
    """
    Checks if a given line of text contains only a single dash character, possibly surrounded by whitespace.
    
    Args:
        line (str): The input line of text to be checked.
    
    Returns:
        bool: True if the line contains only a single dash character, False otherwise.
    """
    return bool(re.match(r'^\s*-\s*$', line))

# all_docs = []
for i in os.listdir("database/raw_db_html/"):
    path = os.path.join("database/raw_db_html/", i)
    html_docs = HTMLTagReader(tag="body").load_data(path)
    # for html_doc in html_docs:
        # html_docs[0].metadata["file_path"] = html_docs[0].metadata["file_path"].replace("database/raw_db_html/", "").replace('_', "/").replace(".html", "")
    html_docs = "\n".join([j.text for j in html_docs])
    # html_docs = html_docs.replace("\n\n", " ")
    html_docs = replace_multiple_newlines(html_docs)
    new_data = []
    for line in html_docs.split("\n"):
        # if len(line.replace(" ", "").replace("   ", "")) < 2 and "-" in line:
        if is_single_dash_line(line):
            pass
        elif not has_text(line):
            pass
        elif len(line) == 1:
            pass
        else:
            new_data.append(remove_leading_whitespace(line))
    with open((path+".txt").replace("database/raw_db_html", dst_folder), "w+") as fp1:
        print(path+".txt".replace("database/raw_db_html", dst_folder))
        fp1.write("\n".join(new_data))

