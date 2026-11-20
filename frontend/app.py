
import streamlit as st
import requests
from streamlit_agraph import agraph, Node, Edge, Config

# Backend API address
API_URL = "http://127.0.0.1:8000"

# Page configuration
st.set_page_config(
    page_title="Infrastructure Impact Analyzer",
    page_icon="🏗️",
    layout="wide",
)

# Store failure simulation results between Streamlit reruns
if "failure_impact" not in st.session_state:
    st.session_state.failure_impact = None

# Page title
st.title("🏗️ Infrastructure Dependency Mapping")
st.subheader("Failure Impact Analysis Dashboard")

st.write(
    "Manage infrastructure components, map dependencies, "
    "and analyze the impact of component failures."
)

# Check backend connection
try:
    response = requests.get(f"{API_URL}/", timeout=5)
    response.raise_for_status()
    st.success("Backend connected successfully!")

except requests.RequestException:
    st.error(
        "Backend is not running. Start FastAPI in a separate terminal."
    )
    st.stop()


# Load dashboard data
st.header("Infrastructure Overview")

try:
    components_response = requests.get(
        f"{API_URL}/components", timeout=5
    )
    components_response.raise_for_status()
    components = components_response.json()

    graph_response = requests.get(
        f"{API_URL}/graph", timeout=5
    )
    graph_response.raise_for_status()
    graph_data = graph_response.json()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Components", len(components))

    with col2:
        st.metric("Total Dependencies", len(graph_data["edges"]))

    with col3:
        st.metric(
            "Critical Components",
            sum(
                1 for c in components
                if c["criticality"].lower() == "critical"
            ),
        )

except requests.RequestException as error:
    st.error(f"Could not load dashboard data: {error}")
    st.stop()


# Display components
st.header("Infrastructure Components")

if components:
    st.dataframe(components, use_container_width=True)
else:
    st.info("No components have been added yet.")


# Add new component
st.header("Add New Component")

with st.form("component_form"):
    component_id = st.text_input("Component ID")
    component_name = st.text_input("Component Name")

    component_type = st.selectbox(
        "Component Type",
        ["server", "database", "api", "service", "application"],
    )

    criticality = st.selectbox(
        "Criticality",
        ["low", "medium", "high", "critical"],
    )

    component_submit = st.form_submit_button("Add Component")

    if component_submit:
        if not component_id.strip() or not component_name.strip():
            st.error(
                "Please enter both Component ID and Component Name."
            )
        else:
            try:
                result = requests.post(
                    f"{API_URL}/components",
                    json={
                        "id": component_id.strip(),
                        "name": component_name.strip(),
                        "type": component_type,
                        "criticality": criticality,
                    },
                    timeout=5,
                )

                if result.status_code == 201:
                    st.success("Component added successfully!")
                    st.rerun()
                else:
                    st.error(
                        result.json().get("detail", result.text)
                    )

            except requests.RequestException as error:
                st.error(f"Could not add component: {error}")


# Dependency Mapping
st.header("Dependency Mapping")

if graph_data["edges"]:
    st.write("Existing dependency connections:")
    st.dataframe(
        graph_data["edges"],
        use_container_width=True,
    )
else:
    st.info("No dependencies have been added yet.")


# Add New Dependency
st.subheader("Add New Dependency")

if len(components) >= 2:

    component_names = {
        f'{c["name"]} ({c["id"]})': c["id"]
        for c in components
    }

    with st.form("dependency_form"):

        source_name = st.selectbox(
            "Dependency (Source Component)",
            list(component_names.keys()),
        )

        target_name = st.selectbox(
            "Dependent (Target Component)",
            list(component_names.keys()),
        )

        dependency_submit = st.form_submit_button(
            "Add Dependency"
        )

        if dependency_submit:

            source_id = component_names[source_name]
            target_id = component_names[target_name]

            if source_id == target_id:
                st.error("A component cannot depend on itself.")

            else:
                try:
                    result = requests.post(
                        f"{API_URL}/dependencies",
                        json={
                            "source_id": source_id,
                            "target_id": target_id,
                        },
                        timeout=5,
                    )

                    if result.status_code == 201:
                        st.success("Dependency added successfully!")
                        st.rerun()
                    else:
                        st.error(
                            result.json().get("detail", result.text)
                        )

                except requests.RequestException as error:
                    st.error(
                        f"Could not add dependency: {error}"
                    )

