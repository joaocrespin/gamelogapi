from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import env

# Conexão com o banco de dados
engine = create_engine(f'postgresql://{env.POSTGRES_NAME}:{env.POSTGRES_PASSWORD}@localhost:5432/postgres')
# Gera as sessões conectadas a db
Session = sessionmaker(engine)
# Classe base para os models se conectarem, com o ORM
Base = declarative_base()