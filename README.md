# pomodoress

Personal utility to send me timed messages with expected productive activity according to current time.  
Based on pomodoro technique. Schedule example:

    🧑🏻‍💻 13:00 - code until 14:00
    🌿 13:25 - 5 minutes rest
    🧑🏻‍💻 13:30 - code...
    🥑 13:55 - eat some fruit! next: guitar
    🎸 14:00 - guitar
    ✨ 14:25 - rest! next: sport
    🎾 14:30 - sport
    💪 14:55 - make some exercises! next: netflix
    📺 15:00 - netflix until 16:00

### Realization

Implemented as stateless function on AWS Lambda with Chalice framework.

Every minute timed event is fired by AWS EventBridge. App look up a relevant Pomodoro for current time then sends a notification in form of a telegram message for pomodoro start, end, rest time etc.