# Check that user is in the SEEDA directory
if [ ! -d "SEEDA" ]; then
    echo "Please run this script from the SEEDA directory of the cloned repository"
    exit 1
fi

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo docker pull postgres:11.22-bullseye

ehco "Please enter the password you would like to use for the database"
read -s POSTGRES_PASSWORD

echo "Please enter the port you would like to use for the database"
read POSTGRES_PORT

docker run --name aspenlog2020-database -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -p $POSTGRES_PORT:5432 -d postgres:11.22-bullseye

# Wait for the Postgres service to start running in the Docker container
echo "Waiting for Postgres service to start..."
while ! docker exec aspenlog2020-database pg_isready -U postgres > /dev/null 2>&1; do
    sleep 1
done

docker exec -it aspenlog2020-database psql -U postgres -c "CREATE DATABASE \"NBCC-2020\";"

# Install Blender
sudo apt-get install xorg openbox
sudo apt install snapd
snap install blender --classic
blender --version

# Install Python
sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update -y
sudo apt-get install -y python3.11 python3-pip
sudo python3.11 -m pip install --upgrade pip

# Populate database
python3.11 database/Population/populate_authentication_data.py
python3.11 database/Population/populate_canadian_postal_code_data.py
python3.11 database/Population/populate_climate_data.py
python3.11 database/Population/populate_save_data.py
python3.11 database/Population/populate_wind_speed_data.py

# Setup Virtual Environment
sudo apt-get install python3.11-venv
python3.11 -m venv seeda_python_virtual_environment
source seeda_python_virtual_environment/bin/activate
pip install --no-cache-dir -r requirements_linux.txt
deactivate