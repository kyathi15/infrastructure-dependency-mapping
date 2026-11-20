from fastapi import FastAPI

from app.api.routes import router
from app.database.connection import Base, engine
from app.models import database_models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Infrastructure Dependency Mapping and Failure Impact Analysis",
    description=(
        "Map infrastructure dependencies and estimate "
        "the impact of component failures."
    ),
    version="1.0.0",
)

app.include_router(router)