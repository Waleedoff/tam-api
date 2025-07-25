from importlib import import_module

APP_MODELS = [
    "app.api.todos.models",
    "app.api.auth.models",
    "app.common.models"

]

for model in APP_MODELS:
    import_module(model)
