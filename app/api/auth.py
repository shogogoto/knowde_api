from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import HTTPException, status


from models.auth import Credential, PlainPassword
from repository import CredentialRepository
from repository.errors import AlreadyExistsError

router = APIRouter()


# @router.exception_handler(AlreadyExistsError)
# async def error_handler(request, err: AlreadyExistsError):
#     raise HTTPException(
#         status_code=status.HTTP_409_CONFLICT,
#         detail=str(e)
#     )


@router.post("/aaa")
async def register_credential(form_data: OAuth2PasswordRequestForm = Depends()):
    p    = PlainPassword(form_data.password)
    cred = Credential(form_data.username, p)
    repo = CredentialRepository()
    repo.create(cred)
    return {}
