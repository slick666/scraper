import json

from urllib.parse import urlencode

import scrapy

from slugify import slugify


class YouTubePlaylistEventSpider(scrapy.Spider):
    """YouTube Playlist Event scraper for PyVideo/PyTube"""

    BASE_API_URL = 'https://www.googleapis.com/youtube/v3/'
    API_MAX_RESULTS = 50

    name = 'youtube_playlist'

    def __init__(self, playlist_id, api_key=None, *args, **kwargs):
        """To run the spider, it's necessary to pass playlist_id and (optionally) an api_key.

        For example:
        $ scrapy runspider videodata/videodata/spiders/youtube_playlist.py \
            -a playlist_id=<PlaylistID> \
            -a api_key=<GoogleAPIKey>
        """
        super().__init__(*args, **kwargs)

        self.playlist_id = playlist_id

        self.base_url_parameters = {
            'part': 'snippet',
            'maxResults': self.API_MAX_RESULTS,
        }

        if api_key:
            self.base_url_parameters['key'] = api_key

        playlists_url_parameters = self.base_url_parameters.copy()
        playlists_url_parameters['id'] = self.playlist_id

        self.start_urls = [
            self.BASE_API_URL + 'playlists?' + urlencode(playlists_url_parameters),
        ]

    def event_item_builder(self, data):
        """Build Event item"""
        return data

    def talk_item_builder(self, data):
        """Build Talk item"""
        return {
            'title': data.get('fulltitle', data['title']),
            'summary': data['description'],
            'description': '',
            'category': '',
            'quality_notes': '',
            'language': '',
            'copyright_text': '',
            'thumbnail_url': data['thumbnail'],
            'duration': data['duration'],
            'source_url': data['webpage_url'],
            'recorded': datetime.strptime(data['upload_date'], '%Y%m%d'),
            'slug': slugify(data['fulltitle'], to_lower=True, max_length=50),
            'tags': data.get('categories', []) + data.get('tags', []),
            'speakers': [],
            'videos': [{
                'length': 0,
                'url': data['webpage_url'],
                'type': 'youtube'
            }]
        }

    def generate_talks_url(self, page_token=None):
        """Generate talks API URL"""
        playlist_items_url_parameters = self.base_url_parameters.copy()
        playlist_items_url_parameters['playlistId'] = self.playlist_id

        if page_token:
            playlist_items_url_parameters['pageToken'] = page_token

        return self.BASE_API_URL + 'playlistItems?' + urlencode(playlist_items_url_parameters)

    def parse_talks(self, response):
        """Parse talks from the response and handle pagination of the Google API results"""
        data = json.loads(response.body.decode())

        items = data.get('items', [])
        for item in items:
            yield self.talk_item_builder(item['snippet'])

        if 'nextPageToken' in data:
            yield scrapy.Request(self.generate_talks_url(page_token=data['nextPageToken']),
                                 callback=self.parse_talks)

    def parse(self, response):
        """Default parser to get the general Event metadata and start the talks scraping"""
        data = json.loads(response.body.decode())

        items = data.get('items', [])
        for item in items:
            yield self.event_item_builder(item['snippet'])

        yield scrapy.Request(self.generate_talks_url(), callback=self.parse_talks)
