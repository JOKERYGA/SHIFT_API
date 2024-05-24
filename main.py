from alembic.util import status
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_users import FastAPIUsers, fastapi_users
from fastapi_users.authentication import Authenticator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
from src.database import User, get_async_session, Salary
from models.models import Salary
from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
from src.auth.base_config import auth_backend

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
authenticator = Authenticator([auth_backend], get_user_manager)


# @app.post("/auth/jwt/login/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


current_active_user = fastapi_users.current_user(active=True)


@app.get("/salary")
async def get_salary(
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(Salary).where(Salary.user_id == user.id))
    salary = result.scalars().first()
    if salary:
        return {
            "current_salary": salary.current_salary,
            "next_raise_date": salary.next_raise_date,
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Salary information not found"
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
