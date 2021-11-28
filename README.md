# pomodoros

# TODO - mention chalice

Personal utility to send me timed messages with expected productive activity based on pomodoro technique

Every minute Dispatcher.tick() is fired and look up a relevant Pomodoro for current time, then sends a relevant notifications for pomodoro start, end, rest time etc.