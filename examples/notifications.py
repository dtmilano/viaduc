import os
import json
import subprocess


def notify(title, text):
    print(['osascript', '-e', f'display notification {json.dumps(text)} with title {json.dumps(title)}'])
    #print(subprocess.run(['echo', 'osascript', '-e', f'display notification {json.dumps(text)} with title {json.dumps(title)}'], capture_output=True).stdout.decode('utf-8'))
    subprocess.run(['osascript', '-e', f'display notification {json.dumps(text)} with title {json.dumps(title)}'])


notify("Title with spaces", 'Heres an alert with a dangling ')
# notify("Title with spaces", "Here's an alert with a dangling")
