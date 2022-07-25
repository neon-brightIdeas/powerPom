# powerPom
cli based pomodoro

This is a CLI based Pomodoro timer that allows you to time your projects with default pomodoro time, 25 minutes of work and 8 minutes of rest. This can be altered per project to something custom as well. In the future there might be an optional GUI. All time is stored in a Database file and can tell you the current stats of the day. In the future, releases will allow exporting to PDF or Excel, plus getting the weeks worth.


### Install
`python setup.py`
Debian based Linux boxes might have to install an additional package.

### Compatibility
Windows 10 & 11<br />
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
| --stats "today" or "week" or "yyyy-mm-dd,yyyy-mm-dd"| Get the current worked time and rest time, you can also use this with `-p` to specify showing just a specific project.
| 

### Examples
Run Generic : `python main.py`

Run time under specific project : <br />
`python main.py -p "some project" -c "some optional Comment"`

Run with specific Time, Rest is required: <br />
`python main.py -p "test" -c "showing with specific time" -t 2 -r 1`

Get Todays Stats: <br />
`python main.py --stats "today"`

Get Todays Stats for specific Project: <br />
`python main.py --stats "today" -p "project0"`

Get Week Stats based on Last Sunday for all Projects: <br />
`python main.py --stats "week"`
