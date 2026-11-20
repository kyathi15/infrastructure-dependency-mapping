from sqlalchemy.orm import Session

from app.models.database_models import ComponentDB
from app.models.schemas import ComponentCreate


def create_component(
    component_data: ComponentCreate,
    db: Session,
) -> dict:

    existing = db.query(ComponentDB).filter(
        ComponentDB.id == component_data.id
    ).first()

    if existing:
        raise ValueError(
            f"Component '{component_data.id}' already exists."
        )

    component = ComponentDB(**component_data.model_dump())

    db.add(component)
    db.commit()
    db.refresh(component)

    return {
        "id": component.id,
        "name": component.name,
        "type": component.type,
        "criticality": component.criticality,
    }


def list_components(db: Session) -> list[dict]:

    components = db.query(ComponentDB).all()

    return [
        {
            "id": component.id,
            "name": component.name,
            "type": component.type,
            "criticality": component.criticality,
        }
        for component in components
    ]