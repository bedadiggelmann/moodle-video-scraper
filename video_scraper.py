import requests

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
        segment_file = f"segment_{i}.ts"
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
