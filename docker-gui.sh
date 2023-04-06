#!/bin/bash

docker create -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY -e TZ $*
