# from datetime import datetime
import os.path
from datetime import datetime

from config import config
from dateutil.relativedelta import relativedelta
from log import log

from google_calendar.calendar_event import CalendarDayHelper, CalendarEvent

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
            day_plus_1 = day + relativedelta(days=1)
            tmin = day.isoformat("T")
            tmax = day_plus_1.isoformat("T")
            log("Getting the upcoming events", level="debug")

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

            cal_day_helper = CalendarDayHelper()
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                text = event["summary"]

                c = CalendarEvent(start, end, text)
                cal_day_helper.add_event(c)

            return cal_day_helper

        except HttpError as error:
            log("An error in GoogleCalendar occurred: %s" % error)

    def load_fake(self):
        log("loading fake calendar events", level="debug")

        today = datetime.now(config.TZ).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(config.TZ)
        tomorrow = datetime.now(config.TZ).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(config.TZ) + relativedelta(days=1)
        today = today.strftime("%Y-%m-%d")
        tomorrow = tomorrow.strftime("%Y-%m-%d")

        cal_day_helper = CalendarDayHelper()

        cal_day_helper.add_event(CalendarEvent(today, tomorrow, "All day some-event"))
        cal_day_helper.add_event(CalendarEvent(today, tomorrow, "Another delivery"))
        cal_day_helper.add_event(CalendarEvent(f"{today}T15:00:00+03:00", f"{today}T16:00:00+03:00", "Test calendar event commute 2:00, back 2"))
        cal_day_helper.add_event(CalendarEvent(f"{today}T19:00:00+03:00", f"{today}T21:00:00+03:00", "Formula-1, focus"))

        return cal_day_helper
