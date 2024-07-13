import requests
import os
url = "http://localhost:8000/uploadFile/"

src = "database/raw_db_txt_2_bk"
for i in os.listdir(src):
    payload = {}
    files=[
        ('uploaded_file',(f'{i}',open(os.path.join("/khangnh/gotit-chatbot", src, i),'rb'),'text/plain'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    # print(response)
    if response.status_code == 200:
        print(f'=insert done {i, response.status_code}=\n')
    else:
        print(f'=cant insert {i, response.status_code}=\n')
