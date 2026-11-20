
# Infrastructure Dependency Mapping and Failure Impact Analysis

## 1. Project Overview

Infrastructure Dependency Mapping and Failure Impact Analysis is a web-based application designed to visualize relationships between IT infrastructure components and analyze the potential impact of component failures.

The system helps identify which services and applications may be affected when an infrastructure component fails.

The project uses graph-based dependency mapping to represent infrastructure relationships and NetworkX to perform failure impact analysis.

## 2. Problem Statement

Modern IT infrastructure consists of interconnected components such as databases, servers, APIs, services, and applications.

A failure in one component can affect multiple dependent components. Identifying these dependencies manually can be difficult and time-consuming.

This project provides a centralized dashboard to map infrastructure dependencies, visualize connections, and estimate the impact of component failures.

## 3. Project Objectives

- Manage IT infrastructure components.
- Create and maintain dependency relationships.
- Visualize infrastructure dependencies using a directed graph.
- Identify components affected by a simulated failure.
- Display the total number of affected components.
- Highlight failed and affected components visually.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend API development |
| Streamlit | Frontend dashboard |
| SQLite | Database |
| SQLAlchemy | Database interaction |
| NetworkX | Graph creation and failure analysis |
| Streamlit-Agraph | Dependency graph visualization |
| Pydantic | Data validation |
| Pytest | Backend testing |

## 5. System Architecture

The application follows a simple three-layer architecture:

1. **Frontend Layer:** Streamlit provides the user interface and dashboard.
2. **Backend Layer:** FastAPI handles requests, component management, dependency management, and failure analysis.
3. **Database and Graph Layer:** SQLite stores infrastructure information, while NetworkX processes dependency relationships and failure impact.

### Architecture Flow

```text
        USER
         |
         v
  STREAMLIT FRONTEND
         |
         v
      FASTAPI
         |
    +----+----+
    |         |
    v         v
  SQLITE   NETWORKX
 DATABASE  GRAPH ANALYSIS
    |         |
    +----+----+
         |
         v
  FAILURE IMPACT RESULTS
         |
         v
  STREAMLIT DASHBOARD
```

## 6. Main Features

### Component Management
- Add infrastructure components.
- Assign component IDs and names.
- Select component types.
- Assign criticality levels.

### Dependency Mapping
- Create relationships between components.
- Prevent duplicate dependencies.
- Prevent circular dependencies.
- Display existing dependencies.

### Infrastructure Visualization
- Display components as graph nodes.
- Display dependencies as directed edges.
- Use different colors to represent component criticality.

### Failure Impact Analysis
- Select a component for failure simulation.
- Identify all downstream dependent components.
- Calculate the total number of affected components.
- Display affected component details.

### Failure Graph Highlighting
- Red indicates the failed component.
- Orange indicates affected components.
- Green indicates unaffected components.
- Reset the graph to its normal criticality colors.

## 7. Sample Infrastructure Scenario

The project uses the following sample infrastructure:

```text
Main Database
      |
      v
Login Service
      |
      v
User Portal
```

If the Main Database fails:

- Main Database is marked as failed.
- Login Service is identified as affected.
- User Portal is identified as affected.
- Total affected components: 2.

## 8. Project Folder Structure

```text
servicenow/
|
|-- app/
|   |-- api/
|   |-- core/
|   |-- database/
|   |-- models/
|   |-- services/
|   |-- main.py
|
|-- frontend/
|   |-- app.py
|
|-- tests/
|   |-- test_impact.py
|
|-- data/
|
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## 9. Installation and Execution

### Step 1: Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 2: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Start the backend

```powershell
python -m uvicorn app.main:app --reload
```

Backend API:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### Step 4: Start the frontend

Open another VS Code terminal, activate the virtual environment, and run:

```powershell
python -m streamlit run frontend/app.py
```

Frontend dashboard:

http://localhost:8501

## 10. Testing

The backend is tested using Pytest.

Run the tests using:

```powershell
python -m pytest -v
```

The project has successfully passed six backend tests covering:

- Component creation and listing.
- Dependency creation.
- Duplicate dependency prevention.
- Circular dependency prevention.
- Failure impact analysis.
- Unknown component failure handling.

**Test Result:** 6 tests passed.

## 11. Limitations

- Infrastructure components and dependencies are entered manually.
- Failure analysis is a simulation and does not detect real-time infrastructure outages.
- The current application is a prototype and does not include enterprise authentication or live infrastructure monitoring.

## 12. Future Enhancements

- Real-time infrastructure monitoring.
- Automated dependency discovery.
- User authentication and role-based access.
- Advanced failure prediction.
- Cloud infrastructure integration.
- Detailed reports and analytics.

## 13. Conclusion

The Infrastructure Dependency Mapping and Failure Impact Analysis project demonstrates how graph-based techniques can help understand infrastructure relationships and estimate the impact of component failures.

By combining FastAPI, Streamlit, SQLite, and NetworkX, the application provides an interactive platform for managing infrastructure components, visualizing dependencies, and performing failure impact simulations.
