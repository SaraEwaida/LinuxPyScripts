# LinuxPyScripts

## Project Overview
LinuxPyScripts is a Python-based toolkit designed to automate various Linux command tasks such as file management, sorting, and system configuration. This project facilitates the execution of predefined scripts to handle repetitive tasks efficiently, aiming to enhance productivity and ensure consistent system management.

## Features
- **Automated Command Execution**: Automate tasks like moving files, deleting, and renaming through scripts.
- **Flexible Configuration**: Utilize JSON-based configuration to manage execution parameters.
- **Detailed Logging**: Implement Python’s logging module to track command execution and results.

## Technologies Used
- Python: For scripting and automation.
- JSON: For configuration management.
- Linux: The project is intended for use in Linux environments.

## Getting Started

### Prerequisites
- Python 3.x installed on your Linux system.
- Basic knowledge of Linux command line and Python.

### Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/SaraEwaida/LinuxPyScripts.git
cd LinuxPyScripts
```

### Usage
To run the automation script, navigate to the src directory and execute the main script:
python3 script_executor.py
Ensure that your configuration file config.json in the config directory is set up according to your specific requirements.

Configuration
Modify the config.json to set thresholds, directory paths, and other parameters like:
```bash
{
    "threshold_size": "10MB",
    "max_commands": 5
}
```
License
Distributed under the MIT License. See LICENSE for more information.

Contact
 Saraowida123456@gmail.com
