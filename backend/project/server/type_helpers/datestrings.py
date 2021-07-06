from datetime import datetime
from project.server import app

class DateStringFormat():
    @staticmethod
    def remove_time_part(date_str):
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").strftime(
            app.config['DATE_FMT']
        )
