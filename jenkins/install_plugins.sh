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

# Path to the jenkins-cli.jar file
CLI_JAR="jenkins-cli.jar"

# Check if jenkins-cli.jar exists
if [ ! -f "$CLI_JAR" ]; then
  echo "Downloading jenkins-cli.jar from $JENKINS_URL"
  curl -o "$CLI_JAR" "$JENKINS_URL/jnlpJars/jenkins-cli.jar"
fi

# Check if plugins.txt exists
if [ ! -f "plugins.txt" ]; then
  echo "plugins.txt file not found!"
  exit 1
fi

# Read plugins.txt into an array and install plugins
mapfile -t plugins < plugins.txt
for plugin in "${plugins[@]}"; do
  # Trim leading and trailing whitespace
  plugin=$(echo "$plugin" | xargs)
  if [ -z "$plugin" ]; then
    continue  # Skip empty lines
  fi
  echo "Installing plugin: $plugin"
  java -jar "$CLI_JAR" -s "$JENKINS_URL" -auth "$JENKINS_USER:$JENKINS_API_TOKEN" install-plugin "$plugin"
  # Check if installation was successful
  if [ $? -ne 0 ]; then
    echo "Error installing plugin: $plugin"
    exit 1
  fi
done

# Safe restart Jenkins to apply the plugins
echo "Restarting Jenkins to apply the plugins..."
java -jar "$CLI_JAR" -s "$JENKINS_URL" -auth "$JENKINS_USER:$JENKINS_API_TOKEN" safe-restart

echo "Plugins installation complete and Jenkins is restarting."