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


def exit_gracefully(self, signum, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    self.shutdown = True


host = '192.168.1.10'

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
    screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
else:
    resolution = [1280, 720]
    screen = pygame.display.set_mode(resolution)

screen_width = screen.get_width()
screen_height = screen.get_height()

log.info("screen_width: " + str(screen_width))
log.info("screen_height: " + str(screen_height))

photo_list_id = client_id

photo_list_initialized = False
total_images = 0
image_index = 0

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

    if not photo_list_initialized:
        log.info("Screensaver initialize first image")

    while not photo_list_initialized:
        try:
            response = photoRepository.get_photolist(photo_list_id)

            if response.status_code == 200:
                total_images = response.total
                image_index = response.current_index
                photo_list_initialized = True
                continue
            elif response.status_code == 404:
                response = photoRepository.create_photolist(photo_list_id)
                if response.status_code == 200:
                    continue
            else:
                pygame.time.wait(2000)
        except requests.exceptions.ConnectionError as ex:
            log.exception("Unable to initialize")
            pygame.time.wait(2000)

    delta = datetime.now() - last_update
    
    if delta.total_seconds() > display_time:

        image_stream = None

        try:
            if image_data is None:
                response = photoRepository.get_photo(photo_list_id, image_index)
                if response.status_code == 404:
                    response = photoRepository.get_photolist(photo_list_id)
                    if response.status_code == 404:
                        photo_list_initialized = False
                        continue

                image_data = response.image_data

            image = pygame.image.load(image_data)

            image_height = image.get_height()
            image_width = image.get_width()
            image_ratio = float(image_width) / float(image_height)

            width_ratio = (screen_width / float(image_width))
            height_ratio = (screen_height / float(image_height))

            if width_ratio > height_ratio:
                image_height = screen_height
                image_width = int((float(screen_height)) * float(image_ratio))
            else:
                image_height = int((float(screen_width)) / float(image_ratio))
                image_width = screen_width

            image = pygame.transform.smoothscale(image, (image_width, image_height))

            image_center_x = screen_width / 2
            image_center_y = screen_height / 2

            image_rect = image.get_rect()
            image_rect.center = [image_center_x, image_center_y]

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
            response = photoRepository.get_photo(photo_list_id, image_index)
            if response.status_code == 200:
                image_data = response.image_data
            elif response.status_code == 404:
                response = photoRepository.create_photolist(photo_list_id)
                if response.status_code == 404:
                    photo_list_initialized = False
                else:
                    log.error("Unable to create photolist. Retry in 10 seconds")
                    pygame.time.wait(10000)
        except Exception, e:
            log.exception("Exception while recording current index in main loop")
            last_update = datetime.now()
            pygame.time.wait(10000)

    pygame.time.wait(50)

pygame.display.quit()
pygame.quit()
sys.exit(0)
