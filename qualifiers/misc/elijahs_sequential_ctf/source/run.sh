#!/bin/bash
docker build -t ljudgecontainer .
docker run --privileged -p 5000:5000 -t ljudgecontainer