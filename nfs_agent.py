#! /usr/bin/python3

import subprocess
import json
import requests
import socket
import time
from datetime import datetime

day_interval = 10
night_interval = 300
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
hostname = hostname.replace('.telviva.com', '')

telviva_42_mounts = ['/var/lib/enswitch', '/var/lib/enswitch_aws/recordings', '/var/lib/enswitch_omf/recordings']
telviva_35_mounts = ['/var/lib/enswitch', '/var/lib/enswitch_aws/recordings']

mounts = telviva_42_mounts
if '197.155.251' not in ip_address:
    mounts = telviva_35_mounts


while True:

    try:
        interval = night_interval
        now = datetime.now()
        hour = now.hour
        if hour >= 7 and hour < 18:
            interval = day_interval
        
        for mount in mounts:
            proc = subprocess.Popen(["nfs-iostat", "jsonstats", mount], stdout=subprocess.PIPE)
            output, error = proc.communicate()

            output = output.strip()
            output_str = output.decode('utf-8')
            jsonstats = json.loads(output_str)
            jsonstats['server'] = hostname

            resp = requests.post('https://nfsmon.telviva.com/nfs/api/save', json=jsonstats, headers={'Content-Type': 'application/json'})
        # Sleep    
        time.sleep(interval)
    except KeyboardInterrupt as e:
        break

