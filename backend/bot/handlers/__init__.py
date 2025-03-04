from .common.user import user_router
from .common.admin import admin_router


__routers__ = [
     user_router,
     admin_router,
]