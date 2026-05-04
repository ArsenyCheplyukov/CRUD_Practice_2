from api.routes.comments import router as comment_router
from api.routes.projects import router as project_router
from api.routes.tasks import router as task_router
from api.routes.users import router as user_router

__all__ = ["comment_router", "project_router", "task_router", "user_router"]
