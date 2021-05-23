'''
Consider each of the tasks below as a separate database query. Using SQLAlchemy, which is the necessary code to:

- Select all the actors with the first name of your choice

- Select all the actors and the films they have been in

- Select all the actors that have appeared in a category of a comedy of your choice

- Select all the comedic films and sort them by rental rate

- Using one of the statements above, add a GROUP BY statement of your choice

- Using one of the statements above, add a ORDER BY statement of your choice

'''
import sqlalchemy
from databases.notes import password
from pprint import pprint

engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/sakila')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# create table objects
actor = sqlalchemy.Table('actor', metadata, autoload=True, autoload_with=engine)
film = sqlalchemy.Table('film', metadata, autoload=True, autoload_with=engine)
film_actor = sqlalchemy.Table('film_actor', metadata, autoload=True, autoload_with=engine)
category = sqlalchemy.Table('category', metadata, autoload=True, autoload_with=engine)
film_category = sqlalchemy.Table('film_category', metadata, autoload=True, autoload_with=engine)

# Select all the actors with the first name of your choice
query = sqlalchemy.select([actor.columns.first_name, actor.columns.last_name]).where(actor.columns.first_name == 'SANDRA')
result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
print('All actors with first name = Sandra:')
pprint(result_set)

# Select all the actors and the films they have been in
join_statement = actor.join(film_actor, film_actor.columns.actor_id == actor.columns.actor_id).join(film, film.columns.film_id == film_actor.columns.film_id)
query = sqlalchemy.select([actor.columns.first_name, actor.columns.last_name, film.columns.title]).select_from(join_statement)
result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
print('All actors and their films:')
pprint(result_set)

# Select all the actors that have appeared in a category of a comedy of your choice
join_statement = actor.join(film_actor, film_actor.columns.actor_id == actor.columns.actor_id).join(film_category, film_category.columns.film_id == film_actor.columns.film_id)
query = sqlalchemy.select([actor.columns.first_name, actor.columns.last_name]).select_from(join_statement).where(film_category.columns.category_id == 5).group_by(actor.columns.actor_id)
result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
print('All actors that appeared in a Comedy:')
pprint(result_set)

# Select all the comedic films and sort them by rental rate
join_statement = film.join(film_category, film_category.columns.film_id == film.columns.film_id)
query = sqlalchemy.select([film.columns.title, film.columns.rental_rate]).select_from(join_statement).where(film_category.columns.category_id == 5).order_by(film.columns.rental_rate)
result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
print('Comedic films sorted by rental rate:')
pprint(result_set)

# Using one of the statements above, add a GROUP BY statement of your choice
join_statement = actor.join(film_actor, film_actor.columns.actor_id == actor.columns.actor_id).join(film, film.columns.film_id == film_actor.columns.film_id)
query = sqlalchemy.select([actor.columns.first_name, actor.columns.last_name]).select_from(join_statement).group_by(actor.columns.actor_id)
result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
print('All actors that have appeared in films:')
pprint(result_set)

# Using one of the statements above, add an ORDER BY statement of your choice
join_statement = actor.join(film_actor, film_actor.columns.actor_id == actor.columns.actor_id).join(film_category, film_category.columns.film_id == film_actor.columns.film_id)
query = sqlalchemy.select([actor.columns.first_name, actor.columns.last_name]).select_from(join_statement).where(film_category.columns.category_id == 5).group_by(actor.columns.actor_id).order_by(actor.columns.last_name)
result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()
print('All actors that appeared in a Comedy ordered by last name:')
pprint(result_set)