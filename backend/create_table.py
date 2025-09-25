from db import engine, Base
from models import Log, Metric

# This will create the tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
