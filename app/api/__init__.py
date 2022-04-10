from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from repository.errors import RepositoryError
from domain.errors import DomainError
from fastapi.responses import JSONResponse


from . import user
from . import auth


router = APIRouter()
# router.include_router(user.router, prefix="/hello")
router.include_router(user.router)
router.include_router(auth.router)


# url/docsで自動生成される文章に使われる
app = FastAPI(
    title='Knowde API',
    description=''
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)


@app.exception_handler(RepositoryError)
async def repository_error_handler(request, err: RepositoryError):
    return JSONResponse(
        status_code=err.status_code,
        content={"detail": err.detail}
    )

@app.exception_handler(DomainError)
async def domain_error_handler(request, err: DomainError):
    return JSONResponse(
            status_code=err.status_code,
            content={"detail": err.detail}
        )
