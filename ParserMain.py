import os
import csv
import logging
import json
import shutil
from datetime import datetime
from optparse import OptionParser
from Commands import CommandFactory
from utilities import parse_size

def setup_logging():
    """Set up logging to file."""
    logging.basicConfig(
        filename='CommandDebugger.log',  # Path to your log file
        level=logging.DEBUG,  # Logging level
        format='%(asctime)s - %(levelname)s - %(message)s'  # Format of log messages
    )
    logger = logging.getLogger('CommandDebugger')
    return logger

def get_parser():
    """Set up CLI argument parser."""
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="Path to the input file", metavar="FILE")
    parser.add_option("-o", "--output", dest="output", help="Output log file", metavar="OUTPUT")
    return parser

def cleanup_directory(directory):
    """Cleanup the directory if it exists."""
    if os.path.exists(directory):
        shutil.rmtree(directory)

def setup_directories(output_dir, clear=True):
    """Setup or clear directories based on the configuration."""
    if clear:
        cleanup_directory(output_dir)
    os.makedirs(output_dir, exist_ok=True)

def manage_run_counter(counter_path='counter.txt'):
    """Manage the counter for run ID."""
    try:
        with open(counter_path, 'r') as file:
            current_run_id = int(file.read().strip())
    except FileNotFoundError:
        current_run_id = 0
    current_run_id += 1
    with open(counter_path, 'w') as file:
        file.write(str(current_run_id))
    return current_run_id

def load_config():
    with open('configuration.json', 'r') as file:
        return json.load(file)

def manage_file_limit(directory, max_files):
    """Ensure the directory contains no more than max_files files, deleting the oldest if necessary."""
    max_files = int(max_files)  # Ensure max_files is an integer
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort(key=os.path.getmtime, reverse=True)  # Sort files by modification time, newest first

    logger = logging.getLogger('CommandDebugger')
    logger.debug(f"Total files in directory before cleanup: {len(files)}")

    if len(files) > max_files:
        files_to_delete = files[max_files:]  # Get all files beyond the max_files limit
        for file in files_to_delete:
            os.remove(file)
            logger.debug(f"Deleted old file: {file}")
        logger.info(f"Removed {len(files_to_delete)} files to maintain the limit of {max_files}.")
    else:
        logger.info("No file deletion needed.")

    remaining_files = os.listdir(directory)
    logger.debug(f"Remaining files in directory after cleanup: {remaining_files}")

def execute_commands_from_file(filename, output_dir, config, logger):
    max_commands = int(config.get('Max_commands', 5))  # Get the maximum number of commands to execute
    count = 0  # Initialize command count
    same_dir = config.get('Same_dir', False)
    output_format = config.get('Output', 'csv')

    passed_dir = output_dir if same_dir else os.path.join(output_dir, "Passed")
    failed_dir = output_dir if same_dir else os.path.join(output_dir, "Failed")

    if not same_dir:
        os.makedirs(passed_dir, exist_ok=True)
        os.makedirs(failed_dir, exist_ok=True)

    with open(filename, 'r') as file:
        for line in file:
            if count >= max_commands:
                break  # Stop processing if maximum commands count is reached
            parts = line.strip().split()
            if parts:
                command_name = parts[0]
                args = parts[1:]  # All arguments after the command name
                try:
                    command = CommandFactory.get_command(command_name, *args)  # Create command instance
                    success = command.execute()  # Execute command and store result
                    file_type = "PASSED" if success else "FAILED"
                    result_filename = f"{file_type}{config['run_id']}"

                    if output_format == "csv":
                        result_path = os.path.join(passed_dir if success else failed_dir, f"{result_filename}.csv")
                        # Append results to the appropriate CSV file
                        with open(result_path, 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([command_name, 'Success' if success else 'Failure'])
                    elif output_format == "log":
                        result_path = os.path.join(passed_dir if success else failed_dir, f"{result_filename}.log")
                        # Append results to the appropriate log file
                        with open(result_path, 'a') as logfile:
                            logfile.write(f"{command_name}: {'Success' if success else 'Failure'}\n")

                    count += 1  # Increment command count
                except Exception as e:
                    logger.error(f"Error executing {command_name} with args {args}: {e}")

    # Managing file limits
    manage_file_limit(passed_dir if same_dir else output_dir, config['Max_log_files'])
    if not same_dir:
        manage_file_limit(failed_dir, config['Max_log_files'])

def main():
    logger = setup_logging()
    parser = get_parser()
    options, args = parser.parse_args()

    if options.filename:
        config = load_config()
        config['run_id'] = manage_run_counter()
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['Output_directory'])

        logger.info(f"Input file is: {options.filename}")
        execute_commands_from_file(options.filename, output_dir, config, logger)
        logger.info(f"Output directory is: {output_dir}")

        # Managing file limits for passed and failed directories
        if not config.get('Same_dir', False):
            passed_dir = os.path.join(output_dir, "Passed")
            failed_dir = os.path.join(output_dir, "Failed")
            manage_file_limit(passed_dir, config['Max_log_files'])
            manage_file_limit(failed_dir, config['Max_log_files'])

if __name__ == "__main__":
    main()
