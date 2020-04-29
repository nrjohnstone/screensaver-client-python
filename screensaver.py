import sys
import pygame
import io
import urllib2
import requests
import json
from urllib2 import urlopen
from datetime import datetime
from datetime import timedelta
import yaml
import os.path
import signal
import logging
import os
from PhotoRepository import PhotoRepository
#import logstash


def exit_gracefully(self, signum, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    self.shutdown = True

host = '192.168.1.10'

#test_logger = logging.getLogger('python-logstash-logger')
#test_logger.setLevel(logging.INFO)
#test_logger.addHandler(logstash.TCPLogstashHandler(host, 19501, version=1))

#test_logger.error('python-logstash: test logstash error message.')

log_path = "/var/log/screensaver/logfile.log"

if os.name == 'nt':
    log_path = "logfile.log"

log = logging.getLogger("my-logger")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(log_path)
fh.setFormatter(formatter)

log.addHandler(fh)

log.info("Screensaver starting")

shutdown = False
file_exists = os.path.isfile("/etc/screensaver/config.yml")

if file_exists:
    config = yaml.load(open("/etc/screensaver/config.yml"))
else:
    config = yaml.load(open("config.yml"))

photo_server = config['photoserver']['host']
port = config['photoserver']['port']
client_id = config['client']['id']
display_time = config['client']['display_time']
run_fullscreen = config['client']['fullscreen']

photoRepository = PhotoRepository(photo_server, port)

pygame.init()
pygame.mouse.set_visible(False)

signal.signal(signal.SIGTERM, exit_gracefully)

if run_fullscreen:
    screen = pygame.display.set_mode([1920, 1280], pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode([0, 0])

screen_width = screen.get_width()
screen_height = screen.get_height()

photo_list_id = client_id
photo_server_base_url = "http://" + photo_server + ":" + str(port) + "/api"

initialized = False
total_images = 0
image_index = 0

log.info("Screensaver initialize first image")
while not initialized:
    try:
        response = photoRepository.getPhotoList(photo_list_id)

        if response.status_code == 404:
            response = photoRepository.createPhotoList(photo_list_id)
            if response.status_code == 200:
                continue
        elif response.status_code == 200:
            total_images = response.total
            image_index = response.current_index
            initialized = True
            continue
        else:
            pygame.time.wait(2000)
    except requests.exceptions.ConnectionError as ex:
        log.exception("Unable to initialize")
        pygame.time.wait(2000)

last_update = datetime.now() - timedelta(minutes=10)

image_data = None

log.info("Screensaver enter mainloop")
while not shutdown:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
    
    delta = datetime.now() - last_update
    
    if delta.total_seconds() > display_time:

        image_stream = None

        try:
            if image_data is None:
                response = photoRepository.getPhoto(photo_list_id, image_index)
                image_data = response.image_data
            
            image = pygame.image.load(image_data)
            
            wpercent = (screen_width/float(image.get_width()))
            hsize = int((float(image.get_height())*float(wpercent)))

            image = pygame.transform.smoothscale(image, (screen_width, hsize))

            image_rect = image.get_rect()
            screen.fill(0)
            screen.blit(image, image_rect)
            pygame.display.flip()
        except Exception, e:
            log.exception("Exception while loading image in main loop - image_index: " + str(image_index))
            last_update = datetime.now()
            pygame.time.wait(1000)

        try:
            last_update = datetime.now()
            image_index += 1
            if image_index >= total_images:
                image_index = 0

            photoRepository.update_current_index(photo_list_id, image_index)

            # Preload the next photo
            response = photoRepository.getPhoto(photo_list_id, image_index)
            image_data = response.image_data
        except Exception, e:
            log.exception("Exception while recording current index in main loop")
            last_update = datetime.now()
            pygame.time.wait(1000)

    pygame.time.wait(50)

pygame.display.quit()
pygame.quit()
sys.exit(0)
