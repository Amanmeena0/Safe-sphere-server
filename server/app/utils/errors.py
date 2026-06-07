from fastapi import HTTPException, status

def bad_request_error(message: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )

def unauthorized_error(message: str = "Unauthorized"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message
    )

def not_found_error(message: str = "Resource not found"):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message
    )

def internal_server_error(message: str = "An unexpected error occurred"):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=message
    )
