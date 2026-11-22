from sqlalchemy import create_engine, text 

engine = create_engine("postgresql://postgres:elpris@localhost:5432/postgres")

with engine.connect() as conn:
    result = conn.exec
