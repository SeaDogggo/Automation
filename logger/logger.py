from datetime import datetime


class Logger:

    def __init__(self, component_name):
        self.name = component_name

    def info(self, message):
        print('[{} - INFO] {}'.format(self.get_time(), message))

    def error(self, message):
        print('[{} - ERROR] {}'.format(self.get_time(), message))

    def get_time(self):
        today = datetime.today()
        return today.strftime('%H:%M:%S')
