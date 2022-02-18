# ra1nstorm
Tethered downgrade 64-bit iDevices vulnerable to checkm8

Since the purpose of this tool is to tethered downgrade a device, after restoring please use one of the tools listed below to tethered boot it:
* [Ramiel](https://github.com/MatthewPierson/Ramiel)
* [PyBoot](https://github.com/MatthewPierson/PyBoot)
* [ra1nsn0w](https://github.com/tihmstar/ra1nsn0w)
## Usage
```
usage: ra1nstorm iPSW [-u]

ra1nstorm - Tethered downgrade 64-bit iDevices vulnerable to checkm8

positional arguments:
  iPSW                  iPSW file used for restoring

optional arguments:
  -h, --help            show this help message and exit
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
## Requirements
* A computer running macOS
* 3 gigabytes free space on the computer
* 64-bit iDevice (vulnerable to checkm8)
* Binaries:
1. [futurerestore](https://nightly.link/m1stadev/futurerestore/workflows/ci/test)
2. [img4tool](https://github.com/tihmstar/img4tool)
3. [img4](https://github.com/xerub/img4lib) (img4lib)
4. [kairos](https://github.com/dayt0n/kairos)
5. [irecovery](https://github.com/libimobiledevice/libirecovery) (irecovery version must be >= 1.0.1)
6. [Kernel64Patcher](https://github.com/Ralph0045/Kernel64Patcher)
7. [asr64_patcher](https://github.com/exploit3dguy/asr64_patcher)
8. [tsschecker](https://github.com/1Conan/tsschecker)

After downloading the binaries above, you have to move them to PATH (e.g. ```/usr/local/bin```)

* [Python3](https://www.python.org/downloads/)
* Install ra1nstorm requirements: ```pip3 install -r requirements.txt```
## Issue
Feel free to open an issue if you need support/report a bug
## Credits
* Special thanks to [m1stadev](https://github.com/m1stadev) for wikiproxy and buildmanifest parser
* [mcg29](https://github.com/mcg29) for [kerneldiff](https://github.com/mcg29/kerneldiff)
