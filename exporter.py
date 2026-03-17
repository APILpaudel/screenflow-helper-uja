import os
import subprocess
import json

class ScreenFlowExporter:
    def __init__(self, project_file):
        self.project_file = project_file
        self.clips = []

    def load_project(self):
        """Load the ScreenFlow project file and extract clip timestamps."""
        try:
            with open(self.project_file, 'r') as file:
                project_data = json.load(file)
                self.clips = project_data.get('clips', [])
        except FileNotFoundError:
            raise FileNotFoundError(f"Project file {self.project_file} not found.")
        except json.JSONDecodeError:
            raise ValueError("Project file is not a valid JSON.")

    def export_clip(self, start_time, end_time, output_file):
        """Export a single clip using ffmpeg."""
        input_file = self.get_input_file()
        if not input_file or not os.path.exists(input_file):
            raise RuntimeError(f"Input file not found: {input_file}")

        command = [
            'ffmpeg',
            '-i', input_file,
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c', 'copy',
            output_file
        ]
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Exported clip to {output_file}")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            raise RuntimeError(f"FFmpeg error: {error_msg}")

    def get_input_file(self):
        """Get the input video file path from the project data."""
        # This function should extract the main video file path from the project data.
        # For simplicity, we are returning a hardcoded path here.
        # TODO: Implement logic to extract the actual input file from project data.
        return "path/to/input_video.mov"

    def export_clips(self, output_dir):
        """Export all clips to the specified directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for index, clip in enumerate(self.clips):
            start_time = clip.get('start_time')
            end_time = clip.get('end_time')
            
            if start_time is None or end_time is None:
                print(f"Skipping clip {index + 1}: missing start_time or end_time")
                continue
                
            output_file = os.path.join(output_dir, f"clip_{index + 1}.mov")

            try:
                self.export_clip(start_time, end_time, output_file)
            except Exception as e:
                print(f"Failed to export clip {index + 1}: {e}")

if __name__ == "__main__":
    exporter = ScreenFlowExporter("path/to/screenflow_project.json")
    try:
        exporter.load_project()
        exporter.export_clips("exported_clips")
    except Exception as e:
        print(f"Error: {e}")
        # TODO: More sophisticated error handling and logging.
