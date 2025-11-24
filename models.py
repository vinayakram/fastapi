from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey


Base = declarative_base()

class JobBoard(Base):
  __tablename__ = 'job_boards'
  id = Column(Integer, primary_key=True)
  slug = Column(String, nullable=False, unique=True)
  job_posts = relationship("JobPost", back_populates="job_board")

class JobPost(Base):
    __tablename__ = 'job_posts'

    id = Column(Integer, primary_key=True)
    job_board_id = Column(Integer, ForeignKey("job_boards.id"), nullable=False)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # relationship back to job board
    job_board = relationship("JobBoard", back_populates="job_posts")
 