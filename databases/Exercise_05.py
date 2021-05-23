'''
Using the API from the API section, write a program that makes a request to
get all of the users and all of their tasks.

Create tables in a new local database to model this data.

Think about what tables are required to model this data. Do you need two tables? Three?

Persist the data returned from the API to your database.

NOTE: If you run this several times you will be saving the same information in the table.
To prevent this, you should add a check to see if the record already exists before inserting it.

'''
import requests
import sqlalchemy
from databases.notes import password

# Check if database exists
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost')
# Query for existing databases
existing_databases = engine.execute("SHOW DATABASES;")
# Results are a list of single item tuples, so unpack each tuple
existing_databases = [d[0] for d in existing_databases]
# Create database if does not exist
if 'api_users_tasks' not in existing_databases:
    # create and activate database
    engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost')
    engine.execute(sqlalchemy.schema.CreateSchema('api_users_tasks'))
    engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/api_users_tasks')
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    # create tables
    users_table = sqlalchemy.Table('users_table', metadata,
                               sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                               sqlalchemy.Column('first_name', sqlalchemy.String(100), nullable=False),
                               sqlalchemy.Column('last_name', sqlalchemy.String(100), nullable=False),
                               sqlalchemy.Column('email', sqlalchemy.String(255), nullable=False),
                               sqlalchemy.Column('createdAt', sqlalchemy.BigInteger, nullable=False),
                               sqlalchemy.Column('updatedAt', sqlalchemy.BigInteger, nullable=False)
                               )
    tasks_table = sqlalchemy.Table('tasks_table', metadata,
                                   sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                                   sqlalchemy.Column('userId', sqlalchemy.Integer, nullable=False),
                                   sqlalchemy.Column('name', sqlalchemy.String(100), nullable=False),
                                   sqlalchemy.Column('description', sqlalchemy.String(255), nullable=False),
                                   sqlalchemy.Column('createdAt', sqlalchemy.BigInteger, nullable=False),
                                   sqlalchemy.Column('updatedAt', sqlalchemy.BigInteger, nullable=False),
                                   sqlalchemy.Column('completed', sqlalchemy.Boolean, nullable=False)
                                   )
    metadata.create_all(engine)
else:
    # connect to database
    engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/api_users_tasks')
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()

# load database tables
users_table = sqlalchemy.Table('users_table', metadata, autoload=True, autoload_with=engine)
tasks_table = sqlalchemy.Table('tasks_table', metadata, autoload=True, autoload_with=engine)

# make lists of user and task ids already in database
query = sqlalchemy.select([users_table.columns.id])
result_proxy = connection.execute(query)
user_result_set = result_proxy.fetchall()
user_list = []
for result in user_result_set:
    user_list.append(result['id'])

query = sqlalchemy.select([tasks_table.columns.id])
result_proxy = connection.execute(query)
task_result_set = result_proxy.fetchall()
task_list = []
for result in task_result_set:
    task_list.append(result['id'])

# download users from api
response = requests.get('http://demo.codingnomads.co:8080/tasks_api/users')
users_data = response.json()
# download tasks from api
response = requests.get('http://demo.codingnomads.co:8080/tasks_api/tasks')
tasks_data = response.json()

# add users to users_table, update if user exists
for i in range(len(users_data['data'])):
    if users_data['data'][i]['id'] in user_list:
        query = sqlalchemy.update(users_table).values(first_name=users_data['data'][i]['first_name'],last_name=users_data['data'][i]['last_name'],email=users_data['data'][i]['email'],createdAt=users_data['data'][i]['createdAt'],updatedAt=users_data['data'][i]['updatedAt'])
        result_proxy = connection.execute(query)
    else:
        query = sqlalchemy.insert(users_table).values(id=users_data['data'][i]['id'],first_name=users_data['data'][i]['first_name'],last_name=users_data['data'][i]['last_name'],email=users_data['data'][i]['email'],createdAt=users_data['data'][i]['createdAt'],updatedAt=users_data['data'][i]['updatedAt'])
        result_proxy = connection.execute(query)

# add tasks to tasks_table, update if task exists
for i in range(len(tasks_data['data'])):
    if tasks_data['data'][i]['id'] in task_list:
        query = sqlalchemy.update(tasks_table).values(userId=tasks_data['data'][i]['userId'],name=tasks_data['data'][i]['name'],description=tasks_data['data'][i]['description'],createdAt=tasks_data['data'][i]['createdAt'],updatedAt=tasks_data['data'][i]['updatedAt'],completed=tasks_data['data'][i]['completed'])
        result_proxy = connection.execute(query)
    else:
        query = sqlalchemy.insert(tasks_table).values(id=tasks_data['data'][i]['id'],userId=tasks_data['data'][i]['userId'],name=tasks_data['data'][i]['name'],description=tasks_data['data'][i]['description'],createdAt=tasks_data['data'][i]['createdAt'],updatedAt=tasks_data['data'][i]['updatedAt'],completed=tasks_data['data'][i]['completed'])
        result_proxy = connection.execute(query)

