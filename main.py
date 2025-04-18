import os
import sys
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from youtubesearchpython import VideosSearch
import yt_dlp

# Load environment variables
load_dotenv()

# Get Spotify API credentials from environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    print("Error: Spotify credentials not found in .env file")
    sys.exit(1)

# Setup Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

def get_playlist_tracks(playlist_url):
    print("Extracting playlist ID from URL...")
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    print(f"Playlist ID: {playlist_id}")
    
    print("Fetching initial playlist data...")
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    page = 1
    
    while results:
        print(f"\nProcessing page {page} of playlist...")
        for i, item in enumerate(results['items'], 1):
            track = item['track']
            if track:
                name = track['name']
                artists = ', '.join([artist['name'] for artist in track['artists']])
                tracks.append(f"{name} {artists}")
                print(f"  [{len(tracks)}] Found track: {name} by {artists}")
        
        if results['next']:
            print("More tracks available, fetching next page...")
            results = sp.next(results)
            page += 1
        else:
            results = None
            print("\nReached end of playlist.")
    
    return tracks

def search_youtube(query):
    print(f"Searching YouTube for: {query}")
    search = VideosSearch(query, limit=1)
    result = search.result()['result']
    if result:
        video_title = result[0]['title']
        video_link = result[0]['link']
        print(f"Found match: {video_title}")
        return video_link
    print("No matches found on YouTube")
    return None

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        filename = d.get('filename', '').split('/')[-1]
        sys.stdout.write(f"\rDownloading {filename}: {downloaded} | Speed: {speed} | ETA: {eta}")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        print("\nDownload complete. Starting audio conversion...")

def clean_downloads_folder(output_path='downloads'):
    print("\nCleaning up download folder...")
    for file in os.listdir(output_path):
        if not file.lower().endswith('.mp3'):
            try:
                os.remove(os.path.join(output_path, file))
            except Exception as e:
                print(f"Failed to remove temporary file {file}: {str(e)}")

def download_song(youtube_url, output_path='downloads'):
    print(f"\nPreparing to download from: {youtube_url}")
    print(f"Output directory: {os.path.abspath(output_path)}")
    os.makedirs(output_path, exist_ok=True)

    ffmpeg_path = r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'quiet': True,
        'ffmpeg_location': ffmpeg_path
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("Starting download...")
        ydl.download([youtube_url])
        clean_downloads_folder(output_path)

def main():
    print("\n=== Spotify Playlist Downloader ===\n")
    playlist_url = input("Enter Spotify playlist URL: ").strip()
    
    print("\nInitializing download directory...")
    os.makedirs("downloads", exist_ok=True)
    print(f"Download directory: {os.path.abspath('downloads')}")

    print("\nConnecting to Spotify API...")
    tracks = get_playlist_tracks(playlist_url)
    print(f"\nTotal tracks found in playlist: {len(tracks)}")

    print("\nStarting download process...")
    successful = 0
    failed = 0

    for i, track in enumerate(tracks, 1):
        print(f"\n{'='*50}")
        print(f"Processing track {i}/{len(tracks)}")
        print(f"Track: {track}")
        
        yt_url = search_youtube(track)
        if yt_url:
            try:
                download_song(yt_url)
                successful += 1
                print(f"Successfully downloaded and converted to MP3")
            except Exception as e:
                failed += 1
                print(f"Failed to download: {str(e)}")
        else:
            failed += 1
            print("Skipping track due to YouTube search failure")

    clean_downloads_folder()  # Final cleanup to ensure no temporary files remain
    
    print("\n{'='*50}")
    print("\nDownload Summary:")
    print(f"Total tracks processed: {len(tracks)}")
    print(f"Successfully downloaded: {successful}")
    print(f"Failed downloads: {failed}")
    print("Done!")

if __name__ == "__main__":
    main()
