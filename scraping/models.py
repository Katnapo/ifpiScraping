from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, index=True)
    song_title = Column(Text, unique=True)
    page_url = Column(Text)
    date = Column(String(50))

    download_links = relationship("DownloadLink", back_populates="song")

class DownloadLink(Base):
    __tablename__ = 'download_links'

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey('songs.id'))
    download_url = Column(Text, unique=True)

    song = relationship("Song", back_populates="download_links")

class VariableType(Base):
    __tablename__ = 'variable_types'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))

    variables = relationship("Variable", back_populates="variable_type")

class Variable(Base):
    __tablename__ = 'variables'

    id = Column(Integer, primary_key=True, index=True)
    variable_type_id = Column(Integer, ForeignKey('variable_types.id'))
    data = Column(String(200), nullable=False, default='')
    timestamp = Column(String, nullable=False)

    variable_type = relationship("VariableType", back_populates="variables")