import datetime
import pickle
import os.path
import tkinter as tk
from tkinter import simpledialog, Listbox, Toplevel, Button
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def fetch_google_calendar_events():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
    
    service = build('calendar', 'v3', credentials=creds)
    
    now = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat() + 'Z'
    # CalendarID can also be 'primary'
    events_result = service.events().list(calendarId='andreas.schmid.as3@roche.com', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])

def show_gui_to_select_event(events):
    def on_select_event(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        event = events[index]
        
        start = event['start'].get('dateTime', event['start'].get('date'))
        attendees = event.get('attendees', [])
        attendees_names = [attendee['email'] for attendee in attendees]
        attendees_str = ""
        for a in attendees_names:
            attendees_str = attendees_str + f"\n  - {a}"

        formatted_event = f"""
---
title: {event['summary']}
source: {event['htmlLink']}
tags:
  - meeting
date: {start}
people: {attendees_str}
---
"""
        print(formatted_event)
        root.destroy()

    root = tk.Tk()
    root.title('Select a Meeting')
    
    listbox = Listbox(root, width=100)
    listbox.pack(pady=15, padx=15)

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        listbox.insert(tk.END, f"{start} - {event['summary']}")

    listbox.bind('<<ListboxSelect>>', on_select_event)
    
    root.mainloop()

if __name__ == '__main__':
    events = fetch_google_calendar_events()
    if events:
        show_gui_to_select_event(events)
    else:
        print("No upcoming events found.")

