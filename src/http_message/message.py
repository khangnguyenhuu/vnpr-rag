from fastapi import status
from fastapi.responses import JSONResponse

# http_status = {
#     "200_code": {
#         "status": status.HTTP_200_OK,
#         "message": "OK"
#     },

#     "415_code": {
#         "status": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#         "message": "File type not supported, please using .txt file"
#     },
    
#     "400_code": {
#         "status": status.HTTP_400_BAD_REQUEST,
#         "message": "Inserted file must not be empty"
#     },

#     "412_code": {
#         "status": status.HTTP_412_PRECONDITION_FAILED,
#         "message": "Insert into redis vector DB failed"
#     },

#     "407_code": {
#         "status": status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
#         "message": "Chatbot currently cant response this message due to some error from server"
#     }
# }

HTTP_STATUS = {
    200: JSONResponse(status_code=status.HTTP_200_OK,
                      content={
                          "status_code": status.HTTP_200_OK,
                          "message": "OK"}),         
    415: JSONResponse(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                      content={
                          "status_code": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                          "message": "File type not supported, please using .txt file"}),
    400: JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                      content={
                          "status_code": status.HTTP_400_BAD_REQUEST,
                          "message": "Inserted file must not be empty"}),
    412: JSONResponse(status_code=status.HTTP_412_PRECONDITION_FAILED,
                      content={
                          "status_code": status.HTTP_412_PRECONDITION_FAILED,
                          "message": "Insert into redis vector DB failed"}),
    407: JSONResponse(status_code= status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
                      content={
                          "status_code": status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
                          "message": "Chatbot currently cant response this message due to some error from server"}),
    500: JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      content={
                          "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                          "message": "Internal server Error"})
}
