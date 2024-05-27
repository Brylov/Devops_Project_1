#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Check if required environment variables are set
if [ -z "$JENKINS_URL" ] || [ -z "$JENKINS_USER" ] || [ -z "$JENKINS_API_TOKEN" ]; then
  echo "One or more required environment variables (JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN) are missing in the .env file."
  exit 1
fi

# Get the list of installed plugins and save it to plugins.txt
java -jar jenkins-cli.jar -s $JENKINS_URL -auth $JENKINS_USER:$JENKINS_API_TOKEN list-plugins > plugins.txt

#!/bin/bash

# Check if original plugins.txt exists
if [ ! -f "plugins.txt" ]; then
  echo "plugins.txt file not found!"
  exit 1
fi

# Create or overwrite the new plugins.txt
> new_plugins.txt

# Read the original plugins.txt and extract the plugin names
while IFS= read -r line; do
  plugin=$(echo $line | awk '{print $1}')
  echo $plugin >> new_plugins.txt
done < plugins.txt

rm -f plugins.txt
mv new_plugins.txt plugins.txt

echo "New plugins.txt with plugin names created successfully."