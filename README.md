# powerPom
cli based pomodoro

This is a CLI based Pomodoro timer that allows you time time your projects with default pomodoro time, 25 minutes of work and 8 minutes of rest. This can be altered per project to something custom as well. In the future there might be an optional GUI. All time is stored in a Database file, future releases will allow exporting to PDF or Excel or just showing stats even in a non GUI environment.


### Install
`python setup.py`
Debian based Linux boxes might have to install an additional package.

### Compatibility
Windows 10, not tested on 11 yet
Linux

### Pre-requirements
Python 3.6+ at minimum.

### Commands
| -h | Help Menu                                                                     |
|----|-------------------------------------------------------------------------------|
| -t | Must be used with (-r), specify custom length of work time                    |
| -r | Must be used with (-t), specify custom length of break time                   |
| -p | (optional - default is, "General") Sets the project the session is for        |
| -c | (optional) Specify the comment on what you are working on during work session |

### Examples
Run Generic : `python main.py`

Run time under specific project :
`python main.py -p "some project" -c "some optional Comment"

Run with specific Time, Rest is required:
`python main.py -p "test" -c "showing with specific time" -t 2 -r 1
