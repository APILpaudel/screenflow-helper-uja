import os
import json
from datetime import datetime

def load_timestamps(file_path):
    """
    Load timestamps from a JSON file.
    
    :param file_path: Path to the JSON file containing timestamps.
    :return: List of timestamps or raises an error if the file can't be loaded.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Timestamp file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        try:
            timestamps = json.load(f)
            if not isinstance(timestamps, list):
                raise ValueError("Timestamps should be a list.")
            return timestamps
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")

def save_clip(clip_data, output_path):
    """
    Save the video clip data to a specified output path.
    
    :param clip_data: Data of the video clip to save.
    :param output_path: Destination path for the output file.
    :return: None
    """
    try:
        with open(output_path, 'wb') as f:
            f.write(clip_data)
    except IOError as e:
        raise IOError(f"Failed to write clip to {output_path}: {e}")

def parse_timestamp(timestamp_str):
    """
    Parse a timestamp string into a datetime object.
    
    :param timestamp_str: Timestamp string in ISO 8601 format.
    :return: datetime object representing the timestamp.
    """
    try:
        return datetime.fromisoformat(timestamp_str)
    except ValueError:
        raise ValueError(f"Invalid timestamp format: {timestamp_str}")

def validate_output_dir(output_dir):
    """
    Validate and create output directory if it does not exist.
    
    :param output_dir: Path to the intended output directory.
    :return: None
    """
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except OSError as e:
            raise OSError(f"Failed to create output directory: {e}")

def format_clip_name(base_name, start_time, end_time):
    """
    Format the clip name using the base name and timestamps.
    
    :param base_name: Base name for the clip.
    :param start_time: Start time of the clip.
    :param end_time: End time of the clip.
    :return: Formatted clip name.
    """
    start_str = start_time.strftime("%Y%m%d_%H%M%S")
    end_str = end_time.strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{start_str}_{end_str}.mp4"

# TODO: Add functions for actual video processing (e.g., using moviepy or ffmpeg-python)
# TODO: Implement better logging instead of print statements
# TODO: Add unit tests for these utility functions
# TODO: Handle edge cases, such as overlapping timestamps or invalid ranges
