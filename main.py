import os
import sys
import json

try:
    from exporter import export_clips
except ImportError:
    print("Error: exporter module not found")
    sys.exit(1)

try:
    from utils import validate_timestamps
except ImportError:
    print("Error: utils module not found")
    sys.exit(1)

def load_config(config_path):
    """Load configuration from a JSON file."""
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
            return config
        except json.JSONDecodeError:
            print("Error decoding JSON from the config file.")
            sys.exit(1)

def get_user_input():
    """Get timestamps from user input."""
    try:
        timestamps_str = input("Enter timestamps in format start,end start,end (e.g., 1.0,2.5 3.0,4.5): ")
        timestamp_pairs = timestamps_str.strip().split()
        timestamps = []
        for pair in timestamp_pairs:
            start, end = pair.split(',')
            timestamps.append((float(start), float(end)))
        
        # Validate timestamps
        if not validate_timestamps(timestamps):
            print("Invalid timestamps. Ensure start is less than end and they are positive.")
            sys.exit(1)
        return timestamps
    except ValueError:
        print("Invalid input format. Please use start,end format separated by spaces.")
        sys.exit(1)

def main():
    """Main entry point for the script."""
    print("Welcome to ScreenFlow Video Clip Exporter!")
    
    # Load configuration
    config_path = 'config.json'  # Assuming config file is named config.json
    config = load_config(config_path)

    # Get timestamps from user
    timestamps = get_user_input()
    
    # Export clips using the exporter
    try:
        for start, end in timestamps:
            print(f"Exporting clip from {start} to {end}...")
            export_clips(config['project_path'], start, end, config['output_path'])
            print(f"Clip exported successfully!")
    except Exception as e:
        print(f"An error occurred during export: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# TODO: Add GUI for easier timestamp input
# TODO: Implement logging instead of print statements
# TODO: Handle more edge cases for user input and export process
# TODO: Improve error handling in the exporter module
