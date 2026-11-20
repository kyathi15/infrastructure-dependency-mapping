from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.graph import get_graph_data
from app.database.connection import get_db
from app.models.schemas import ComponentCreate, DependencyCreate
from app.services.component_service import (
    create_component,
    list_components,
)
from app.services.dependency_service import create_dependency
from app.services.impact_service import analyze_failure

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Infrastructure Impact Analyzer API is running"
    }


@router.get("/components")
def get_components(db: Session = Depends(get_db)):
    return list_components(db)


@router.post("/components", status_code=201)
def add_new_component(
    component: ComponentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_component(component, db)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/dependencies", status_code=201)
def add_new_dependency(
    dependency: DependencyCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_dependency(dependency, db)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/graph")
def get_graph(db: Session = Depends(get_db)):
    return get_graph_data(db)


@router.post("/simulate-failure/{component_id}")
def simulate_failure(
    component_id: str,
    db: Session = Depends(get_db),
):
    try:
        return analyze_failure(component_id, db)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))