import functools

from .common import InfoExtractor
from .vhx import VHXIE
from ..utils import (
    OnDemandPagedList,
    extract_attributes,
    get_elements_html_by_class,
    traverse_obj
)

class DropoutIE(VHXIE):
    _VALID_URL = VHXIE._VALID_URL_TEMPL % r'(?:www\.)?dropout\.tv'
    _NETRC_MACHINE = 'dropout'
    _LOGIN_URL = 'https://www.dropout.tv/login'
    _URL_BASE = 'https://www.dropout.tv/'

    _TESTS = [
        {
            'url': 'https://www.dropout.tv/game-changer/season:2/videos/yes-or-no',
            'note': 'Episode in a series',
            'md5': '5e000fdfd8d8fa46ff40456f1c2af04a',
            'info_dict': {
                'id': '738153',
                'display_id': 'yes-or-no',
                'ext': 'mp4',
                'title': 'Yes or No',
                'description': 'Ally, Brennan, and Zac are asked a simple question, but is there a correct answer?',
                'release_date': '20200508',
                'thumbnail': 'https://vhx.imgix.net/chuncensoredstaging/assets/351e3f24-c4a3-459a-8b79-dc80f1e5b7fd.jpg',
                'series': 'Game Changer',
                'season_number': 2,
                'season': 'Season 2',
                'episode_number': 6,
                'episode': 'Yes or No',
                'duration': 1180,
                'uploader_id': 'user80538407',
                'uploader_url': 'https://vimeo.com/user80538407',
                'uploader': 'OTT Videos'
            },
            'expected_warnings': ['Ignoring subtitle tracks found in the HLS manifest']
        },
        {
            'url': 'https://www.dropout.tv/dimension-20-fantasy-high/season:1/videos/episode-1',
            'note': 'Episode in a series (missing release_date)',
            'md5': '712caf7c191f1c47c8f1879520c2fa5c',
            'info_dict': {
                'id': '320562',
                'display_id': 'episode-1',
                'ext': 'mp4',
                'title': 'The Beginning Begins',
                'description': 'The cast introduces their PCs, including a neurotic elf, a goblin PI, and a corn-worshipping cleric.',
                'thumbnail': 'https://vhx.imgix.net/chuncensoredstaging/assets/4421ed0d-f630-4c88-9004-5251b2b8adfa.jpg',
                'series': 'Dimension 20: Fantasy High',
                'season_number': 1,
                'season': 'Season 1',
                'episode_number': 1,
                'episode': 'The Beginning Begins',
                'duration': 6838,
                'uploader_id': 'user80538407',
                'uploader_url': 'https://vimeo.com/user80538407',
                'uploader': 'OTT Videos'
            },
            'expected_warnings': ['Ignoring subtitle tracks found in the HLS manifest']
        },
        {
            'url': 'https://www.dropout.tv/videos/misfits-magic-holiday-special',
            'note': 'Episode not in a series',
            'md5': 'c30fa18999c5880d156339f13c953a26',
            'info_dict': {
                'id': '1915774',
                'display_id': 'misfits-magic-holiday-special',
                'ext': 'mp4',
                'title': 'Misfits & Magic Holiday Special',
                'description': 'The magical misfits spend Christmas break at Gowpenny, with an unwelcome visitor.',
                'release_date': '20211215',
                'thumbnail': 'https://vhx.imgix.net/chuncensoredstaging/assets/d91ea8a6-b250-42ed-907e-b30fb1c65176-8e24b8e5.jpg',
                'duration': 11698,
                'uploader_id': 'user80538407',
                'uploader_url': 'https://vimeo.com/user80538407',
                'uploader': 'OTT Videos'
            },
            'expected_warnings': ['Ignoring subtitle tracks found in the HLS manifest']
        }
    ]


class DropoutSeasonIE(InfoExtractor):
    _PAGE_SIZE = 24
    _VALID_URL = r'https?://(?P<domain>(?:www\.)?dropout\.tv)/(?P<id>[^\/$&?#]+)(?:/?$|/season:(?P<season>[0-9]+)/?$)'
    _TESTS = [
        {
            'url': 'https://www.dropout.tv/dimension-20-fantasy-high/season:1',
            'note': 'Multi-season series with the season in the url',
            'playlist_count': 24,
            'info_dict': {
                'id': 'dimension-20-fantasy-high-season-1',
                'title': 'Dimension 20 Fantasy High - Season 1'
            }
        },
        {
            'url': 'https://www.dropout.tv/dimension-20-fantasy-high',
            'note': 'Multi-season series with the season not in the url',
            'playlist_count': 24,
            'info_dict': {
                'id': 'dimension-20-fantasy-high-season-1',
                'title': 'Dimension 20 Fantasy High - Season 1'
            }
        },
        {
            'url': 'https://www.dropout.tv/dimension-20-shriek-week',
            'note': 'Single-season series',
            'playlist_count': 4,
            'info_dict': {
                'id': 'dimension-20-shriek-week-season-1',
                'title': 'Dimension 20 Shriek Week - Season 1'
            }
        },
        {
            'url': 'https://www.dropout.tv/breaking-news-no-laugh-newsroom/season:3',
            'note': 'Multi-season series with season in the url that requires pagination',
            'playlist_count': 25,
            'info_dict': {
                'id': 'breaking-news-no-laugh-newsroom-season-3',
                'title': 'Breaking News No Laugh Newsroom - Season 3'
            }
        }
    ]

    def _fetch_page(self, url, season_id, page):
        page += 1
        webpage = self._download_webpage(
            f'{url}?page={page}', season_id, note=f'Downloading page {page}', expected_status={400})
        yield from [self.url_result(item_url, DropoutIE) for item_url in traverse_obj(
            get_elements_html_by_class('browse-item-link', webpage), (..., {extract_attributes}, 'href'))]

    def _real_extract(self, url):
        season_id = self._match_id(url)
        season_num = self._match_valid_url(url).group('season') or 1
        season_title = season_id.replace('-', ' ').title()

        return self.playlist_result(
            OnDemandPagedList(functools.partial(self._fetch_page, url, season_id), self._PAGE_SIZE),
            f'{season_id}-season-{season_num}', f'{season_title} - Season {season_num}')
