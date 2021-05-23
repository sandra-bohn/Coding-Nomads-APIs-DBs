'''

Please create a new Python application that interfaces with a brand new database.
This application must demonstrate the ability to:

    - create at least 3 tables
    - insert data to each table
    - update data in each table
    - select data from each table
    - delete data from each table
    - use at least one join in a select query

BONUS: Make this application something that a user can interact with from the CLI. Have options
to let the user decide what tables are going to be created, or what data is going to be inserted.
The more dynamic the application, the better!

'''
import sqlalchemy
from databases.notes import password

# Check if ice cream database exists
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost')
# Query for existing databases
existing_databases = engine.execute("SHOW DATABASES;")
# Results are a list of single item tuples, so unpack each tuple
existing_databases = [d[0] for d in existing_databases]
# Create database if does not exist
if 'ice_cream' not in existing_databases:
    # create and activate database
    engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost')
    engine.execute(sqlalchemy.schema.CreateSchema('ice_cream'))
    engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/ice_cream')
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()

    #create tables
    flavors = sqlalchemy.Table('flavors', metadata,
                           sqlalchemy.Column('flavorId', sqlalchemy.Integer(), autoincrement=True, primary_key=True),
                           sqlalchemy.Column('flavor_name', sqlalchemy.String(100), nullable=False),
                           sqlalchemy.Column('description', sqlalchemy.String(255), nullable=False),
                           sqlalchemy.Column('active', sqlalchemy.Boolean(), default=True)
                  )
    toppings = sqlalchemy.Table('toppings', metadata,
                           sqlalchemy.Column('toppingId', sqlalchemy.Integer(), autoincrement=True, primary_key=True),
                           sqlalchemy.Column('topping_name', sqlalchemy.String(100), nullable=False),
                           sqlalchemy.Column('description', sqlalchemy.String(255), nullable=False),
                           sqlalchemy.Column('active', sqlalchemy.Boolean(), default=True)
                  )
    orders = sqlalchemy.Table('orders', metadata,
                           sqlalchemy.Column('orderId', sqlalchemy.Integer(), autoincrement=True, primary_key=True),
                           sqlalchemy.Column('flavorId', sqlalchemy.Integer(), nullable=False),
                           sqlalchemy.Column('toppingId', sqlalchemy.Integer(), nullable=True),
                           sqlalchemy.Column('completed', sqlalchemy.Boolean(), default=False)
                  )
    metadata.create_all(engine)

    # upload data to tables
    flavors = sqlalchemy.Table('flavors', metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.insert(flavors)
    new_records = [{'flavor_name': 'vanilla', 'description': 'plain old vanilla', 'active': True},
                   {'flavor_name': 'chocolate', 'description': 'yummy chocolate', 'active': True},
                   {'flavor_name': 'strawberry', 'description': 'pink with strawberry chunks', 'active': True},
                   {'flavor_name': 'cookie dough', 'description': 'vanilla with chocolate chip cookie dough', 'active': True}]
    result_proxy = connection.execute(query, new_records)

    toppings = sqlalchemy.Table('toppings', metadata, autoload=True, autoload_with=engine)
    query = sqlalchemy.insert(toppings)
    new_records = [{'topping_name': 'none', 'description': 'no topping', 'active': True},
                   {'topping_name': 'rainbow sprinkles', 'description': 'colorful sugar shapes', 'active': True},
                   {'topping_name': 'chocolate sprinkles', 'description': 'brown sugar shapes', 'active': True},
                   {'topping_name': 'strawberry syrup', 'description': 'liquid strawberry', 'active': True},
                   {'topping_name': 'chopped nuts', 'description': 'chopped mixed nuts', 'active': True}]
    result_proxy = connection.execute(query, new_records)
else:
    engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/ice_cream')
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    flavors = sqlalchemy.Table('flavors', metadata,
                           sqlalchemy.Column('flavorId', sqlalchemy.Integer(), autoincrement=True, primary_key=True),
                           sqlalchemy.Column('flavor_name', sqlalchemy.String(100), nullable=False),
                           sqlalchemy.Column('description', sqlalchemy.String(255), nullable=False),
                           sqlalchemy.Column('active', sqlalchemy.Boolean(), default=True)
                  )
    toppings = sqlalchemy.Table('toppings', metadata,
                           sqlalchemy.Column('toppingId', sqlalchemy.Integer(), autoincrement=True, primary_key=True),
                           sqlalchemy.Column('topping_name', sqlalchemy.String(100), nullable=False),
                           sqlalchemy.Column('description', sqlalchemy.String(255), nullable=False),
                           sqlalchemy.Column('active', sqlalchemy.Boolean(), default=True)
                  )
    orders = sqlalchemy.Table('orders', metadata,
                           sqlalchemy.Column('orderId', sqlalchemy.Integer(), autoincrement=True, primary_key=True),
                           sqlalchemy.Column('flavorId', sqlalchemy.Integer(), nullable=False),
                           sqlalchemy.Column('toppingId', sqlalchemy.Integer(), nullable=True),
                           sqlalchemy.Column('completed', sqlalchemy.Boolean(), default=False)
                  )

# user interface
choice = 0
while choice != 99:
    choice = int(input('Choose an option:\n1) Place an order\n2) Complete an order\n3) Add a flavor\n4) Add a topping\n5) Change item status\n6) Cancel an order\n99) Exit\n'))
    if choice == 1:
        # Place an order
        # Print ice cream menu
        query = sqlalchemy.select([flavors.columns.flavorId, flavors.columns.flavor_name]).where(flavors.columns.active == True)
        result_proxy = connection.execute(query)
        result_set = result_proxy.fetchall()
        for result in result_set:
            print(f"{result['flavorId']}) {result['flavor_name']}")
        # Get ice cream choice
        myflavor = input('What flavor ice cream would you like? ')
        # Print toppings menu
        query = sqlalchemy.select([toppings.columns.toppingId, toppings.columns.topping_name]).where(toppings.columns.active == True)
        result_proxy = connection.execute(query)
        result_set = result_proxy.fetchall()
        for result in result_set:
            print(f"{result['toppingId']}) {result['topping_name']}")
        # Get topping choice
        mytopping = input('What topping would you like on your ice cream? ')
        # Add order to orders table
        orders = sqlalchemy.Table('orders', metadata, autoload=True, autoload_with=engine)
        query = sqlalchemy.insert(orders)
        new_record = [{'flavorId': myflavor, 'toppingId': mytopping}]
        result_proxy = connection.execute(query, new_record)
        # Display order
        join_statement = orders.join(flavors, flavors.columns.flavorId == orders.columns.flavorId).join(toppings, orders.columns.toppingId == toppings.columns.toppingId)
        query = sqlalchemy.select([orders.columns.orderId, flavors.columns.flavor_name, toppings.columns.topping_name]).select_from(join_statement).order_by(sqlalchemy.desc(orders.columns.orderId))
        result_proxy = connection.execute(query)
        result = result_proxy.fetchone()
        print(f"Your order for {result['flavor_name']} with {result['topping_name']} is order number {result['orderId']}.")
    elif choice == 2:
        # Complete an order
        # Show open orders
        join_statement = orders.join(flavors, flavors.columns.flavorId == orders.columns.flavorId).join(toppings, orders.columns.toppingId == toppings.columns.toppingId)
        query = sqlalchemy.select(
            [orders.columns.orderId, flavors.columns.flavor_name, toppings.columns.topping_name]).select_from(
            join_statement).where(orders.columns.completed == False)
        result_proxy = connection.execute(query)
        result_set = result_proxy.fetchall()
        for result in result_set:
            print(f"{result['orderId']}) {result['flavor_name']} with {result['topping_name']}")
        myorder = input("Which order would you like to complete? ")
        query = sqlalchemy.update(orders).values(completed=True).where(orders.columns.orderId == myorder)
        result = connection.execute(query)
        print(f"Order number {myorder} completed.")
    elif choice == 3:
        # Add a flavor
        newflavor = input("What is the name of the new flavor? ")
        newflavordesc = input("What is the description for the new flavor? ")
        query = sqlalchemy.insert(flavors).values(flavor_name=newflavor, description=newflavordesc)
        result_proxy = connection.execute(query)
        print(f"{newflavor} ice cream has been added to the menu")
    elif choice == 4:
        # Add a topping
        newtopping = input("What is the name of the new topping? ")
        newtoppingdesc = input("What is the description for the new flavor? ")
        query = sqlalchemy.insert(toppings).values(topping_name=newtopping, description=newtoppingdesc)
        result_proxy = connection.execute(query)
        print(f"{newtopping} topping has been added to the menu")
    elif choice == 5:
        # Change item status
        itemtype = int(input("For which type of item would you like to change the status?\n1) ice cream flavor\n2) topping\n"))
        if itemtype == 1:
            # update flavor status
            # Print ice cream menu
            query = sqlalchemy.select([flavors.columns.flavorId, flavors.columns.flavor_name])
            result_proxy = connection.execute(query)
            result_set = result_proxy.fetchall()
            for result in result_set:
                print(f"{result['flavorId']}) {result['flavor_name']}")
            # Get ice cream choice
            myflavor = input('Which flavor ice cream would you like to update? ')
            newstatus = input('Is this flavor available? y/n ')
            if newstatus == 'y':
                query = sqlalchemy.update(flavors).values(active=True).where(flavors.columns.flavorId == myflavor)
                result = connection.execute(query)
                print(f"{myflavor} is now available")
            elif newstatus == 'n':
                query = sqlalchemy.update(flavors).values(active=False).where(flavors.columns.flavorId == myflavor)
                result = connection.execute(query)
                print(f"{myflavor} is no longer available")
        elif itemtype == 2:
            # update topping status
            # Print toppings menu
            query = sqlalchemy.select([toppings.columns.toppingId, toppings.columns.topping_name])
            result_proxy = connection.execute(query)
            result_set = result_proxy.fetchall()
            for result in result_set:
                print(f"{result['toppingId']}) {result['topping_name']}")
            # Get topping choice
            mytopping = input('Which topping would you like to update? ')
            newstatus = input('Is this topping available? y/n ')
            if newstatus == 'y':
                query = sqlalchemy.update(toppings).values(active=True).where(toppings.columns.toppingId == mytopping)
                result = connection.execute(query)
                print(f"{mytopping} is now available")
            elif newstatus == 'n':
                query = sqlalchemy.update(toppings).values(active=False).where(toppings.columns.toppingId == mytopping)
                result = connection.execute(query)
                print(f"{mytopping} is no longer available")
        else:
            print('That is not an option.')
    elif choice == 6:
        # Cancel an order
        # Show open orders
        join_statement = orders.join(flavors, flavors.columns.flavorId == orders.columns.flavorId).join(toppings, orders.columns.toppingId == toppings.columns.toppingId)
        query = sqlalchemy.select(
            [orders.columns.orderId, flavors.columns.flavor_name, toppings.columns.topping_name]).select_from(
            join_statement).where(orders.columns.completed == False)
        result_proxy = connection.execute(query)
        result_set = result_proxy.fetchall()
        for result in result_set:
            print(f"{result['orderId']}) {result['flavor_name']} with {result['topping_name']}")
        myorder = input("Which order would you like to cancel? ")
        query = sqlalchemy.delete(orders).where(orders.columns.orderId == myorder)
        result = connection.execute(query)
        print(f"Order number {myorder} has been canceled.")
    elif choice == 99:
        print('Goodbye')
    else:
        print('That is not an option.')
