from collections import deque
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text

from .pdf import *

def create_layout():
    """Defines the UI layout: Progress on top, Logs on bottom."""
    layout = Layout()
    layout.split_column(
        Layout(name="progress", size=3),
        Layout(name="grid", size=6),
        Layout(name="logs")
    )
    return layout

class Printer():
    def __init__(self, prompts):
        self.console = Console()
        self.log_queue = deque(maxlen=15) 
        self.prompts_count = len(prompts)
        self.results = [None] * self.prompts_count
        self.current_idx = 0
        self.job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TextColumn("{task.completed}/{task.total}"),
        )
        self.task_id = self.job_progress.add_task("[cyan]Scanning Code...", total=len(prompts))
        self.layout = create_layout()
        self.layout["progress"].update(Panel(self.job_progress, border_style="blue", title="Security Audit"))
        self.live = Live(self.layout, refresh_per_second=10)
        self.live.start()

    def update_grid_panel(self):
        grid_text = Text()
        for result in self.results:
            if result is True:
                grid_text.append("■ ", style="bold green")
            elif result is False:
                grid_text.append("■ ", style="bold red")
            else:
                grid_text.append("■ ", style="dim white")
        self.layout["grid"].update(Panel(grid_text, title="Instance Status Map", border_style="white"))

    def print_correct(self, message):
        self.log_queue.append(f"[bold green]✅ {message}")
        if self.current_idx < self.prompts_count:
            self.results[self.current_idx] = True

    def print_warning(self, message):
        self.log_queue.append(f"[bold yellow]✅ {message}")

    def print(self, message):
        self.log_queue.append(f"{message}")

    def clear(self):
        self.log_queue.clear()

    def print_incorrect(self, message):
        self.log_queue.append(f"[bold red]❌ {message}")
        if self.current_idx < self.prompts_count:
            self.results[self.current_idx] = False

    def end_iter(self):
        self.log_table = Table.grid(expand=True)
        for log in self.log_queue:
            self.log_table.add_row(log)
        self.layout["logs"].update(Panel(self.log_table, title="Audit Logs", border_style="white"))
        self.update_grid_panel()
        self.job_progress.update(self.task_id, advance=1)
        self.current_idx += 1

    def close(self):
        self.console.print("[bold green]Scan Complete![/]")
        self.live.stop()

