# from datetime import datetime
import os.path
from dateutil.relativedelta import relativedelta
from config import config

from google_calendar.calendar_event import CalendarEvent, CalendarDayHelper

from log import log

""" pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib """

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.


class GoogleCalendar:

    credentials_json_path = f"{config.BASE_DIR}/src/google_calendar/credentials.json"
    token_json_path = f"{config.BASE_DIR}/src/google_calendar/token.json"
    scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

    def __init__(self) -> None:
        self.creds = None
        self.auth()

    def auth(self):
        if os.path.exists(self.token_json_path):
            self.creds = Credentials.from_authorized_user_file(self.token_json_path, self.scopes)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_json_path, self.scopes)
                self.creds = flow.run_local_server(port=8085)
        # Save the credentials for the next run
        with open(self.token_json_path, "w") as token:
            token.write(self.creds.to_json())

    def load_for_day(self, day):
        try:
            service = build("calendar", "v3", credentials=self.creds)

            # Call the Calendar API
            # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

            # today = datetime.today()
            day_plus_1 = day + relativedelta(days=1)

            # tmin = day.isoformat('T') + "Z"
            # tmax = day_plus_1.isoformat('T') + "Z"
            tmin = day.isoformat("T")
            tmax = day_plus_1.isoformat("T")

            # print('day', day)

            # print('tmin', tmin)
            # print('tmax', tmax)

            # tmin = day.isoformat()+ "Z"
            # tmax = day_plus_1.isoformat()+ "Z"

            # one_day = round(time.time())+86400
            log("Getting the upcoming events")

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=tmin,
                    timeMax=tmax,
                    maxResults=100,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                log("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events

            cal_day_helper = CalendarDayHelper()
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                text = event["summary"]

                c = CalendarEvent(start, end, text)
                cal_day_helper.add_event(c)

                # log(c.description)
                # log(event)

            return cal_day_helper

        except HttpError as error:
            log("An error in GoogleCalendar occurred: %s" % error)

    def load_fake(self):

        cal_day_helper = CalendarDayHelper()

        cal_day_helper.add_event(CalendarEvent("2021-12-24", "2021-12-25", "All day some-event"))
        cal_day_helper.add_event(CalendarEvent("2021-12-24", "2021-12-25", "Another delivery"))
        cal_day_helper.add_event(
            CalendarEvent(
                "2021-12-24T15:00:00+03:00",
                "2021-12-24T16:00:00+03:00",
                "Тестовое календарное событие commute 2:00, back 2",
            )
        )
        cal_day_helper.add_event(CalendarEvent("2021-12-24T19:00:00+03:00", "2021-12-24T22:00:00+03:00", "Formula-1"))

        return cal_day_helper
