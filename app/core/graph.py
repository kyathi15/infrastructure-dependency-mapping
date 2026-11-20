import networkx as nx
from sqlalchemy.orm import Session

from app.models.database_models import ComponentDB, DependencyDB


def build_graph(db: Session) -> nx.DiGraph:
    """Build a dependency graph using database records."""

    graph = nx.DiGraph()

    components = db.query(ComponentDB).all()

    for component in components:
        graph.add_node(
            component.id,
            id=component.id,
            name=component.name,
            type=component.type,
            criticality=component.criticality,
        )

    dependencies = db.query(DependencyDB).all()

    for dependency in dependencies:
        graph.add_edge(
            dependency.source_id,
            dependency.target_id,
        )

    return graph


def get_graph_data(db: Session) -> dict:
    """Return graph nodes and edges."""

    graph = build_graph(db)

    return {
        "nodes": list(graph.nodes(data=True)),
        "edges": [
            {"source": source, "target": target}
            for source, target in graph.edges()
        ],
    }