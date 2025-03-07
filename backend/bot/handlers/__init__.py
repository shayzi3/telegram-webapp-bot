from bot.callbacks.admin import admin_callback_router
from bot.callbacks.callback import callback_router

from .common.user import user_router
from .common.admin import admin_router



__routers__ = [
     user_router,
     admin_router,
     admin_callback_router,
     callback_router,
]