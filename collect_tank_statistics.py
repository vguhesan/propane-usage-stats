#!/usr/bin/env python3

####################################################################
# This script makes an HTTP request to the Otodata server and
# extracts the current statistics from your tank.
# How to invoke this script:
#     pipenv run ./collect_tank_statistics.py "userid" "password"
####################################################################

import requests
import datetime
import json
import sys
import base64
from datetime import datetime
from tzlocal import get_localzone  
import rfc3339

# See full list of timezones:
# https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
timezone = "US/Eastern"


def call_client(auth_key):
    session = requests.Session()

    # print("Acquiring data from Otodata server...")
    r = session.get(
        "https://telematics.otodatanetwork.com:4432/v1.5/DataService.svc/GetAllDisplayPropaneDevices",
        headers={
            "Accept": "*/*",
            "Accept-Language": "en-US;q=1, fa-US;q=0.9",
            "User-Agent": "Nee-Vo/2.6.4 (iPhone; iOS 16.0.2; Scale/3.00)",
            "Host": "telematics.otodatanetwork.com:4432",
            "Authorization": auth_key,
        },
    )
    j = json.loads(r.text)
    # The TankCapacity is sometimes coming back as zero
    # (so hard-coding it here to 1000 Gallon tank capacity)
    # process_data(j[0]["TankCapacity"], j[0]["Level"])
    process_data(1000, j[0]["Level"])


def process_data(tank_capacity, current_level):
    try:
        gallonsRemaining = (current_level / 100) * tank_capacity
        percentRemaining = current_level
    except Exception as e:
        if hasattr(e, "message"):
            print(e.message)
        else:
            print(e)
        exit(1)

    # timestamp = get_date_time_by_zone(timezone)
    now = datetime.now(get_localzone())
    timestamp = get_date_string(now)
    # timestamp,gallonsRemaining, percentRemaining
    print(f"{timestamp},{int(gallonsRemaining)},{int(percentRemaining)}")


def get_date_string(date_object):
    return rfc3339.rfc3339(date_object)


def base64_encode(userid, password):
    encode_string = userid + ":" + password
    encode_string_bytes = encode_string.encode("ascii")
    encoded_bytes = base64.b64encode(encode_string_bytes)
    encoded_string = encoded_bytes.decode("ascii")
    return encoded_string


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            'Run me like this: pipenv run ./collect_tank_statistics.py "userid" "password"'
        )
        exit(0)
    else:
        userid = sys.argv[1]
        password = sys.argv[2]
        if (userid == None or password == None) or (userid == 'USERID' or password == 'PASSWORD'):
            print("You must provide a valid userid and password")
            exit(0)
        else:
            # print(f"UserId: {userid}, Password: {password}")
            auth_key = "Basic " + base64_encode(userid, password)
            # print(f"Auth key: {auth_key}")
            call_client(auth_key)
            exit(0)
