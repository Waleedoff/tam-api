from importlib import import_module

APP_MODELS = [
    "app.api.todos.models",
    "app.api.auth.models",
    "app.common.models",
    "app.api.organization.models",
    "app.api.announcement.models", 
    "app.api.room.model",
    "app.api.message.models",
    "app.api.goal.models",
    "app.api.brd.models",
    "app.api.backlog.model"

]

for model in APP_MODELS:
    import_module(model)
