import subprocess
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

last_run = None


class HourlyTaskMiddleware(MiddlewareMixin):
    def process_request(self, request):
        global last_run
        now = timezone.now()

        if last_run is None or now.hour != last_run.hour:
            subprocess.run(["python", "manage.py", "calculate_average"])
            last_run = now
