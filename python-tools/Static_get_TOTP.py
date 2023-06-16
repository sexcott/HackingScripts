#!/usr/bin/python3


import ntplib
import pyotp
import time


client = ntplib.NTPClient()
response = client.request('10.10.10.246')

totp = "orxxi4c7orxwwzlo"

totp = pyotp.TOTP(totp)

opt = totp.at(response.tx_time)
print(opt)

