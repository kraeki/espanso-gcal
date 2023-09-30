
## Install

### Clone this repo
```
git clone https://github.com/kraeki/espanso-gcal.git
```
### Get Google Calendar API key Create credentials.json file
1. Enable Google Calendar API
2. Create oauth credentials
3. Download and store `credentials.json` (e.g. https://console.cloud.google.com/apis/credentials?referrer=search&project=calendar-cli-399317)

### Install Dependencies
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```


### Test
```
./fetch_meeting.sh
```

### Espanso - Setup
```
matches:
  - trigger: ":meet"
    replace: "{{gcal_meetings}}"
    vars:
      - name: gcal_meetings
        type: shell
        params:
          cmd: "~/work/espanso-gcal/fetch_meeting.sh"
```


### i3 config: Open in float mode
```
# espanso + gcal fetcher ()
for_window [title="Select a Meeting"] floating enable
```
