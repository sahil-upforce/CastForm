from core.router import NoSlashRouter
from users_app.views import GenderModelViewSet

user_router = NoSlashRouter()
user_router.register(r"genders", GenderModelViewSet)
