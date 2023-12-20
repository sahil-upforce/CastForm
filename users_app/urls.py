from core.router import NoSlashRouter
from users_app.views import GenderModelViewSet, UserTypeModelViewSet

user_router = NoSlashRouter()
user_router.register(r"genders", GenderModelViewSet)
user_router.register(r"user-types", UserTypeModelViewSet)
