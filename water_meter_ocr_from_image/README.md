#My water meter

## Development
I based myself on https://afterhourscoding.wordpress.com/2023/01/21/making-your-own-home-assistant-add-on/

I replaced `ARG BUILD_FROM` with `ARG BUILD_FROM=homeassistant/amd64-base:latest` in Dockerfile. then just did docker build and run to test things locally.

Read https://developers.home-assistant.io/docs/add-ons/testing for more details

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
So the actual coommand for me is: `scp -r /home/chris/workspace/water_meter_ocr ha:/root/addons`

## Coding the actual addon
All credit goes to https://github.com/bvlaicu/home-assistant-addons/tree/master/meter-reader. I just changed the code to get the latest image from a remote location instead of a camera. This because I have a flash attached to my camera. I have one homeassistant automation which activates the falsh and saves a picture to my NAS. This addont hen retrieves the lates image and uses Amazon Rekogniion to extract the value
