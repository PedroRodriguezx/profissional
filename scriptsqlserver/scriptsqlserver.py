from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace these with your specific database credentials and info
DATABASE_TYPE = 'mssql+pyodbc'  # Use 'mssql+pymssql' if you prefer pymssql
USERNAME = '<>  # Replace with your database username
PASSWORD = '<>'  # Replace with your database password
HOST = '<>'  # Replace with your database host
PORT = '1433'  # Replace with your database port
DATABASE_NAME = 'sales_company'  # Replace with your database name
DRIVER_NAME = 'ODBC Driver 17 for SQL Server'  # Replace with the driver you have installed

# Create the database URI using string formatting
DATABASE_URI = "{}://{}:{}@{}:{}/{}?driver={}".format(DATABASE_TYPE, USERNAME, PASSWORD, HOST, PORT, DATABASE_NAME, DRIVER_NAME)

# Define a model class
Base = declarative_base()

class Sale(Base):
    __tablename__ = 'sales'  # Replace with your table name
    sale_id = Column(Integer, primary_key=True)
    sale_date = Column(Date)
    product_name = Column(String(255))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL(10, 2))
    total_price = Column(DECIMAL(10, 2))

# Create the engine and session
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)  # This will create the table if it doesn't exist
Session = sessionmaker(bind=engine)
session = Session()

# Create faker instance
fake = Faker()

# Generate and insert fake data
def generate_fake_data(entries=1000):  # Set to 1000 entries
    for _ in range(entries):
        fake_sale = Sale(
            sale_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
            product_name=fake.word(),
            quantity=fake.random_int(min=1, max=100),
            unit_price=fake.random_int(min=10, max=1000),
        )
        fake_sale.total_price = fake_sale.quantity * fake_sale.unit_price
        session.add(fake_sale)
    session.commit()

# Call the function to generate and insert fake data
generate_fake_data()
