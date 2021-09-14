import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live


class cli(object):
    def get_file_size(self, file):
        return os.path.getsize(file) / 1024 / 1024

    def __init__(self, files, plugin, confirm, **kwargs):
        self.name = 'cli'
        self.description = 'A rich Terminal based experience'
        self.plugin = plugin
        self.confirm = bool(confirm)
        self.files = files
        self.console = Console()
        self.confirmed = not confirm
        self.progress = [(False, '') for file in files]
        self.filesizes = [
            f'{round(self.get_file_size(file), 2)} MB' for file in files]

    def generate_table(self):
        table = Table(title=self.plugin.name, show_header=True)
        table.add_column('File')
        table.add_column('Size')
        table.add_column('Progress')
        for file in self.files:
            progress_indicator = ' -- '
            if(self.progress[self.files.index(file)][0] == True and self.progress[self.files.index(file)][1] == ''):
                progress_indicator = ':heavy_check_mark: Done'
            if(self.progress[self.files.index(file)][0] == True and self.progress[self.files.index(file)][1] != ''):
                progress_indicator = ':cross_mark: Error!'
            table.add_row(file, self.filesizes[self.files.index(file)], progress_indicator)
        return table

    def on_file_success(self, f, live):
        self.progress[self.files.index(f)] = (True, '')
        live.update(self.generate_table())
        live.refresh()

    def on_file_error(self, f, e, live):
        self.progress[self.files.index(f)] = (True, e)
        live.update(self.generate_table())
        live.refresh()

    def run(self):
        self.console.print(self.generate_table())
        self.console.print(
            f'\nThe housekeeping action [bold red]{self.plugin.name}[/bold red] will be applied on the files listed above.')
        if(self.confirm):
            self.console.print(
                f'Are you sure you want to continue? [bold red](Y)es[/bold red] or [bold red](N)o[/bold red]')
            value = self.console.input().lower()
            if(value == 'y' or value == 'yes'):
                self.confirmed = True
            else:
                self.console.print(
                    f'[bold red]Aborted by user. [/bold red]')
                exit(0)

        self.console.clear()

        with Live(self.generate_table(), auto_refresh=False) as live:
            if(self.confirmed):
                self.plugin.run_action(self.files, lambda f: self.on_file_success(
                    f, live), lambda f, e: self.on_file_error(f, e, live))

        if(any([item[0] for item in self.progress])):
            if(all([item[1] == '' for item in self.progress])):
                self.console.print(
                    f'[bold green]:heavy_check_mark: Housekeeping routine completed successfully[/bold green]')
                exit(0)
            else:
                self.console.print(
                    f'[bold red]:cross_mark: Housekeeping routine completed, but some files could not be processed.[/bold red]'
                )
                exit(1)
