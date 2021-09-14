import subprocess

try:
    subprocess.run(["pipenv", "install"])
    subprocess.run(['pipenv', 'run', 'python', 'create_routine.py'])
except FileNotFoundError:
    print("pipenv not installed. Retry after installing pipenv.\n\nTry running the command:\npip install pipenv")
    exit(1)
except Exception as e:
    print("Something went wrong while trying to setup housekeep's environment.\n\nThe following exception was raised:\n\n")
    print(e)
    exit(1)