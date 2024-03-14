from typing import List, Optional
from datetime import date, time, datetime
from sqlalchemy import create_engine, Integer, String, ForeignKey, Column, Table
from sqlalchemy.orm import declarative_base, relationship, Mapped, sessionmaker, mapped_column


Base = declarative_base()

# Database connection and session creation
engine = create_engine('postgresql://postgres:postgres@localhost/SIST')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Tourist and Outing - many to many
association_table = Table(
    "association_table",
    Base.metadata,
    Column("tourist_id", ForeignKey("tourists.id")),
    Column("outing_id", ForeignKey("outing.id")),
)


class Tour(Base):
    __tablename__ = 'tours'
    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(400))
    length_in_hours: Mapped[int] = mapped_column(nullable=False)
    fee: Mapped[float] = mapped_column(nullable=False)

    # Tour(parent)-Test(child): one-to-one
    test: Mapped['Test'] = relationship(back_populates="tour")

    # Tour(parent)-QualifiedGuide(children): one-to-many
    qualified_guides: Mapped[List["QualifiedGuide"]] = relationship(back_populates="tour")
    # Tour(parent)-TourLocation(children): one-to-many
    tour_locations: Mapped[List["TourLocation"]] = relationship(back_populates="tour")
    # Tour(parent)-Outing(children): one-to-many
    outings: Mapped[List["Outing"]] = relationship(back_populates="tour")


class Guide(Base):
    __tablename__ = 'guides'
    employee_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    home_address: Mapped[str] = mapped_column(String(150), nullable=False)
    date_of_hire: Mapped[date] = mapped_column(nullable=False)


class Test(Base):
    __tablename__ = 'tests'
    qualification_name: Mapped[str] = mapped_column(primary_key=True)

    # a Test is associate with a Tour
    tour_name: Mapped[str] = mapped_column(ForeignKey("tours.name"), nullable=False)
    tour: Mapped["Tour"] = relationship(back_populates="test")


class GuideQualification(Base):
    __tablename__ = 'guide_qualifications'
    employee_id: Mapped[int] = mapped_column(ForeignKey('guides.employee_id'), primary_key=True)
    qualification_name: Mapped[str] = mapped_column(ForeignKey('tests.qualification_name'), primary_key=True)
    date_of_completion: Mapped[date] = mapped_column(nullable=False)

    # relationship with Tour: many to one
    tour_name: Mapped[int] = mapped_column(ForeignKey("tours.name"))
    tour: Mapped["Tour"] = relationship(back_populates="qualified_guide")
    # relationship with Outing: 1-1
    outing_id: Mapped[int] = mapped_column(ForeignKey("outings.id"))
    outing: Mapped["Outing"] = relationship(back_populates="qualified_guide")


class Location(Base):
    __tablename__ = 'locations'
    name: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(400), nullable=False)

    # location(parent):tour location(children): one to many 
    tour_locations = Mapped[List['TourLocation']] = relationship(back_populates="location")


class TourLocation(Base):
    __tablename__ = 'tour_locations'
    tour_name: Mapped[str] = mapped_column(ForeignKey('tours.name'), primary_key=True)
    Location_name: Mapped[str] = mapped_column(ForeignKey('locations.name'), primary_key=True)
    visit_order: Mapped[int] = mapped_column(nullable=False)

    # location(parent)-tour locations(children): one-to-many
    location: Mapped['Location'] = relationship(back_populates='tour_locations')
    # tour(parent)- tour locations(children): one-to-many
    tour: Mapped['Tour'] = relationship(back_populates="tour_locations")


class Outing(Base):
    __tablename__ = 'outings'
    id: Mapped[int] = mapped_column(primary_key=True)
    date_and_time: Mapped[datetime] = mapped_column(nullable=False)
    # relationship with Tour 1-many
    tour_name: Mapped[str] = mapped_column(ForeignKey("tours.name"), nullable=False)
    tour: Mapped['Tour'] = relationship(back_populates="outings")
    # relationship with QualifiedGuide 1-1
    qualified_employee_id: Mapped[int] = mapped_column(ForeignKey("qualified_guides.employee_id"),                                                  nullable=False)
    qualified_guide: Mapped['QualifiedGuide'] = relationship(back_populates="outing")


class Tourist(Base):
    __tablename__ = 'tourists'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(unique=True, nullable=False)
    # relationship with Outing: many to many
    outings: Mapped[List[Outing]] = relationship(secondary='association_table')

Base.metadata.create_all(engine)