# GoogleBooks2Notion
Python Script and VM setup to automatically run the script every minute to check for changes in your notiong database.

1. Edit ```Books-Public.py``` with your API keys and Notion database ID that you want to look for changes in.
2. Create your virtual machine and install python3.
3. Upload or copy ```Books-Public.py``` onto your VM, I created a "python" folder in /opt to store my scripts and pasted the code into a text file.
4. Edit crontab config from command line ```crontab -e```
5. add line after comments ```* * * * * python3 /opt/python/<script>.py``` change path and script name as needed.
## Crontab syntax for different frequencies:
### Run a script every minute
```* * * * * command```

### Run a script every hour at the top of the hour
```0 * * * * command```

### Run a script every day at midnight
```0 0 * * * command```

### Run a task every week at midnight on Sunday
```0 0 * * 0 command```

### Run a task every month at midnight on the first day of the month
```0 0 1 * * command```
