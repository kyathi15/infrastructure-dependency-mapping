from sqlalchemy import Column, ForeignKey, String

from app.database.connection import Base


class ComponentDB(Base):
    __tablename__ = "components"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    criticality = Column(String, nullable=False)


class DependencyDB(Base):
    __tablename__ = "dependencies"

    id = Column(String, primary_key=True, index=True)
    source_id = Column(
        String,
        ForeignKey("components.id"),
        nullable=False,
    )
    target_id = Column(
        String,
        ForeignKey("components.id"),
        nullable=False,
    )