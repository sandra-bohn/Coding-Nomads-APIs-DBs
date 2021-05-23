'''

All of the following exercises should be done using sqlalchemy.

Using the provided database schema, write the necessary code to print information about the film and category table.

'''
import sqlalchemy
from databases.notes import password
from pprint import pprint

engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/sakila')
connection = engine.connect()
metadata = sqlalchemy.MetaData()
film_category = sqlalchemy.Table('film_category', metadata, autoload=True, autoload_with=engine)

print('Columns in film and category table:\n', film_category.columns.keys())
print('Film and category table metadata:')
pprint(repr(metadata.tables['film_category']))
