#!/bin/bash

docker create -v /etc/timezone:/etc/timezone:ro -v /etc/localtime:/etc/localtime:ro -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY $*
