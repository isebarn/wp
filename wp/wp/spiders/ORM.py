import os
import json
from datetime import datetime
from sqlalchemy import ForeignKey, desc, create_engine, func, Column, BigInteger, Integer, Float, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pprint import pprint

engine = create_engine(os.environ.get('WP_DATABASE'), echo=False)
Base = declarative_base()

class PluginVersion(Base):
  __tablename__ = 'plugin_version'

  Id = Column('id', Integer, primary_key=True)
  Key = Column('key', String)
  Value = Column('value', String)

  def __init__(self, data):
    self.Key = data['key']
    self.Value = data['value']

class Plugin(Base):
  __tablename__ = 'plugin'

  Id = Column('id', Integer, primary_key=True)
  Name = Column('name', String)
  Version = Column('version', String)
  Site = Column('site', Integer, ForeignKey('site.id'))

  def __init__(self, plugin_name, version, site):
    self.Name = plugin_name
    self.Version = version
    self.Site = site

class Site(Base):
  __tablename__ = 'site'

  Id = Column('id', Integer, primary_key=True)
  Name = Column('name', String)
  WordPress = Column('wordpress', Boolean)


  def __init__(self, data):
    self.Name = data['site']
    self.WordPress = data['wordpress']

Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class Operations:

  def SavePlugin(plugin_name, version, site):
    plugin = session.query(Plugin).filter_by(Site=site, Name=plugin_name).first()
    if plugin == None:
      session.add(Plugin(plugin_name, version, site))

    elif plugin.Version != version:
      plugin.Version = version

    session.commit()

  def SaveSite(data):
    site = session.query(Site).filter_by(Name=data['site']).first()
    if site == None:
      site = Site(data)
      session.add(site)
      session.commit()

    return site


  def QuerySite():
    return session.query(Site).all()

  def QueryPlugin():
    return session.query(Plugin).all()

  def UpdatePluginVersion(data):
    plugin = session.query(PluginVersion).filter_by(Key=data['key']).first()
    if plugin == None:
      session.add(PluginVersion(data))
    else:
      plugin.Value = data['value']

    session.commit()


if __name__ == "__main__":
  pprint([x.__dict__ for x in Operations.QueryPlugin()])

