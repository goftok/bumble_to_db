from enum import Enum as PyEnum
from sqlalchemy import create_engine, Column, Integer, String, Text, BLOB, ForeignKey, Index, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the base class
Base = declarative_base()


class Gender(PyEnum):
    MALE = 0
    FEMALE = 1
    NON_BINARY = 2
    OTHER = 3


# Define a model for main information
class MainInformationModel(Base):
    __tablename__ = "main_information"

    id = Column(Integer, primary_key=True)
    gender = Column(Enum(Gender))
    name = Column(String(255))
    age = Column(Integer)
    description = Column(Text)

    # Relationship to images
    images = relationship("ImagesModel", back_populates="main_info")


# Define a model for images
class ImagesModel(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    main_info_id = Column(Integer, ForeignKey("main_information.id"))
    image_data = Column(BLOB)

    # Relationship to main information
    main_info = relationship("MainInformationModel", back_populates="images")


# Add an index to improve query performance on frequently queried columns
Index("idx_main_information_gender", MainInformationModel.gender)
Index("idx_main_information_age", MainInformationModel.age)
Index("idx_images_main_info_id", ImagesModel.main_info_id)


def get_session(path: str) -> sessionmaker:
    # Create an SQLite engine that stores data in the local directory
    engine = create_engine(f"sqlite:///{path}")

    # Create all tables in the engine
    Base.metadata.create_all(engine)

    # Create a sessionmaker bound to this engine
    Session = sessionmaker(bind=engine)

    # Create a session
    session = Session()

    return session