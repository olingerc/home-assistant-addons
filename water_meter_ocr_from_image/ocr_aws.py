import boto3
import paho.mqtt.client as mqtt
import requests
import json
import time
import os
import re
import sys
from smb.SMBConnection import SMBConnection

config_json = json.loads(open("/data/options.json").read())

def list_latest():
    conn = SMBConnection(config_json["user"], config_json["password"], 'ds', 'ds')
    conn.connect('192.168.178.111')
    results = conn.listPath('hass_share', 'water_meter/latest')
    latest = None

    for x in results:
        if x.filename.endswith(".jpg"):
            latest = x.filename
            break
    
    return latest

if __name__ == '__main__':
    baseline = int(config_json["baseline"])
    base_low = baseline - int(config_json["under"])
    base_up = baseline + int(config_json["over"])
    
    _lates_picture_filename = None

    while True:
        print("Start")
        latest = list_latest()
        print(latest)
        try:
            """
            takereading()
            print("foto action finished")
            reading = processor(base_low, baseline, base_up)
            if reading != "":
                print("Reading = ok = ", reading)
                baseline = int(reading)
                base_low = baseline - int(config_json["under"])
                base_up = baseline + int(config_json["over"])
                publishMQTT(reading)
                publishhiloMQTT(base_low, base_up)
            else:
                base_low = base_low - int(config_json["under"])
                base_up = base_up + int(config_json["over"])
                publishhiloMQTT(base_low, base_up)
            """
            pass
        except Exception:
            print("Unexpected error:", sys.exc_info())
            print("OCR failed. Will try again later.")
        time.sleep(int(config_json["upd_interval"]))
