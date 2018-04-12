To setup Raspberry Pi

	1. Download and flash a new install of Raspian from raspberry pi foundation
	2. Run following commands:
		sudo apt-get update
		sudo apt-get upgrade
		sudo raspi-config
			*Modify to boot to text console
			*Enable SSH
			*Enable SPI
			*Enable GPIO over network

	3. Install SPIDEV
		sudo apg-get install python-dev python3-dev
		git clone https://github.com/doceme/py-spidev.git
		make
		sudo make install
	4. Make sure SPIDEV installed correctly making sure it imports w/o errors
		python3
		>>>import spidev

	5. Clone autobot-racing
		git clone https://github.com/agoeckner/autobot-racing.git


To have Raspberry Pi start event loop on boot

	1. Run command inside pi-drivers folder
		sudo ./bootSetup.sh
