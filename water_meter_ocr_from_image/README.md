# My water meter OCR from an image

## Development

I based myself on https://afterhourscoding.wordpress.com/2023/01/21/making-your-own-home-assistant-add-on and https://developers.home-assistant.io/docs/add-ons/testing for more details.

For local development I mount an options.json config into the docker to imitiate the actual home assistant environment. This options.json is located in a testdata folder which I mount as /data in the docker. As soon as I need to test mqtt stuff I need to install the addon into my home assistant setup. cf next point for that

```json
{
    "upd_interval": 1800,
    "user": null,
    "password": null,
    "baseline": 1,
    "under": 1,
    "over": 1,
    "aws_access_key_id": null,
    "aws_secret_access_key": null,
    "region": null,
    "mqtt_host": "127.0.0.1",
    "mqtt_port": 1883,
    "mqtt_user": "mqtt",
    "mqtt_pwd": "mqtt_pwd",
    "mqtt_topic": "home/meter"
}
```

Use the `test.sh` script to build and run locally.


## Install locally

Copy via ssh to ha. I have the ssh addon installed and configured. for me the comand is `ssh -p 23 root@192.168.178.53` for ssh with a ecdsa key. 
I have ssh configured:
```
Host ha
  HostName 192.168.178.53
  Port 23
  User root
  IdentityFile /home/chris/.ssh/id_ecdsa
```
So the actual coommand for me is: `scp -r /home/chris/workspace/home-assistant-addons/water_meter_ocr_from_image/ ha:/root/addons`

## Coding the actual addon

All credit goes to https://github.com/bvlaicu/home-assistant-addons/tree/master/meter-reader. I just changed the code to get the latest image from a remote location instead of a camera. This because I have a flash attached to my camera. I have one homeassistant automation which activates the falsh and saves a picture to my NAS. This addont hen retrieves the lates image and uses Amazon Rekogniion to extract the value.
