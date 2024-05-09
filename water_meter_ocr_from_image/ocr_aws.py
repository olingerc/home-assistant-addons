import boto3
import paho.mqtt.client as mqtt
import requests
import json
import time
import os
import re
import sys
from PIL import Image
from smb.SMBConnection import SMBConnection

config_json = json.loads(open("/data/options.json").read())
path = "/root/.aws"
reading_path = "/data/meter.jpg"

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

f = open("/root/.aws/credentials", "w")
f.write("[default]")
f.write("\n")
f.write("aws_access_key_id = " + config_json["aws_access_key_id"])
f.write("\n")
f.write("aws_secret_access_key = " + config_json["aws_secret_access_key"])
f.close()
f = open("/root/.aws/config", "w")
f.write("[default]")
f.write("\n")
f.write("region = " + config_json["region"])
f.close()

baseline = int(config_json["baseline"])
base_low = baseline - int(config_json["under"])
base_up = baseline + int(config_json["over"])

client = boto3.client('rekognition')

def download_latest():
    conn = SMBConnection(config_json["user"], config_json["password"], 'ds', 'ds')
    conn.connect('192.168.178.111')
    results = conn.listPath('hass_share', 'water_meter/latest')
    latest = None

    for x in results:
        if x.filename.endswith(".jpg"):
            latest = x.filename
            break
    
    if latest:
        with open(reading_path, 'wb+') as fp:
            res = conn.retrieveFile('hass_share', 'water_meter/latest/' + latest, fp)
            print("File downloaded") 
            
            im = Image.open(reading_path)
            # Setting the points for cropped image
            left = 320
            top = 240
            right = 570
            bottom = 300
            im1 = im.crop((left, top, right, bottom))
            im1 = im1.save(reading_path)
    
    return latest


def reader(file):
    with open(file, "rb") as image_file:
        encoded_string = image_file.read()
        return encoded_string


def processor(base_low, baseline, base_up):
    data_str = reader(reading_path)
    response = client.detect_text(Image={'Bytes': data_str})
    print(response)
    print("")
    found = (response['TextDetections'])
    reading = ""
    for item in found:
        print("DetectedText:", item['DetectedText'])
        print("Type:", item['Type'])
        print("Confidence", item['Confidence'])
        print("Id", item['Id'])
        if item['Type'] != 'LINE':
            print("ParentId:", item['ParentId'])
        if (item['Type'] == 'WORD') or (item['Type'] == 'LINE'):
            print("value conversion")
            temp = item['DetectedText']
            print("x", temp, "x")
            temp = re.sub("[^0-9]", "", temp)
            print("x", temp, "x")
            nw = 0
            try:
                nw = int(temp)
            except Exception:
                print("Conversion to int failed")
                pass
            print("Converted int: ", nw, base_low, base_up)
            if (nw >= base_low and nw <= base_up):
                print("Value found in range:")
                reading = temp
                print(temp)
                print(base_low, nw, base_up)
        print("-----------")
    print("Returning reading: ", reading)
    return reading


def publishMQTT(reading):
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "meter_reader")
    mqttc.username_pw_set(username=config_json["mqtt_user"], password=config_json["mqtt_pwd"])
    mqttc.connect(config_json["mqtt_host"], int(config_json["mqtt_port"]))
    mqttc.publish(config_json["mqtt_topic"], reading, retain=True)
    mqttc.disconnect()


def publishhiloMQTT(low, high):
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "meter_reader")
    mqttc.username_pw_set(username=config_json["mqtt_user"], password=config_json["mqtt_pwd"])
    mqttc.connect(config_json["mqtt_host"], int(config_json["mqtt_port"]))
    mqttc.publish("home/band/low", str(low), retain=True)
    mqttc.publish("home/band/high", str(high), retain=True)
    mqttc.disconnect()


if __name__ == '__main__':
    baseline = int(config_json["baseline"])
    base_low = baseline - int(config_json["under"])
    base_up = baseline + int(config_json["over"])
    
    _lates_picture_filename = None

    print("Start")
    while True:
        latest = download_latest()
        if latest == _lates_picture_filename:
            pass
        else:
            _lates_picture_filename = latest
        try:
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
        except Exception:
            print("Unexpected error:", sys.exc_info())
            print("OCR failed. Will try again later.")
        time.sleep(int(config_json["upd_interval"]))
