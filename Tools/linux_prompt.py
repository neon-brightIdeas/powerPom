import argparse

from pynotifier import Notification

parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("-m", '--message', type=str, help="'m' Variable is prompt message")

args = parser.parse_args()
p = args

def send_notification(type_effort):
    Notification(
	title=f' Session',
	description=f'{type_effort} has ended',
	#icon_path='/absolute/path/to/image/icon.png', # On Windows .ico is required, on Linux - .png
	duration=6,                                   # Duration in seconds
	urgency='normal'
).send()

send_notification(p.message)
