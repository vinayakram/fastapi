from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey

Base = declarative_base()

class JobBoard(Base):
    __tablename__ = 'job_boards'
    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=False, unique=True)
    logo_url = Column(String, nullable=True)

    job_posts = relationship(
        "JobPost",
        back_populates="job_board",
        cascade="all, delete-orphan"
    )


class JobPost(Base):
    __tablename__ = "job_posts"

    id = Column(Integer, primary_key=True)
    job_board_id = Column(Integer, ForeignKey("job_boards.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="open")

    # ← Relationship back to board
    job_board = relationship("JobBoard", back_populates="job_posts")

    # ⭐ ADD THIS — cascade job applications!
    applications = relationship(
        "JobApplication",
        back_populates="job_post",
        cascade="all, delete-orphan"
    )


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True)
    job_post_id = Column(Integer, ForeignKey("job_posts.id", ondelete="CASCADE"), nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    resume_url = Column(String, nullable=False)

    # ← Relationship back to JobPost (pair with applications=...)
    job_post = relationship("JobPost", back_populates="applications")
