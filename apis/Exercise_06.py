'''

Create an application that interfaces with the user via the CLI - prompt the user with a menu such as:

Please select from the following options (enter the number of the action you'd like to take):
1) Create a new account (POST)
2) View all your tasks (GET)
3) View your completed tasks (GET)
4) View only your incomplete tasks (GET)
5) Create a new task (POST)
6) Update an existing task (PATCH/PUT)
7) Delete a task (DELETE)

It is your responsibility to build out the application to handle all menu options above.

'''
import requests
choice = 0
while choice != 99:
    # Get user input
    choice = int(input("Please select from the following options (enter the number of the action you'd like to take):\n1) Create a new account\n2) View all your tasks\n3) View your completed tasks\n4) View only your incomplete tasks\n5) Create a new task\n6) Update an existing task\n7) Delete a task\n99) Exit\n"))
    # execute chosen task
    if choice == 1:
        # create a new account
        firstname = input('Enter first name: ')
        lastname = input('Enter last name: ')
        email = input('Enter email: ')
        body = {'first_name': firstname, 'last_name': lastname, 'email': email}
        response = requests.post('http://demo.codingnomads.co:8080/tasks_api/users', json=body)
        response = requests.get('http://demo.codingnomads.co:8080/tasks_api/users')
        data = response.json()
        print('Your new account information is:\n', data['data'][-1])
    elif choice == 2:
        # view user's tasks
        userid = int(input('Enter your userId: '))
        response = requests.get(f'http://demo.codingnomads.co:8080/tasks_api/tasks?userId={userid}&complete=trueORcomplete=false')
        data = response.json()
        print('Your tasks are:')
        for i in range(len(data['data'])):
            print(data['data'][i])
    elif choice == 3:
        # view user's completed tasks
        userid = int(input('Enter your userId: '))
        response = requests.get(f'http://demo.codingnomads.co:8080/tasks_api/tasks?userId={userid}&complete=true')
        data = response.json()
        print('Your completed tasks are:')
        for i in range(len(data['data'])):
            print(data['data'][i])
    elif choice == 4:
        # view user's incomplete tasks
        userid = input('Enter your userId: ')
        response = requests.get(f'http://demo.codingnomads.co:8080/tasks_api/tasks?userId={userid}&complete=false')
        data = response.json()
        print('Your incomplete tasks are:')
        for i in range(len(data['data'])):
            print(data['data'][i])
    elif choice == 5:
        # create a new task
        userid = int(input('Enter userId: '))
        taskname = input('Enter task name: ')
        description = input('Enter task description: ')
        body = {'userId': userid, 'name': taskname, 'description': description, 'completed': 'false'}
        response = requests.post('http://demo.codingnomads.co:8080/tasks_api/tasks', json=body)
        response = requests.get('http://demo.codingnomads.co:8080/tasks_api/tasks')
        data = response.json()
        print('You added a task:\n', data['data'][-1])
    elif choice == 6:
        # update an existing task
        task = input('Which task would you like to update? Enter task id: ')
        response = requests.get(f'http://demo.codingnomads.co:8080/tasks_api/tasks/{task}')
        data = response.json()
        print(data['data'])
        newtask = input('Update task name (y/n)? ')
        if newtask == 'y':
            data['data']['name'] = input('Enter new task name: ')
        newdesc = input('Update task description (y/n)? ')
        if newdesc == 'y':
            data['data']['description'] = input('Enter new task description: ')
        newstatus = input('Update task status (y/n)? ')
        if newstatus == 'y':
            data['data']['completed'] = input('Has task been completed (true/false)? ')
        response = requests.put('http://demo.codingnomads.co:8080/tasks_api/tasks', json=data['data'])
        response = requests.get(f'http://demo.codingnomads.co:8080/tasks_api/tasks/{task}')
        data = response.json()
        print(f'You updated task {task}:\n', data['data'])
    elif choice == 7:
        # delete a task
        task = input("Enter the number of the task you would like to delete: ")
        response = requests.delete(f'http://demo.codingnomads.co:8080/tasks_api/tasks/{task}')
        print(f'Task {task} has been deleted.')
    elif choice == 99:
        print('Goodbye')
    else:
        print('Your choice was not an option.')
