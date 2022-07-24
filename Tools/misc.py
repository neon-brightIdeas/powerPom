import time

from datetime import datetime


def get_epoch() -> str:
	today_epoch = datetime.timestamp(datetime.utcnow())
	return str(today_epoch)


def get_current_time():
	current = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	return current
