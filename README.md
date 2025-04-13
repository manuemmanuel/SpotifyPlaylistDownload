# Spotify Playlist Downloader

A Python script that downloads songs from Spotify playlists using YouTube as the source.

## Features

- Downloads entire Spotify playlists
- Converts videos to MP3 format
- Shows detailed progress information
- Provides download statistics
- Handles errors gracefully

## Prerequisites

1. **Python 3+**
2. **FFmpeg**
   - Install using Chocolatey (recommended):
     ```bash
     choco install ffmpeg
     ```
   - Or download manually from [FFmpeg's official website](https://ffmpeg.org/download.html)

3. **Required Python packages**
   ```bash
   pip install spotipy python-dotenv youtube-search-python yt-dlp```

## Setup Instructions

1. **Clone or download this repository**

2. **Create a Spotify Developer Account**
   - Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Log in with your Spotify account
   - Create a new application
   - Note down your Client ID and Client Secret

3. **Configure Environment Variables**
   - Create a `.env` file in the project directory
   - Add your Spotify credentials:
     ```plaintext
     SPOTIFY_CLIENT_ID=your_client_id_here
     SPOTIFY_CLIENT_SECRET=your_client_secret_here
     ```

## Usage

1. **Start the program**
   ```bash
   python main.py
   ```

2. **Enter Playlist URL**
   - Copy the Spotify playlist URL (e.g., https://open.spotify.com/playlist/...)
   - Paste it when prompted

3. **Wait for Downloads**
   - The program will process each track
   - Progress information will be displayed
   - Downloaded files will be saved in the `downloads` folder

## Output Format

- All songs are saved in the `downloads` directory
- Files are converted to MP3 format
- Audio quality: 192kbps
- Filename format: `{song_title}.mp3`

## Progress Information

The program shows:
- Current track being processed
- Download progress percentage
- Download speed
- Estimated time remaining
- Conversion status
- Final summary with success/failure counts

## Troubleshooting

### Common Issues:

1. **FFmpeg Error**
   - Ensure FFmpeg is properly installed
   - Verify the FFmpeg path in `main.py`
   - Try reinstalling FFmpeg

2. **Spotify API Errors**
   - Check your credentials in the `.env` file
   - Ensure your Spotify Developer application is active
   - Verify your internet connection

3. **Download Failures**
   - Check your internet connection
   - Verify the YouTube video is available in your region
   - Try running the program again for failed tracks

## Limitations

- YouTube search results may not always match the exact song version
- Some videos might be unavailable or region-locked
- Download speed depends on your internet connection
- YouTube's terms of service may change

## Legal Notice

This tool is for personal use only. Please ensure you:
- Respect copyright laws
- Follow Spotify's terms of service
- Comply with YouTube's terms of service
- Use downloaded content for personal purposes only

## Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share improvements

## License

This project is for educational purposes only. Use responsibly and at your own risk.
```