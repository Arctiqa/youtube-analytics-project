from googleapiclient.discovery import build
import os
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.title = self.channel['items'][0]['snippet']['title']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"<{self.title}> (<{self.url}>)"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=5))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, json_file):
        data = {
            'channel_id': self.__channel_id,
            'url': self.url,
            'title': self.title,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=5)

# ch = Channel('UCwHL6WHUarjGfUM_586me8w')
# ch.print_info()
# print(ch.url)
# print(ch.subscriber_count)
# print(ch.video_count)
# print(ch.view_count)
# ch.print_info()
# values = ch.__dict__
# print(values)
# print(ch.title)
# ch.to_json('channel_info.json')
# ch.__channel_id = 'Новое название'
# print(ch.channel_id)
