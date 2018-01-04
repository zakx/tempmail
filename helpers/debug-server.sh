#!/bin/bash

echo "Starting debug server for the first time..."
while true; do
	python3 app.py 2>&1;
	echo "Debug server quit, waiting 5 seconds to restart";
  	sleep 5;
done

