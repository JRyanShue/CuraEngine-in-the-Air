sudo apt-get -y update  # update Ubuntu
sudo apt-get -y install git wget autoconf automake libtool curl make g++ unzip cmake python3 python3-dev python3-sip-dev python3-pip nodejs build-essential protobuf-compiler libprotoc-dev libprotobuf-dev awscli # install immediate dependencies
sudo wget https://github.com/google/protobuf/releases/download/v3.5.0/protobuf-all-3.5.0.zip
sudo git clone https://github.com/Ultimaker/libArcus.git
sudo unzip protobuf-all-3.5.0.zip
cd /protobuf-3.5.0
sudo ./autogen.sh
sudo ./configure
sudo make
sudo make install
sudo ldconfig
cd /libArcus
sudo git pull
sudo git checkout 4.4
sudo mkdir build
cd build
sudo cmake .. && make -j4 && make install
cd /
sudo git clone https://github.com/JRyanShue/ZengerEngine.git
cd /ZengerEngine
sudo mkdir build
cd build
sudo cmake .. && make
cd /
sudo mkdir app
cd /app
sudo git clone https://github.com/JRyanShue/ZengerEngine-Presets.git
cd ZengerEngine-Presets
sudo git pull
cd /
cd app
sudo git clone https://github.com/JRyanShue/Test-STLs.git
cd Test-STLs
sudo git pull
cd /
cd app
sudo mkdir resources  # unused
sudo wget https://raw.githubusercontent.com/JRyanShue/ZengerCuraEngine-in-the-Air/main/requirements.txt?token=ATIMPYVPEAAEVLMO37X37KLBFJ7S4 -o requirements.txt
sudo pip3 install -r requirements.txt
sudo apt-get install curl

sudo git clone https://github.com/JRyanShue/ZengerCuraEngine-in-the-Air.git
cd ZengerCuraEngine-in-the-Air
sudo git pull
cd ..

# JS
cd /
cd app
sudo apt-get -y install npm  # add JS stuff
sudo npm install --global http-server
sudo git clone https://github.com/JRyanShue/Zenger-Writer-Frontend.git
cd Zenger-Writer-Frontend
sudo git pull

# Build React App

# sudo python3 ./ZengerCuraEngine-in-the-Air/main.py