else:
    st.info(
        "Add at least two components to create a dependency."
    )


# Failure Impact Simulation
st.header("Failure Impact Simulation")

component_options = {
    f'{c["name"]} ({c["id"]})': c["id"]
    for c in components
}

if component_options:

    selected_component = st.selectbox(
        "Select a component to simulate failure",
        list(component_options.keys()),
    )

    col1, col2 = st.columns(2)

    with col1:
        simulate_button = st.button(
            "Simulate Failure",
            use_container_width=True,
        )

    with col2:
        reset_button = st.button(
            "Reset Graph",
            use_container_width=True,
        )

    # Run failure simulation
    if simulate_button:

        failed_id = component_options[selected_component]

        try:
            result = requests.post(
                f"{API_URL}/simulate-failure/{failed_id}",
                timeout=5,
            )

            if result.status_code == 200:
                st.session_state.failure_impact = result.json()
                st.success("Failure simulation completed!")

            else:
                st.error(
                    result.json().get("detail", result.text)
                )

        except requests.RequestException as error:
            st.error(
                f"Failure simulation failed: {error}"
            )

    # Reset failure highlighting
    if reset_button:
        st.session_state.failure_impact = None
        st.rerun()

    # Display failure analysis results
    impact = st.session_state.failure_impact

    if impact:

        st.subheader("Failure Analysis Results")

        st.metric(
            "Total Affected Components",
            impact["total_affected"],
        )

        failed_component = impact["failed_component"]
        st.write(
            f'**Failed Component:** {failed_component["name"]}'
        )

        if impact["affected_components"]:
            st.write("Affected components:")
            st.dataframe(
                impact["affected_components"],
                use_container_width=True,
            )
        else:
            st.success(
                "No dependent components were affected."
            )

else:
    st.info(
        "Add a component before running failure simulation."
    )


# Visual Dependency Graph
st.header("Infrastructure Dependency Graph")

try:
    visual_graph_response = requests.get(
        f"{API_URL}/graph", timeout=5
    )
    visual_graph_response.raise_for_status()
    visual_graph_data = visual_graph_response.json()

    nodes = []
    edges = []

    # Normal criticality colors
    criticality_colors = {
        "critical": "#FF4B4B",
        "high": "#FF9F43",
        "medium": "#FFD93D",
        "low": "#2ECC71",
    }

    # Failure highlighting colors
    failure_color = "#FF0000"
    affected_color = "#FF8C00"
    unaffected_color = "#2ECC71"

    # Get failure information
    impact = st.session_state.failure_impact

    failed_id = None
    affected_ids = set()

    if impact:
        failed_id = impact["failed_component"]["id"]

        affected_ids = {
            component["id"]
            for component in impact["affected_components"]
        }

    # Create graph nodes
    for component in components:

        component_id = component["id"]

        # Use normal criticality colors by default
        node_color = criticality_colors.get(
            component["criticality"].lower(),
            "#808080",
        )

        # Change colors after failure simulation
        if impact:

            if component_id == failed_id:
                node_color = failure_color

            elif component_id in affected_ids:
                node_color = affected_color

            else:
                node_color = unaffected_color

        nodes.append(
            Node(
                id=component_id,
                label=(
                    f'{component["name"]}\n'
                    f'({component["type"]})\n'
                    f'Criticality: {component["criticality"]}'
                ),
                size=35,
                color=node_color,
            )
        )

    # Create graph edges
    for dependency in visual_graph_data["edges"]:
        edges.append(
            Edge(
                source=dependency["source"],
                target=dependency["target"],
            )
        )

    # Display graph
    if nodes:

        config = Config(
            width=900,
            height=500,
            directed=True,
            physics=True,
            hierarchical=True,
        )

        agraph(
            nodes=nodes,
            edges=edges,
            config=config,
        )

        # Display appropriate legend
        st.subheader("Graph Legend")

        if impact:
            st.markdown(
                """
                🔴 **Red:** Failed Component

                🟠 **Orange:** Affected Components

                🟢 **Green:** Unaffected Components
                """
            )
        else:
            st.markdown(
                """
                🔴 **Red:** Critical

                🟠 **Orange:** High

                🟡 **Yellow:** Medium

                🟢 **Green:** Low
                """
            )

    else:
        st.info("Add components to display the graph.")

except requests.RequestException as error:
    st.error(
        f"Could not display dependency graph: {error}"
    )
