# TeamJoint
this code is meant to be run an Pycom LoPy4 with a Pytrack shield. The purpose
of this code is to measure a users joint movement constantly following joint
arthroplasty. This code was created as part of a capstone project at The
Pennsylvania State University in partnership with Hershey Medical Center. This
code was written by John Comonitski while working as a member of TeamJoint.

## Modes
The device features 4 modes. They are:

Mode: "write" prints data to disk

Mode: "Ewrite" prints encrypted data to disk

Mode: "adafruit" publishes data to adafruitIO

Mode: "decrypt" Will decrypt data if given private key

The mode can be changed in the config.json file

## Encryption
Data collected by the device can be encrypted to ensure user/patient data is
private. This done using a public and private key. The are expected to be .pem
files

Public and private keys are generate using these OpenSSl commands:

$ openssl genrsa -des3 -out private.pem 2048

$ openssl rsa -in private.pem -outform PEM -pubout -out public.pem

$ openssl rsa -in private.pem -out private_unencrypted.pem -outform PEM

When setting up the device, the public key may be saved onto the sd card,
however only put the private key on the sd card when decrypting data and should
be removed once done. Keep the private key private to ensure user data is
secure.

## Networking
The device requires wifi to set the internal clock. Networks can be added in
the config.json

## Data Collection Speed
The number of measurements per second can be adjusted by altering the
frequency in the config.json

## Adafuit
An adafruit mode was included to allow for live demonstrations of the device.
This mode sends live data to Adafuit.io. It is currently configure for our
personal TeamJoint dashboard. Those settings can be changed in the congfig.json.
It sends data at a rate of once every 2 seconds.

## LED
The LoPy 4 features an LED. We use this LED to indicate the board is running and
what mode it is currently running.

Color: Green - writing data

Color: Blue - connected to Adafruit.io

Color: Red - Decrypting data (blue once complete)

When using this device for long term patient test, it may be advised to turn off
the LED to save battery.
