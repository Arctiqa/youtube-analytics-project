import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.title = youtube.playlists().list(part="snippet",
                                              id=self.playlist_id)\
            .execute()['items'][0]['snippet']['localized']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails',
                                               id=','.join(video_ids)
                                               ).execute()
        total = timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        videos = []
        for video in video_ids:
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video
                                                   ).execute()
            videos.append(video_response)
        best_video = max(videos, key=lambda x: x['items'][0]['statistics']['likeCount'])
        video_id = f"https://youtu.be/{best_video['items'][0]['id']}"
        return video_id
