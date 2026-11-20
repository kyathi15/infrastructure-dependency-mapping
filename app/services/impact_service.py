import networkx as nx
from sqlalchemy.orm import Session

from app.core.graph import build_graph


def analyze_failure(component_id: str, db: Session) -> dict:

    graph = build_graph(db)

    if component_id not in graph:
        raise ValueError(
            f"Component '{component_id}' does not exist."
        )

    failed_component = graph.nodes[component_id]

    affected_ids = list(
        nx.descendants(graph, component_id)
    )

    affected_ids.sort(
        key=lambda node_id: nx.shortest_path_length(
            graph,
            component_id,
            node_id,
        )
    )

    affected_components = []

    for node_id in affected_ids:
        component = dict(graph.nodes[node_id])

        component["dependency_distance"] = (
            nx.shortest_path_length(
                graph,
                component_id,
                node_id,
            )
        )

        affected_components.append(component)

    return {
        "failed_component": failed_component,
        "total_affected": len(affected_components),
        "affected_components": affected_components,
        "message": (
            f"{len(affected_components)} component(s) may be affected."
        ),
    }