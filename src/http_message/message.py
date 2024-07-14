from fastapi import status

http_status = {
    "200_code": {
        "status": status.HTTP_200_OK,
        "message": "OK"
    },

    "415_code": {
        "status": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "message": "File type not supported, please using .txt file"
    },
    
    "400_code": {
        "status": status.HTTP_400_BAD_REQUEST,
        "message": "Inserted file must not be empty"
    },

    "412_code": {
        "status": status.HTTP_412_PRECONDITION_FAILED,
        "message": "Insert into redis vector DB failed"
    },

    "407_code": {
        "status": status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
        "message": "Chatbot currently cant response this message due to some error from server"
    }
}