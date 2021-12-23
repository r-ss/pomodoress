"""
google-api-python-client = "^2.33.0"
google-auth-httplib2 = "^0.1.0"
google-auth-oauthlib = "^0.4.6"
python-dateutil = "^2.8.2"
"""


from __future__ import print_function

from datetime import datetime
import os.path
import dateutil.parser
from dateutil.relativedelta import relativedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class CalendarEvent:

    dtformat = '%m-%d-%Y %H:%M'

    def __init__(self, start, end, text) -> None:
        self.start = dateutil.parser.parse(start)
        self.end = dateutil.parser.parse(end)
        self.text = text

    @property
    def duration(self):
        return self.end - self.start

    @property
    def all_day(self):
        if self.duration.seconds == 0:
            return True
        return False

    @property
    def formatted_start(self):
        return self.start.strftime(self.dtformat)

    @property
    def formatted_end(self):
        return self.end.strftime(self.dtformat)

    @property
    def description(self) -> str:
        return f'{self.all_day} - {self.formatted_start} - {self.formatted_start} - {self.text}'


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8085)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        today = datetime.today()
        tomorrow = today + relativedelta(days=30)

        tmin = today.isoformat('T') + "Z"
        tmax = tomorrow.isoformat('T') + "Z"
        

        # one_day = round(time.time())+86400
        print('Getting the upcoming events')


        events_result = service.events().list(calendarId='primary', timeMin=tmin, timeMax=tmax, maxResults=100, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            text = event['summary']

            c = CalendarEvent(start, end, text)

            print(c.description)
            # print(event)

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()