# ra1nstorm
Tethered downgrade 64-bit iDevices vulnerable to checkm8

Since the purpose of this tool is to tethered downgrade a device, after restoring please use one of the tools listed below to tethered boot it:
* [Ramiel](https://github.com/MatthewPierson/Ramiel)
* [PyBoot](https://github.com/MatthewPierson/PyBoot)
* [ra1nsn0w](https://github.com/tihmstar/ra1nsn0w)

ra1nstorm now supports downgrading untethered from any iOS to iOS 10.3.3 on some A7 devices
## Before using it, please keep in mind
YOU are fully responsible to any data loss or damaged cause to your device while using ra1nstorm
## Usage
```
usage: ra1nstorm iPSW [-u] [-s PATH] [-t BLOB]

ra1nstorm - Tethered downgrade 64-bit iDevices vulnerable to checkm8

positional arguments:
  iPSW                  iPSW file used for restoring

optional arguments:
  -h, --help            show this help message and exit
  -t BLOB, --blob BLOB  Manually specify SHSH used for restoring (SHSH will be
                        automatically saved if this argument is skipped)
  -s PATH, --save-log PATH
                        Specify path for saving futurerestore log
  -u, --update          Keep data while restoring (Untested)
```
## Supported version
All iOS versions from iOS 11 - iOS 14 are supported

NOTE: Due to SEP limitation, you can only restore to an iOS version which its SEP firmware is still being signed
## Success
|  Device   |  From  |   To   |
|-----------|--------|--------|
| iPhone9,1 | 15.2.1 |  14.3  |
| iPad4,2   | 12.5.4 | 10.3.3 |
| iPad4,2   | 12.5.4 |  12.0  |
## Requirements
* A computer running macOS
* 3 gigabytes free space on the computer
* 64-bit iDevice (vulnerable to checkm8)
* Binaries:
1. [futurerestore(fork)](https://github.com/Mini-Exploit/futurerestore) (you can use [futurerestore-compiler](https://github.com/Mini-Exploit/futurerestore-compiler) to compile it)
2. [img4tool](https://github.com/tihmstar/img4tool)
3. [img4](https://github.com/xerub/img4lib) (img4lib)
4. [kairos](https://github.com/dayt0n/kairos)
5. [iBoot64Patcher](https://github.com/tihmstar/iBoot64Patcher)
6. [ldid](https://drive.google.com/uc?export=download&id=1_amZww5ypZ9gcdHDlNmEL2Zh-t3eLKXi)
7. [Kernel64Patcher](https://github.com/Ralph0045/Kernel64Patcher)
8. [asr64_patcher](https://github.com/exploit3dguy/asr64_patcher)
9. [tsschecker](https://github.com/1Conan/tsschecker)

After downloading the binaries above, you have to move them to PATH (e.g. ```/usr/local/bin```)

* [Python3](https://www.python.org/downloads/)
* Install ra1nstorm requirements: ```pip3 install -r requirements.txt```
## Issue
There are 2 ways for you to get support:
1. Open an issue
2. [Join my Discord server](https://discord.gg/nK3Uu6BaDN) 

## Credits
* Special thanks to [m1stadev](https://github.com/m1stadev) for wikiproxy and buildmanifest parser
* [mcg29](https://github.com/mcg29) for [kerneldiff](https://github.com/mcg29/kerneldiff)
