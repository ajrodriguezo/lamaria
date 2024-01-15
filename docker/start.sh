#!/bin/bash
docker build -t freelance_jaca/lamarina:latest .

docker run -it \
    --rm \
    --net="host"\
    --name="lamaria"\
    -v $(pwd)/..:/lamaria \
    freelance_jaca/lamarina