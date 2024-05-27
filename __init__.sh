#!/bin/bash

# Change directory to jenkins
cd jenkins

# Define the name of the Docker network
network_name="jenkins_nw"

jenkins_container_name="jenkins-app-1"

# Check if the Docker network exists
if ! docker network inspect "$network_name" &>/dev/null; then
    # Create the Docker network
    docker network create "$network_name"
fi
# Start Jenkins environment with Docker Compose
docker compose up --build -d

# Define the path to the initialAdminPassword file inside the container
password_file="/var/jenkins_home/secrets/initialAdminPassword"

# Define the maximum wait time in seconds (2 minutes)
max_wait_time=120

# Initialize a counter to track elapsed time
elapsed_time=0

# Loop until the file exists or the maximum wait time is reached
while [ "$elapsed_time" -lt "$max_wait_time" ]; do
    # Check if the file exists in the container
    docker exec $jenkins_container_name test -e "$password_file" && break
    
    sleep 1  # Wait for 1 second
    elapsed_time=$((elapsed_time + 1))  # Increment elapsed time counter
done

# Check if the file exists
if [ "$elapsed_time" -lt "$max_wait_time" ]; then
    # Extract the content of the initialAdminPassword file from the container
    password=$(docker exec $jenkins_container_name cat "$password_file")
    
    # Check if the password is not empty
    if [ -n "$password" ]; then
        echo "The Password for Jenkins is: $password"
        echo "The Jenkins URL is: http://localhost:8080"
    else
        echo "Error: The initialAdminPassword file is empty." >&2
        exit 1
    fi
else
    # Print an error message and exit with a non-zero status code
    echo "Error: The initialAdminPassword file was not found after waiting for $max_wait_time seconds." >&2
    exit 1
fi

wget http://localhost:8080/jnlpJars/jenkins-cli.jar