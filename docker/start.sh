#!/bin/bash
docker build -t camilop121/lamarina:latest .

docker run -it \
    --rm \
    --net="host"\
    --name="lamaria"\
    -v $(pwd)/..:/lamaria \
    camilop121/lamarina