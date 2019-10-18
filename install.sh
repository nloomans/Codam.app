#!/bin/bash

# INIT
DIR="/Users/$USER/Applications/"
APP_NAME=$(echo $1 | awk '{print tolower($0)}')
APP_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${APP_NAME:0:1})${APP_NAME:1}"
if [ $1 = "-controls" ]; then
	echo "sh install.sh [App Name] [Absolute Install Location(optional)]"
	exit 1
fi
VAL=$(curl https://api.github.com/repos/nloomans/Codam.app/releases/latest  --silent | grep 'browser_download_url' | grep $APP_NAME)
if [ -z VAL ]; then
	# not found
	echo "App Not Supported"
	exit 1
fi

# Work
if  [[ ! -z $2 ]]; then
	DIR= $(echo $2)
fi
cd $DIR
if [ $? -eq 1 ]; then
	echo "Custom Location Does Not Exist"
	echo "Choose One That Does"
	exit 1
fi
VAL=$(echo $VAL | cut -f4 -d'"')
echo "Downloading Package"
curl -L $VAL > ${APP_NAME}.app.tar.gz
echo "Package Downloaded"
echo "Installing Package"
tar -zxvf ${APP_NAME}.app.tar.gz
rm ${APP_NAME}.app.tar.gz
echo "Package Installed"