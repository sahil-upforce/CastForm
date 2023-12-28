from core.router import NoSlashRouter
from users_app import views

user_router = NoSlashRouter()
user_router.register(r"genders", views.GenderModelViewSet)
user_router.register(r"user-types", views.UserTypeModelViewSet)
user_router.register(r"account", views.UserModelViewSet)
