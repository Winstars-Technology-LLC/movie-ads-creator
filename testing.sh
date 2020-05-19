#!/bin/bash
sudo apt-get install wget
sudo dpkg -l | grep wget
cd ..
mkdir -p data

cd movie-ads-creator || exit
mkdir -p test_data
cd test_data || exit

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1BLNSwCNosTgIUm6xYP8hZA6gKIBXQX2s' -O test_logo.png
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1AE9RIo11Zc-7C3k8lZ9PD42ydnUcsPOl' -O test_video.mp4

cd ..

sudo apt-get remove docker docker-engine docker.io containerd runc

sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

if [ -z "$(sudo docker images -q movie_creator:1.0)" ]
then
sudo docker build -t movie_creator:1.0 .
fi

#if [ -z "$(sudo docker ps -a |grep movie_creator:1.0)" ]
#then
#CONTAINER_ID=sudo docker ps -aqf "name=movie_creator:1.0"
#sudo docker container rm "$CONTAINER_ID"
#fi
#
sudo docker run -p 80:80 -it --name dock --mount type=bind,source="$(pwd)"/data,target=/app/output movie_creator:1.0

#docker-machine start
#docker-machine env
#eval "$(docker-machine env)"
#docker build -t movie_creator:1.0 .
#cd ..
#docker run -p 80:80 -it --name dock --mount type=bind,source="$(pwd)"/data,target=/app/output movie_creator:1.0
