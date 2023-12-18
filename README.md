# VideoURL2Wav (Bilibili and YouTube Audio Downloader)
Python Script to Extract Audio Files (.wav) from YouTube or Bilibili Video Links.

This script allows you to download and convert audio from Bilibili and YouTube videos into WAV format. It is useful for extracting high-quality audio tracks from online video content.

## Features
- **[NEW]:** Support for downloading audio from multi-part Bilibili videos.
- **[NEW]:** Command-line arguments for input CSV file and download directory.
- Download audio from Bilibili and YouTube URLs.
- Convert downloaded audio to WAV format.
- Support for proxy usage during downloads.

## Installation

1. Clone this repository:
   `git clone https://github.com/HarryHe11/VideoURL2Wav.git`
2. Navigate to the project directory:
   `cd VideoURL2Wav`
3. Install required packages:
   `pip install -r requirements.txt`

## Usage

To use the script with command-line arguments, follow these steps:

1. Ensure you have a CSV file with video URLs in a column named "Url".
2. Use command-line arguments to specify the input CSV file and output path.
3. Run the script:
   `python run.py -f <path_to_csv_file> -d <download_directory>`

   For example:
   `python run.py -f urls.csv -d downloads`

Note: Replace `<path_to_csv_file>` with the path to your CSV file and `<download_directory>` with the path to your desired download directory.
