#!/bin/bash

sudo docker container start dock
sudo docker logs -f dock > data/log_file.log