import argparse
import time

from win10toast import ToastNotifier

parser = argparse.ArgumentParser(description='passes params to appropriate os')
parser.add_argument("-m", '--message', type=str, help="'m' Variable is prompt message")

args = parser.parse_args()
p = args

# j_TODO : Need to make this more universal
def windows_toast(type_effort):
    # One-time initialization
    toaster = ToastNotifier()

    # Show notification whenever needed
    toaster.show_toast("Work Complete!\n", f'\n\nTime for {type_effort}!', threaded=True,
                    icon_path=None, duration=6)  # 3 seconds

    # To check if any notifications are active,
    # use `toaster.notification_active()`
    while toaster.notification_active():
        time.sleep(0.6)

windows_toast(p.message)
