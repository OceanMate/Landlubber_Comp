# Landlubber Computer - ROV Framework

This project is meant to act as a framework for programming ROVs for MATE ROV competitions.

## Project Structure

All programming should only have to be done in the `Robot` and `transmission` folders.

## Installation

In order to auto-install required Python libraries, run the following command in the project directory:

```bash
pip install -r requirements.txt
```

## Network Setup

1. Connect an ethernet cable
2. Go to settings and switch to manual ethernet setup
3. Set IPv4 to `192.168.1.1`
4. Set subnet mask to `255.255.255.0`

## Using PuTTY to Connect to Nautical Computer

1. Connect to `192.168.1.2`
2. Login credentials:
   - **Username:** `materov`
   - **Password:** `1234`

## Running the System

Run the startup script:

```bash
./startup.sh
```

## Updating Repository from Main

Run the git pull script:

```bash
./gitpull.sh
```

## Credits

This project is based on the Command framework from FIRST Robotics. The GUI was inspired by Shuffleboard FRC.

_Yar Har_
