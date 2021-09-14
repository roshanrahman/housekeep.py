import subprocess
import os
from string import Template, ascii_lowercase
from rich.console import Console
import tkinter as tk
from tkinter import filedialog
import random

root = tk.Tk()
root.withdraw()

console = Console()
console.clear()


risky_directories = [
    ':/Windows', ':/Program Files', 'AppData', 'system32', '/root', '/usr', '/dev', '/boot'
]


def display_instructions(runner_file):
    if os.name == 'nt':
        console.rule(
            '[bold yellow]Instructions for scheduling this task on Windows[/]')
        console.print(f'''
        To run the routine, run the batch file in the same directory as this script.
        [bold white][link=file://{runner_file}]{runner_file}[/link][/]

        To schedule this routine to run automatically, create a Windows task using 
        Task Scheduler.

        1. Open Task Scheduler. (Start -> search "Task Scheduler")
        
        2. Click "Create Basic Task" on the right pane.
        
        3. Enter the Name and Description of your choice.
        
        4. Select the Trigger for the task. e.g. Daily at 1:00 PM, 
           When computer starts, etc. This will run the routine at the specified time.
        
        5. Select the Action for the task. Choose the "Start a program" action.
        
        6. Click Browse on "Program/Script" and locate the batch file 
           or copy/paste this path:

           [bold white link=file://{runner_file}]{runner_file}[/] 
           
           Copy the path for the next step as well.
        
        7. Paste the same path into the "Start in" field.
        
        8. Verify the task details and click Finish to create your scheduled task.

        For more details, google 'run batch script task scheduler' or check out 
        [link=https://stackoverflow.com/a/13173752]https://stackoverflow.com/a/13173752[/]
        ''')
        return
    if os.name == 'posix':
        console.rule(
            '[bold yellow]Instructions for scheduling this task on Linux/macOS[/]')
        console.print(f'''
        To run the routine, run the shell script in the same directory as this script.
        [bold white][link=file://{runner_file}]{runner_file}[/link][/]

        To schedule this routine to run automatically, you can use crontab on linux
        and macOS systems.

        It goes something like this:
        
        1. Run the crontab command using your terminal. 

        `crontab -e` or to directly specify an editor of your choice (e.g. nano), pass variable: `env EDITOR=nano crontab -e`

        2. The crontab file containing list of cron jobs will open. 

        3. If you are unsure about crontab syntax, check out [link=https://crontab.guru/]https://crontab.guru/[/]

        4. Add the following line to the crontab file, replacing * * * * * * with your own cron expression:

        * * * * * * [bold white][link=file://{runner_file}]{runner_file}[/link][/]

        e.g. 0 10 * * 6 [bold white][link=file://{runner_file}]{runner_file}[/link][/] 
        This will run the routine at 10:00 AM on Saturday. Customize as needed.

        5. Save the file. The task will recur automatically.

        For more details, google 'run create a cron job' or check out these links:
        On macOS: [link=https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx/]https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx/[/]
        On Ubuntu: [link=https://help.ubuntu.com/community/CronHowto]https://help.ubuntu.com/community/CronHowto[/]
        ''')
        return


def generate_random_name(prefix, suffix):
    return prefix + ''.join(random.choice(ascii_lowercase) for i in range(2)) + suffix


def build_routine_from_template(root, plugin, interface, regex, routine_name):
    current_working_directory = os.getcwd()
    template_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'routine_template.py.txt')
    template = Template(open(template_path).read())
    routine_path = os.path.join(
        current_working_directory, routine_name)
    with open(routine_path, 'w') as routine:
        routine.write(template.substitute(
            root=root, plugin=plugin, interface=interface, regex=f'r\'{regex}\'' if regex is not None else None))
    return routine_path


