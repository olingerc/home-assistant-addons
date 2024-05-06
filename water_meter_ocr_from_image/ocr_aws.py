import boto3
import paho.mqtt.client as mqtt
import requests
import json
import time
import os
import re
import sys

config_json = json.loads(open("/data/options.json").read())

if __name__ == '__main__':
    baseline = int(config_json["baseline"])
    base_low = baseline - int(config_json["under"])
    base_up = baseline + int(config_json["over"])
    while True:
        print("Start")
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
