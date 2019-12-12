# Codam.app

Codam.app is a repository of applications which are normally difficult to
install on a Codam iMac because of the inability to mount `.dmg`s.

## Installing

The recommended way to install an app is to use the installation script.
Download the install.sh file from the git repository using the command below.

```bash
curl https://raw.githubusercontent.com/nloomans/Codam.app/master/install.sh > install.sh
```

You can this bash file to install programs using the following syntax.

```bash
sh install.sh <program name> [<application folder>]
```

## Manual Installation

You can find the latest downloads on
[the releases page.](https://github.com/nloomans/Codam.app/releases/latest/)
Download the tar.gz file for your application. Extract into your desired
installation directory. Once Extracted the program is installed. You can delete
the tar.gz file. Double click on the .app folder/file to start the program.

## Deletion

You can delete the programs at any time by going to the install location and
deleting the .app folder. By default this location is `~/Applications`.

## Requesting an .app

Create a separate issue for every app you want to add. Put the app name in the
title for easy searching.

Requirements for inclusion:

 - Must not be installable using homebrew.

## Visual Studio Code

Visual Studio Code is not included because it can be installed using homebrew.
Run the following command to install the latest version of Visual Studio Code:

```bash
brew cask install visual-studio-code --appdir=~/Applications
```

## Atom

Atom is not included because it can be installed using homebrew.
Run the following command to install the latest version of Atom:

```bash
brew cask install atom --appdir=~/Applications
```
