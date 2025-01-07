from youtube_transcript_api import YouTubeTranscriptApi 
from pytube import YouTube
import re
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class GetVideo:
    @staticmethod
    def Id(link):
        """Extracts the video ID from a YouTube video link."""
        logging.debug(f"Processing video link: {link}")
        if "youtube.com" in link:
            pattern = r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
            match = re.search(pattern, link)
            if match:
                video_id = match.group(1)
                logging.debug(f"Video ID: {video_id}")
                return video_id
            else:
                logging.error("Invalid YouTube URL format.")
                return None
        elif "youtu.be" in link:
            pattern = r"youtu\.be/([a-zA-Z0-9_-]+)"
            match = re.search(pattern, link)
            if match:
                video_id = match.group(1)
                logging.debug(f"Video ID: {video_id}")
                return video_id
            else:
                logging.error("Invalid shortened YouTube URL format.")
                return None
        else:
            logging.error("Invalid URL. Not a valid YouTube link.")
            return None

    @staticmethod
    def title(link):
        """Gets the title of a YouTube video using pytube."""
        try:
            yt = YouTube(link)
            return yt.title
        except Exception as e:
            logging.error(f"Error retrieving video title: {e}")
            return "⚠️ There seems to be an issue with the YouTube video link provided. Please check the link and try again."
        
    @staticmethod
    def transcript(link):
        """Gets the transcript of a YouTube video."""
        video_id = GetVideo.Id(link)
        if video_id is None:
            return "⚠️ Invalid YouTube link."
        
        try:
            transcript_dict = YouTubeTranscriptApi.get_transcript(video_id)
            final_transcript = " ".join(i["text"] for i in transcript_dict)
            logging.debug(f"Transcript retrieved: {final_transcript[:100]}...")  # Show first 100 chars for debugging
            return final_transcript
        except Exception as e:
            logging.error(f"Error fetching transcript: {e}")
            return "⚠️ Failed to retrieve video transcript."
        
    @staticmethod
    def transcript_time(link):
        """Gets the transcript of a YouTube video with timestamps."""
        video_id = GetVideo.Id(link)
        if video_id is None:
            return "⚠️ Invalid YouTube link."
        
        try:
            transcript_dict = YouTubeTranscriptApi.get_transcript(video_id)
            final_transcript = ""
            for i in transcript_dict:
                timevar = round(float(i["start"]))
                hours = int(timevar // 3600)
                timevar %= 3600
                minutes = int(timevar // 60)
                timevar %= 60
                timevex = f"{hours:02d}:{minutes:02d}:{timevar:02d}"
                final_transcript += f'{i["text"]} "time:{timevex}" '
            logging.debug(f"Timestamped transcript retrieved: {final_transcript[:100]}...")  # Show first 100 chars for debugging
            return final_transcript
        except Exception as e:
            logging.error(f"Error fetching timestamped transcript: {e}")
            return "⚠️ Failed to retrieve video transcript with timestamps."
