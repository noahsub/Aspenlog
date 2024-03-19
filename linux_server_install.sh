# check if user has run the script with sudo
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "This script will install the necessary software to run the AspenLog2020 application on a Linux server."

echo "Running this script will result in the deletion of the existing database if it already exists, are you sure you want to continue? (y/n)"
read CONTINUE
if [ "$CONTINUE" != "y" ]
  then echo "Exiting..."
  exit
fi

echo "Downloading and installing Docker..."
# Add Docker's official GPG key:
apt-get update
apt-get install ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update

apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "Removing existing database..."
docker stop aspenlog2020-database
docker rm aspenlog2020-database

echo "Creating PostgreSQL database..."
docker pull postgres:11.22-bullseye

echo ""
echo "Please enter the password you would like to use for the database:"
read POSTGRES_PASSWORD

echo ""
echo "Please enter the port you would like to use for the database:"
read POSTGRES_PORT

docker run --name aspenlog2020-database -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -p $POSTGRES_PORT:5432 -d postgres:11.22-bullseye

# Wait for the Postgres service to start running in the Docker container
until [ "`docker inspect -f {{.State.Running}} aspenlog2020-database`"=="true" ]; do
    sleep 0.1;
done;

echo "Press Enter to continue..."
read

docker exec -it aspenlog2020-database psql -U postgres -c "CREATE DATABASE \"NBCC-2020\";"

# Install Blender
apt-get install xorg openbox
apt install snapd
snap install blender --classic
blender --version

# Install Python
apt-get install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt-get update -y
apt-get install -y python3.11 python3-pip
python3.11 -m pip install --upgrade pip

# Setup Virtual Environment
apt-get install python3.11-venv
python3.11 -m venv seeda_python_virtual_environment
source seeda_python_virtual_environment/bin/activate
pip install --no-cache-dir -r requirements_linux.txt

# Remove existing environment variables
rm database/.env
rm data/EnvironmentVariables/.env

# Set up environment variables
python3.11 main.py True

# Populate database
python3.11 -m database.Population.populate_authentication_data
python3.11 -m database.Population.populate_canadian_postal_code_data
python3.11 -m database.Population.populate_climate_data
python3.11 -m database.Population.populate_save_data
python3.11 -m database.Population.populate_wind_speed_data
deactivate