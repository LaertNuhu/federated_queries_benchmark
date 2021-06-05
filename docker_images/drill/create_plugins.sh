#!/bin/bash

for f in /configs/*; do
    curl -X POST -H "Content-Type: application/json" --data "@$f" http://localhost:8047/storage/myplugin.json
done