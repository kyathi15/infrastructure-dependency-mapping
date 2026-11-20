import uuid
import networkx as nx
from sqlalchemy.orm import Session

from app.models.database_models import ComponentDB, DependencyDB
from app.models.schemas import DependencyCreate


def create_dependency(dependency_data: DependencyCreate, db: Session) -> dict:

    source_id = dependency_data.source_id
    target_id = dependency_data.target_id

    # Check source component
    source = db.query(ComponentDB).filter(
        ComponentDB.id == source_id
    ).first()

    if not source:
        raise ValueError(f"Component '{source_id}' does not exist.")

    # Check target component
    target = db.query(ComponentDB).filter(
        ComponentDB.id == target_id
    ).first()

    if not target:
        raise ValueError(f"Component '{target_id}' does not exist.")

    # Prevent self-dependency
    if source_id == target_id:
        raise ValueError("A component cannot depend on itself.")

    # Check duplicate dependency
    existing = db.query(DependencyDB).filter(
        DependencyDB.source_id == source_id,
        DependencyDB.target_id == target_id,
    ).first()

    if existing:
        raise ValueError("This dependency already exists.")

    # Get existing dependencies from database
    dependencies = db.query(DependencyDB).all()

    # Create graph
    graph = nx.DiGraph()

    # Add all components to graph
    components = db.query(ComponentDB).all()

    for component in components:
        graph.add_node(component.id)

    # Add existing dependency connections
    for dependency in dependencies:
        graph.add_edge(
            dependency.source_id,
            dependency.target_id,
        )

    # Check for circular dependency
    if nx.has_path(graph, target_id, source_id):
        raise ValueError("This dependency would create a cycle.")

    # Save new dependency
    new_dependency = DependencyDB(
        id=str(uuid.uuid4()),
        source_id=source_id,
        target_id=target_id,
    )

    db.add(new_dependency)
    db.commit()
    db.refresh(new_dependency)

    return {
        "source_id": source_id,
        "target_id": target_id,
        "message": f"{target_id} depends on {source_id}",
    }