from sqlalchemy import create_engine, text 

engine = create_engine("postgresql://henrik:crazy_db@localhost:5432/elpris")

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.scalar())
