from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import HTTPException, status
from pydantic import BaseModel
from fastapi.param_functions import Form

from domain.auth import Credential, PlainPassword
from repository import CredentialRepository
from repository.errors import AlreadyExistsError

router = APIRouter()


# @router.exception_handler(AlreadyExistsError)
# async def error_handler(request, err: AlreadyExistsError):
#     raise HTTPException(
#         status_code=status.HTTP_409_CONFLICT,
#         detail=str(e)
#     )
class RepasswordForm(BaseModel):
    grant_type: str = Form(None, regex="password")
    username: str   = Form(...)
    password: str   = Form(...)
    repassword: str = Form(...)


@router.post("/users", tags=["users"])
async def create_credential(form_data: OAuth2PasswordRequestForm = Depends()):
    p    = PlainPassword(form_data.password)
    cred = Credential(form_data.username, p)
    repo = CredentialRepository()
    repo.create(cred)
    return {"test": "test"}

@router.put("/users", tags=["users"])
async def repassword_user(form_data: RepasswordForm = Depends()):
    oldPwd = PlainPassword(form_data.password)
    newPwd = PlainPassword(form_data.repassword)
    oldCred = Credential(form_data.username, oldPwd)
    newCred = Credential(form_data.username, newPwd)
    repo = CredentialRepository()
    repo.update(oldCred, newCred)
    return {}

@router.delete("/users", tags=["users"])
async def delete_user(form_data: OAuth2PasswordRequestForm = Depends()):
    p    = PlainPassword(form_data.password)
    cred = Credential(form_data.username, p)
    repo = CredentialRepository()
    repo.delete(cred)
    return {}
