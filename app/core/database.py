from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
host = os.environ.get('POSTGRES_HOST', 'localhost')
password = os.environ.get('POSTGRES_PASSWORD', 'YourPW')

# Conexão com o banco de dados
engine = create_engine(f'postgresql://postgres:{password}@{host}:5432/postgres')
# Gera as sessões conectadas a db
Session = sessionmaker(engine)
# Classe base para os models se conectarem, com o ORM
Base = declarative_base()