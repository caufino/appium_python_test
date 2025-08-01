# Mentortools Login test implementation

This implementation was done with Appium & Python/Pytest configuration.

## Setup

### Install Node.js & NPM
Depending on your system, installation is different, please refer to NPM documentation:
https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

```
node -v
npm -v
```

### Install Appium
```
npm install -g appium
appium -v
```

https://appium.io/docs/en/2.0/quickstart/install/

### Install UiAutomator2 Driver
```
appium driver install uiautomator2
```
https://appium.io/docs/en/2.0/quickstart/uiauto2-driver/

### Install Python3
Download & install Python3 (3.13+) depending on your OS:
https://www.python.org/downloads/

### Install pip3 dependencies
```
python -m pip install -r requirements.txt
```

### Install Android Studio
Depending on your system, installation is different, please refer to Android Studio documentation:
https://developer.android.com/studio/install

### Create Emulator (for example Pixel 9)
After running Android studio, you'll need to create your own emulated device.
It can be done in Android Studio > Virtual Device Manager > Create Virtual Device

https://developer.android.com/studio/run/managing-avds

### Setup emulated device
You'll need to boot up your emulated device (you might need to update **deviceName** in **test_utils/capabilities.py** depending on created emulated device name by listing:
```
adb devices -l
```

Install Mentortools Academy from Play Store.

## Usage
Fist, you'll need to run your Appium server:
```
appium
```

After setting & starting everything up, tests can be run from home directory via CMD:
```
 pytest -v tests/ --email <email_account> --password <email_password>
```

It expects two input parameters:
 -  --email
 -  --password

to test actual login into the app, so don't forget to pass working account, otherwise tests will fail!
