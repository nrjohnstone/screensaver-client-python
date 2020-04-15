import sys, pygame
import io
import urllib2
import requests
import json
from urllib2 import urlopen
from datetime import datetime
from datetime import timedelta
import yaml

config = yaml.load(open("./config.yml"))

photo_server = config['photoserver']['host']
port = config['photoserver']['port']
client_id = config['client']['id']
display_time = config['client']['display_time']
run_fullscreen = config['client']['fullscreen']

pygame.init()
pygame.mouse.set_visible(False)

if run_fullscreen:
    screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode([0,0])

screen_width = screen.get_width()
screen_heigh = screen.get_height()

last_update = datetime.now() - timedelta(minutes=10)

guid = client_id
response = requests.post("http://" + photo_server + ":" + str(port) + "/api/photoLists/" + guid)

response = requests.get("http://" + photo_server + ":" + str(port) + "/api/photoLists/" + guid)
photo_list_json = response.json()
total_images = photo_list_json['total']
image_index = 0

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
    
    delta = datetime.now() - last_update
    
    if delta.total_seconds() > display_time:
        
        image_url = "http://" + photo_server + ":" + str(port) + "/api/photoLists/"+ client_id + "/photos/" + str(image_index) + "/data"
        image_stream = None

        try:
            response = requests.get(image_url)

            image_data = io.BytesIO(response.content)
            
            image = pygame.image.load(image_data)
            
            wpercent = (screen_width/float(image.get_width()))
            hsize = int((float(image.get_height())*float(wpercent)))

            image = pygame.transform.smoothscale(image, (screen_width, hsize))

            image_rect = image.get_rect()
            screen.fill(0)
            screen.blit(image, image_rect)
            pygame.display.flip()
            last_update = datetime.now()
            image_index += 1
            if image_index >= total_images:
                image_index = 0                
        except Exception, e:
            print "Generic exception caught"
            last_update = datetime.now()

    pygame.time.wait(50)