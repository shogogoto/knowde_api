from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import HTTPException, status
from pydantic import BaseModel
from fastapi.param_functions import Form
from usecase import AuthUsecase
from dependency import DIContainer
from .errors import error_response
from domain.errors import DomainError, UnauthorizedError

router = APIRouter()


usecase = DIContainer().resolve(AuthUsecase)

# @router.exception_handler(AlreadyExistsError)
# async def error_handler(request, err: AlreadyExistsError):
#     raise HTTPException(
#         status_code=status.HTTP_409_CONFLICT,
#         detail=str(e)
#     )
class CredentialForm(BaseModel):
    userId: str = Form(...)
    password: str = Form(...)

class RepasswordForm(BaseModel):
    userId: str   = Form(...)
    current_password: str = Form(...)
    new_password: str = Form(...)


@router.post("/users", tags=["auth"],
    responses=error_response([UnauthorizedError]))
async def create_credential(form_data: CredentialForm = Depends()):
    usecase.registerCredential(**form_data.dict())
    return

@router.put("/users", tags=["auth"])
async def repassword_user(form_data: RepasswordForm = Depends()):
    usecase.repassword(**form_data.dict())
    return form_data.dict()


@router.delete("/users", tags=["auth"])
async def delete_user(form_data: CredentialForm = Depends()):
    usecase.deleteCredential(**form_data.dict())
    return form_data.json()
