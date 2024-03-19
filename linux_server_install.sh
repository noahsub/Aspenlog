#!/bin/bash

# Ensure script is not run as sudo
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

# Update and install necessary packages
sudo apt-get update > /dev/null
sudo apt-get install -y ca-certificates curl software-properties-common xorg openbox snapd python3.11 python3-pip > /dev/null

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings > /dev/null
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc > /dev/null

# Add the Docker repository to Apt sources
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update > /dev/null

# Install Docker and its plugins
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin > /dev/null

# Stop and remove any existing Docker container
sudo docker stop aspenlog2020-database || true
sudo docker rm aspenlog2020-database || true

# Pull the latest Docker image for Postgres
sudo docker pull postgres:11.22-bullseye > /dev/null

# Prompt for database password and port
read -p "Please enter the password you would like to use for the database: " POSTGRES_PASSWORD
read -p "Please enter the port you would like to use for the database: " POSTGRES_PORT

# Kill any process using the selected port
pid=$(sudo lsof -t -i:$POSTGRES_PORT)
if [ -n "$pid" ]; then
    sudo kill -9 $pid > /dev/null
    echo "Killed process $pid on port $POSTGRES_PORT"
else
    echo "No process using port $POSTGRES_PORT was found"
fi

# Run the Docker container
sudo docker run --name aspenlog2020-database -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -p $POSTGRES_PORT:5432 -d postgres:11.22-bullseye > /dev/null

# Set maximum number of attempts to prevent infinite loop
max_attempts=30
count=0

# Wait for the Postgres service to start accepting connections
echo "Waiting for the PostgreSQL to start..."
until sudo docker exec -it aspenlog2020-database pg_isready -U postgres -h localhost > /dev/null 2>&1 || [ $count -eq $max_attempts ]; do
    sleep 1
    count=$((count+1))
done

# Create the database if the service started, otherwise print an error message
if [ $count -lt $max_attempts ]; then
    echo "PostgreSQL started successfully, creating NBCC-2020 database..."
    sudo docker exec -it aspenlog2020-database psql -U postgres -c "CREATE DATABASE \"NBCC-2020\";" > /dev/null
else
    echo "PostgreSQL did not start within the expected time."
    exit 1
fi

# Install Blender
sudo apt install -y snapd > /dev/null
sudo snap install blender --classic > /dev/null
echo "Installed Blender version:"
blender --version | grep Blender

# Upgrade pip
sudo python3.11 -m pip install --upgrade pip > /dev/null

# Install python venv
sudo apt-get install python3.11-venv > /dev/null

# Setup Python virtual environment
python3.11 -m venv seeda_python_virtual_environment > /dev/null
source seeda_python_virtual_environment/bin/activate
pip install --no-cache-dir -r requirements_linux.txt

# Remove existing environment variables
sudo rm -f database/.env data/EnvironmentVariables/.env

# Set up environment variables
python3.11 main.py --install --host 127.0.0.1 --port $POSTGRES_PORT --admin_username postgres --admin_password $POSTGRES_PASSWORD

# Populate database
python3.11 -m database.Population.populate_authentication_data
python3.11 -m database.Population.populate_canadian_postal_code_data
python3.11 -m database.Population.populate_climate_data
python3.11 -m database.Population.populate_save_data
python3.11 -m database.Population.populate_wind_speed_data

# Deactivate the virtual environment
deactivate