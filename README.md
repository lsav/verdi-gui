# verdi-gui

Small Python program to interface a Windows PC with a Coherent Verdi series laser. Allows for laser control, monitoring and logging of laser health stats.

## Usage

Just run the installer found at `installer/verdigui-setup-1.1.2.exe`. No other installations needed.

Don't trust weird executables from github? You can run it as a python script, but will need to install Python 2.7 and follow the instructions below to install the other dependencies.

## Changes

August 2017: add baseplate temperature to logfiles, allow adding a comment when making a log.

May 2019: commit Windows installer.

## Development

### Dependencies

`pip install requirements.txt`

Also needs PyQt4. Installer here: [Sourceforge](https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/)

### Building

To create a standalone exe:

`pyinstaller build.spec`

Whatever setup utility you like to create an installer. I used [Innosetup](http://www.jrsoftware.org/isinfo.php).
