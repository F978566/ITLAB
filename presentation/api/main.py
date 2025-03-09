from fastapi import FastAPI

from presentation.api.problems import handlers


app = FastAPI()

app.include_router(handlers.router)