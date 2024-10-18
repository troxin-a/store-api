from fastapi.routing import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users_list():
    return {"users": "users"}
