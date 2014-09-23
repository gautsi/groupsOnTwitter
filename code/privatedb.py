from sqlalchemy import MetaData, create_engine

engine = create_engine('mysql+pymysql://gautsi:gautsi@173.255.208.109/groups_on_twitter')

meta = MetaData()

meta.reflect(bind=engine)

users = meta.tables['users']

arrows = meta.tables['arrows']

conn = engine.connect()
