#!/usr/bin/env bash

# Init
APPLICATION_DIR="/Users/$USER/Applications/"
APP_NAME="$(echo $1)"
if [ "$1" = "--help" ]; then
	echo "sh install.sh <program name> [<application folder>]"
	exit 1
fi
if ! echo "$1" | grep -q -E '^[A-Za-z0-9]+$'; then
	echo "program name failed regex [A-Za-z0-9 ]+"
	exit 1
fi

# Locate
echo "Locating package $APP_NAME"
URL=$(curl https://api.github.com/repos/nloomans/Codam.app/releases/latest  --silent | grep 'browser_download_url' | grep -i $APP_NAME)
if [ -z "$URL" ]; then
	echo "App Not Supported"
	exit 1
fi
URL=$(echo $URL | cut -f4 -d'"')

# Install
if  [[ ! -z "$2" ]]; then
	APPLICATION_DIR="$2"
fi
cd $APPLICATION_DIR
if [ $? -eq 1 ]; then
	echo "Custom location does not exist"
	echo "Choose one that does"
	exit 1
fi
echo "Downloading $URL"
TARBALL_NAME=$(basename $URL)
curl -L $URL > ${TARBALL_NAME}
echo "Extracting Package"
tar -zxvf ${TARBALL_NAME}
rm ${TARBALL_NAME}
echo "Package Installed"
