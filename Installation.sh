#!/bin/bash  
 
# Bash script for installing most required packages for AldaCourse.
sudo apt-get clean
sudo apt-get update
sudo python3 -m pip install Django
sudo python3 -m pip install selenium
sudo python3 -m pip install numpy

sudo python3 -m pip install -U googlemaps 
sudo python3 -m pip install --upgrade gensim
sudo python3 -m pip install -U nltk
