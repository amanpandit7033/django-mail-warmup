import subprocess
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run server and warmup runner together"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Django server and Warmup engine...\n")

        # Start warmup runner
        warmup_process = subprocess.Popen(
            [sys.executable, "manage.py", "warmup_runner"]
        )

        try:
            # Start Django runserver
            subprocess.run([sys.executable, "manage.py", "runserver"])
        except KeyboardInterrupt:
            pass
        finally:
            self.stdout.write("\nStopping warmup engine...")
            warmup_process.terminate()
