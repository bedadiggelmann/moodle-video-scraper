import requests
import subprocess
import os
import shutil

# Create a temporary directory for downloads
temp_dir = "temp_video_download"
os.makedirs(temp_dir, exist_ok=True)

# Base URL for the segments
base_url = ""
# Segment name pattern
segment_pattern = "seg-{}-v1-a1.ts"
# Parameters
params = {
    "Policy": "",
    "Signature": "",
    "Key-Pair-Id": "",
}
# Range of segments (replace with actual range)
start_segment = 1
end_segment = 2

segment_files = []

for i in range(start_segment, end_segment + 1):
    segment_url = base_url + segment_pattern.format(i)
    response = requests.get(segment_url, params=params)

    if response.status_code == 200:
        segment_file = os.path.join(temp_dir, f"segment_{i}.ts")
        with open(segment_file, "wb") as f:
            f.write(response.content)
        segment_files.append(segment_file)
        print(f"Downloaded segment {i}")
    else:
        print(f"Failed to download segment {i}")

# Write the segment file list for ffmpeg
with open("segments.txt", "w") as f:
    for segment_file in segment_files:
        f.write(f"file '{segment_file}'\n")

# Run ffmpeg command to concatenate segments
ffmpeg_command = [
    "ffmpeg",
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    "segments.txt",
    "-c",
    "copy",
    "-bsf:a",
    "aac_adtstoasc",
    "output.mp4",
]

print("Running ffmpeg command to concatenate segments...")
subprocess.run(ffmpeg_command)
print("Video concatenation complete: output.mp4")

# Validate the output file (optional step)
if os.path.exists("output.mp4"):
    print("Output file exists. Deleting temporary files...")
    # Delete the temporary directory and its contents
    shutil.rmtree(temp_dir)
    print("Temporary files deleted.")
else:
    print("Output file does not exist. Keeping temporary files for inspection.")
