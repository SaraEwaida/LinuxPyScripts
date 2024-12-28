import os
import logging
from abc import ABC, abstractmethod
from utilities import parse_size

# Abstract Base Class for all commands
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class Categorize(Command):
    def __init__(self, directory, threshold_size):
        self.directory = directory
        self.threshold_size = parse_size(threshold_size)  # Convert the threshold size to bytes

    def execute(self):
        logger = logging.getLogger('CommandDebugger')
        small_files_dir = os.path.join(self.directory, "SmallerThanThreshold")
        large_files_dir = os.path.join(self.directory, "LargerThanThreshold")

        os.makedirs(small_files_dir, exist_ok=True)
        os.makedirs(large_files_dir, exist_ok=True)

        files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) if
                 os.path.isfile(os.path.join(self.directory, f))]

        for file in files:
            size = os.path.getsize(file)
            if size < self.threshold_size:
                os.rename(file, os.path.join(small_files_dir, os.path.basename(file)))
                logger.debug(f"Moved {file} to {small_files_dir}")
            else:
                os.rename(file, os.path.join(large_files_dir, os.path.basename(file)))
                logger.debug(f"Moved {file} to {large_files_dir}")

        logger.info(f"Files categorized in {self.directory} based on threshold size {self.threshold_size}")
        return True

class Mv_last(Command):
    def __init__(self, src_directory, des_directory):
        self.src_directory = src_directory
        self.des_directory = des_directory

    def execute(self):
        try:
            files = [os.path.join(self.src_directory, f) for f in os.listdir(self.src_directory)]
            if not files:
                raise FileNotFoundError("No files to move.")
            latest_file = max(files, key=os.path.getctime)
            os.replace(latest_file, os.path.join(self.des_directory, os.path.basename(latest_file)))
            return f"Moved {latest_file} to {self.des_directory}"
        except Exception as e:
            logging.error(f"Error moving file: {str(e)}")
            return None

class Count(Command):
    def __init__(self, directory):
        self.directory = directory

    def execute(self):
        try:
            file_count = len([name for name in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, name))])
            logging.info(f"Number of files in {self.directory}: {file_count}")
            return file_count
        except Exception as e:
            logging.error(f"Error counting files in {self.directory}: {str(e)}")
            return None

class Delete(Command):
    def __init__(self, filename, directory):
        self.filename = filename
        self.directory = directory

    def execute(self):
        try:
            target_path = os.path.join(self.directory, self.filename)
            if os.path.exists(target_path):
                os.remove(target_path)
                logging.info(f"Deleted file: {target_path}")
                return True
            else:
                logging.error(f"File not found: {target_path}")
                return False
        except Exception as e:
            logging.error(f"Error deleting file {self.filename} from {self.directory}: {str(e)}")
            return False

class Rename(Command):
    def __init__(self, old_name, new_name, directory):
        self.old_name = old_name
        self.new_name = new_name
        self.directory = directory

    def execute(self):
        try:
            old_path = os.path.join(self.directory, self.old_name)
            new_path = os.path.join(self.directory, self.new_name)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                logging.info(f"Renamed {old_path} to {new_path}")
                return True
            else:
                logging.error(f"File not found: {old_path}")
                return False
        except Exception as e:
            logging.error(f"Error renaming file {self.old_name} to {self.new_name} in {self.directory}: {str(e)}")
            return False

class List(Command):
    def __init__(self, directory):
        self.directory = directory

    def execute(self):
        try:
            files_and_dirs = os.listdir(self.directory)
            logging.info(f"Contents of {self.directory}: {files_and_dirs}")
            return files_and_dirs
        except Exception as e:
            logging.error(f"Error listing contents of {self.directory}: {str(e)}")
            return None

class Sort(Command):
    def __init__(self, directory, criteria):
        self.directory = directory
        self.criteria = criteria.lower()

    def execute(self):
        try:
            files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
            if self.criteria == "name":
                files.sort(key=lambda x: os.path.basename(x).lower())
            elif self.criteria == "date":
                files.sort(key=os.path.getmtime)
            elif self.criteria == "size":
                files.sort(key=os.path.getsize)
            else:
                logging.error(f"Unknown sorting criteria: {self.criteria}")
                return False
            sorted_files = [os.path.basename(f) for f in files]
            logging.info(f"Sorted files in {self.directory} by {self.criteria}: {sorted_files}")
            return sorted_files
        except Exception as e:
            logging.error(f"Error sorting files in {self.directory} by {self.criteria}: {str(e)}")
            return None

class CommandFactory:
    @staticmethod
    def get_command(command_name, *args):
        if command_name == "Categorize":
            return Categorize(args[0], args[1])
        elif command_name == "Mv_last":
            return Mv_last(args[0], args[1])
        elif command_name == "Count":
            return Count(args[0])
        elif command_name == "Delete":
            return Delete(args[0], args[1])
        elif command_name == "Rename":
            return Rename(args[0], args[1], args[2])
        elif command_name == "List":
            return List(args[0])
        elif command_name == "Sort":
            return Sort(args[0], args[1])
        else:
            raise ValueError(f"Unknown command type: {command_name}")
