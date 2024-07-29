#!/bin/sh
# env.sh
# Copyright 2024, Athena Decision Systems
# @author Joel Milgram
# @description This script is called when Nginx starts. It replicates or injects REACT_APP env variables into the React Application via the file env-config.js

# Recreate config file
rm -rf ./env-config.js
touch ./env-config.js

# Add assignment 
echo "window._env_ = {" >> ./env-config.js

# Loop through REACT_APP environment variables
printenv | grep ^REACT_APP | awk -F'=' '{
  if ($2 ~ /^".*"$|^\x27.*\x27$/) {
    print $1 " : " $2 ","
  } else {
    print $1 " : \"" $2 "\","
  }
}' >> ./env-config.js

# Close the object
echo "}" >> ./env-config.js


