import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from app.api.announcement import routes as  announcement_router
from app.api.organization import routes as  organization_router
from app.api.auth import routes as auth_router
from app.api.todos import routes as todo_router
from app.api.room import routes as room_user
from app.api.sprint import routes as sprint_route
from app.api.message import routes as message_router
from app.api.goal import routes as goal_router
from app.api.userStory import routes as userStory_router
from core.langChain import routes as langChain_router
from app.api.brd import routes as brd_router
from app.api.backlog import routes as backlog_router
from app.config import config

# Set the timezone based on the app configuration
os.environ["TZ"] = config.APP_TZ
time.tzset()

# Initialize the FastAPI app
app = FastAPI(
    docs_url=config.docs_url,  # URL for Swagger UI documentation
    debug=not config.production,  # Debug mode based on production configuration
    openapi_url=config.openapi_url,  # URL for OpenAPI schema
)

# Add middleware to handle proxy headers and trusted hosts
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=config.FORWARDED_ALLOW_IPS)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.allow_hosts)

# Add GZip middleware for response compression

# Add CORS middleware to handle Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,  # Allow credentials like cookies
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Include routers for todos and users

# TODO: Comment on the purpose of the commented-out code below
# if config.ENVIRONMENT in ["staging", "prod"]:
#     app.on_event("startup")(add_groups_and_roles)


routes = [
    todo_router,
    auth_router,
    announcement_router, 
    organization_router,
    room_user,
    message_router,
    sprint_route,
    userStory_router,
    langChain_router,
    goal_router,
    brd_router,
    backlog_router
    # Add other routers as needed
]
# Loop through the routes list and include routers in the FastAPI app
for router_model in routes:
    app.include_router(
        router_model.router,
        prefix=router_model.prefix, tags=router_model.tags

    )