def build_batch_from_template(routine):
    extension = '.bat' if os.name == 'nt' else '.sh'
    current_working_directory = os.getcwd()
    template_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'batch_template.bat.txt')
    template = Template(open(template_path).read())
    batch_path = os.path.join(
        current_working_directory, f'{routine[:-3]}{extension}')
    with open(batch_path, 'w') as batch:
        batch.write(template.substitute(
            path=current_working_directory, routine=routine))
    return batch_path


def agree(value, default=None):
    if(default == 'y'):
        if(len(value) == 0):
            return True
    elif(default == 'n'):
        if(len(value) == 0):
            return False
    return len(value) > 0 and value.lower()[0] == 'y'


def main():
    plugin = None
    root = None
    regex = None
    routine_name = None

    console.rule("Create a new housekeeping routine")

    console.print(
        "\n[bold]This script will help you create a new housekeeping routine.[/] [grey]Press CTRL+C to cancel.[/grey]\n")

    console.print(
        '[bold blue underline]Step 1: Choose housekeeping action[/]\n')
    console.print(
        'Currently available action is "delete". This plugin will send files to Recycle Bin on Windows (Trash location on other systems)\n')
    value = console.input(
        '[bold yellow]Do you want to use this plugin? [Y/n] (default: yes)[/] > ')
    if(not agree(value, default='y')):
        raise KeyboardInterrupt
    console.print('[green]:white_check_mark: Plugin "delete" selected.[/]\n')
    plugin = 'delete'
    console.rule()

    console.print(
        '\n[bold blue underline]Step 2: Choose root folder this action will run in[/]\n')
    console.print(
        'Select the folder that you want to run this routine on. (No files outside this path will be affected.)\n')
    value = console.input(
        '[bold yellow]Press any key to open file browser dialog[/] > ')
    file_path = os.path.normpath(str(filedialog.askdirectory()).strip())
    if(file_path is None):
        raise KeyboardInterrupt
    if(any([item in file_path for item in risky_directories])):
        console.print(
            '\n[red]:bangbang: The path you provided appears to be an important system directory. It is not recommended to use this path.[/]')
        value = console.input(
            '[bold yellow]Do you still want to proceed with the selected path? [y/N] (default: no)[/] > ')
        if(not agree(value, default='n')):
            raise KeyboardInterrupt
    console.print(
        '[green]:white_check_mark: Folder selected: ' + file_path + '[/]\n')
    root = file_path
    console.rule()

    console.print(
        '\n[bold blue underline]Step 3: Provide a regex pattern to filter files[/]\n')
    console.print(
        'If you want to select only certain files to be affected, provide a regex pattern the files must match. Optional, but recommended.\n')
    value = console.input(
        '[bold yellow]Press enter your regex pattern or leave empty[/] > ')
    if(len(value) > 0):
        regex = value
        console.print(
            f'[green]:white_check_mark: Regex pattern selected: {regex}[/]\n')
    console.rule()

    console.print(
        '\n[bold blue underline]Step 4: Provide a name for your routine[/]\n')
    console.print(
        'If you want, provide a name for your routine. Skip to autogenerate a name.\n')
    value = console.input(
        '[bold yellow]Press enter the name for the routine or leave empty[/] > ')
    if(len(value) > 0):
        value = generate_random_name(prefix=f'{value}_', suffix='.py')
    else:
        value = generate_random_name(prefix=f'routine_{plugin}_', suffix='.py')
    console.print(
        f'[green]:white_check_mark: Routine name selected: {value}[/]\n')
    routine_name = value
    console.rule()

    file_gen = build_routine_from_template(
        root, plugin, 'cli', regex, routine_name)
    console.print('\n[green]:white_check_mark: Routine file generated.[/]')
    console.print(f'[link={file_gen}]{file_gen}[/]\n')
    batch_gen = build_batch_from_template(routine_name)
    console.print(
        '\n[green]:white_check_mark: Batch file to run routine generated.[/]')
    console.print(f'[link={batch_gen}]{batch_gen}[/]\n')
    display_instructions(batch_gen)


try:
    main()
except KeyboardInterrupt:
    console.print("[red]Aborted by user[/]")
    exit(0)
