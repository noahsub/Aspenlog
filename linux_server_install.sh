#!/bin/bash
########################################################################################################################
# linux_server_install.sh
# This file installs the necessary packages and sets up the environment for the Aspenlog 2020 backend on a Linux server.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

# Ensure script is not run as sudo
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run as root"
    exit 1
fi

clear

echo "================================================================================================================="
echo "ASPENLOG 2020 LINUX SERVER INSTALLATION SCRIPT"
echo "================================================================================================================="
echo "This script will install the necessary packages and set up the environment for the Aspenlog 2020 backend."
echo "This include the following:"
echo "  - Docker"
echo "  - Blender"
echo "  - Python 3.11"
echo "  - Python virtual environment"
echo "Note: This will delete any existing Docker container named 'aspenlog2020-database' and any existing environment "
echo "variables associated with the application. Please ensure that you have backed up any necessary data before"
echo "running this script."

echo "_________________________________________________________________________________________________________________"
echo "INSTALLING NECESSARY PACKAGES"
echo "_________________________________________________________________________________________________________________"
# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y ca-certificates curl software-properties-common xorg openbox snapd python3.11 python3-pip screen
echo "Packages installed successfully."

echo "_________________________________________________________________________________________________________________"
echo "INSTALLING DOCKER"
echo "_________________________________________________________________________________________________________________"
# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings > /dev/null
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc > /dev/null

# Add the Docker repository to Apt sources
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install Docker and its plugins
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "Installed Docker version:"
sudo docker --version | grep Docker

echo "_________________________________________________________________________________________________________________"
echo "STOPPING AND REMOVING EXISTING DOCKER CONTAINER IF IT EXISTS"
echo "_________________________________________________________________________________________________________________"

# Stop and remove any existing Docker container
sudo docker stop aspenlog2020-database 2>&1 || true
sudo docker rm aspenlog2020-database 2>&1 || true
echo "Stopped and removed existing Docker container if it existed"

echo "_________________________________________________________________________________________________________________"
echo "SETUP DOCKER CONTAINER FOR POSTGRES DATABASE"
echo "_________________________________________________________________________________________________________________"

# Pull the latest Docker image for Postgres
sudo docker pull postgres:11.22-bullseye

# Prompt for database password and port
read -p "Please enter the password you would like to use for the database: " POSTGRES_PASSWORD
read -p "Please enter the port you would like to use for the database: " POSTGRES_PORT

# Kill any process using the selected port
pid=$(sudo lsof -t -i:"$POSTGRES_PORT")
if [ -n "$pid" ]; then
    sudo kill -9 "$pid"
    echo "Killed process $pid on port $POSTGRES_PORT"
else
    echo "No process using port $POSTGRES_PORT was found"
fi

# Run the Docker container
sudo docker run --name aspenlog2020-database -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" -p "$POSTGRES_PORT":5432 -d --restart=unless-stopped postgres:11.22-bullseye

# Set maximum number of attempts to prevent infinite loop
max_attempts=30
count=0

# Wait for the Postgres service to start accepting connections
echo "Waiting for the PostgreSQL to start..."
until sudo docker exec -it aspenlog2020-database pg_isready -U postgres -h localhost 2>&1 || [ $count -eq $max_attempts ]; do
    sleep 1
    count=$((count+1))
done

# Create the database if the service started, otherwise print an error message
if [ $count -lt $max_attempts ]; then
    echo "PostgreSQL started successfully, creating NBCC-2020 database..."
    sudo docker exec -it aspenlog2020-database psql -U postgres -c "CREATE DATABASE \"NBCC-2020\";"
else
    echo "PostgreSQL did not start within the expected time."
    exit 1
fi

echo "_________________________________________________________________________________________________________________"
echo "INSTALLING BLENDER"
echo "_________________________________________________________________________________________________________________"
# Install Blender
sudo apt install -y snapd
sudo snap install blender --classic
echo "Installed Blender version:"
blender --version | grep Blender

echo "_________________________________________________________________________________________________________________"
echo "INSTALLING REQUIRED BLENDER PACKAGES"
echo "_________________________________________________________________________________________________________________"

# Get the first integer labelled directory
integer_dir=$(find /snap/blender -type d -name "*[0-9]*" | sort -n | head -1)

# Get the first float labelled directory
float_dir=$(find "$integer_dir" -type d -name "*.*" | sort -n | head -1)

# Get the first python version
python_version=$(ls "$float_dir"/python/bin | grep -P '^python3\.\d+$' | sort -V | head -1)

# Construct the pip install command
blender_pip_update="$float_dir/python/bin/$python_version -m pip install --upgrade pip"
json_pickle_install="$float_dir/python/bin/$python_version -m pip install jsonpickle"

# Execute the pip install command
$blender_pip_update
$json_pickle_install

echo "_________________________________________________________________________________________________________________"
echo "SETUP PYTHON 3.11 VIRTUAL ENVIRONMENT"
echo "_________________________________________________________________________________________________________________"
# Upgrade pip
sudo python3.11 -m pip install --upgrade pip

# Install python venv
sudo apt-get install python3.11-venv

# Setup Python virtual environment
python3.11 -m venv seeda_python_virtual_environment
source seeda_python_virtual_environment/bin/activate
echo "Installing Python packages, this may take a while..."
pip install --no-cache-dir -r requirements_linux.txt -q
echo "Python packages installed successfully."

echo "_________________________________________________________________________________________________________________"
echo "SETTING ENVIRONMENT VARIABLES"
echo "_________________________________________________________________________________________________________________"

# Remove existing environment variables
sudo rm -f database/.env data/EnvironmentVariables/.env

# Set up environment variables
python3.11 main.py --install --host 127.0.0.1 --port "$POSTGRES_PORT" --admin_username postgres --admin_password "$POSTGRES_PASSWORD"

echo "Environment variables set successfully."

echo "_________________________________________________________________________________________________________________"
echo "POPULATING DATABASE"
echo "_________________________________________________________________________________________________________________"

# Populate database
python3.11 -m database.Population.populate_authentication_data
python3.11 -m database.Population.populate_canadian_postal_code_data
python3.11 -m database.Population.populate_climate_data
python3.11 -m database.Population.populate_save_data
python3.11 -m database.Population.populate_wind_speed_data

# Deactivate the virtual environment
deactivate

echo "_________________________________________________________________________________________________________________"
echo "RESULT"
echo "_________________________________________________________________________________________________________________"

echo "The installation was successful. The server is now ready to run the Aspenlog 2020 backend."
echo "You can access the postgres database using credentials you created:"
echo "  - Host: 127.0.0.1"
echo "  - Port: $POSTGRES_PORT"
echo "  - Username: postgres"