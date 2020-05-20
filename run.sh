#!/bin/bash

sudo docker container start dock
sudo sh -c 'docker logs -f dock > data/log_file.log'