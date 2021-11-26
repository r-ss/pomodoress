from typing import Union

def midnight_fix(time: Union[int, str]) -> int:
    ''' recieves time in String or Int. Converting to Int, simple fix midnight problem - 00:00 as 0 and terurns as int '''

    # Union[int, str] means argument can be either int or str

    if type(time) == str:
        time = int(time.replace(':', ''))

    # fixing time int to work propelty after midnight
    # 500 means 5:00, 2400 means 24:00
    if time < 500:
        time += 2400
    return time