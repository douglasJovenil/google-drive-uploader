# Google Drive Uploader
This is a Discord bot and it's purporse is watch for some channel searching for Twitch links of clips and then download, convert it to mp4 and finally upload the video to Google Drive.

- https://discord.com/api/oauth2/authorize?client_id=1050006525055352903&permissions=1040&scope=bot

```bash
flyctl auth login
flyctl launch
flyctl deploy
flyctl secrets set APP_AKEYLESS_CLIENT_ID=CLIENT-ID APP_AKEYLESS_ACCESS_KEY=ACCESS-KEY
flyctl vm stop VM_ID
```