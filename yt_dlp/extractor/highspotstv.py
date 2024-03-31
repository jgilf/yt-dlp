import functools

from .common import InfoExtractor
from .vhx import VHXIE
from ..utils import (
    OnDemandPagedList,
    extract_attributes,
    get_elements_html_by_class,
    traverse_obj
)


class HighspotsTVIE(VHXIE):
    _VALID_URL = VHXIE._VALID_URL_TEMPL % r'(?:www\.)?highspots\.tv'
    _NETRC_MACHINE = 'highspots'
    _LOGIN_URL = 'https://www.highspots.tv/login'
    _URL_BASE = 'https://www.highspots.tv/'


class HighspotsTVSeasonIE(InfoExtractor):
    _PAGE_SIZE = 24
    _VALID_URL = r'https?://(?P<domain>(?:www\.)?highspots\.tv)/(?P<id>[^\/$&?#]+)(?:/?$|/season:(?P<season>[0-9]+)/?$)'

    def _fetch_page(self, url, season_id, page):
        page += 1
        webpage = self._download_webpage(
            f'{url}?page={page}', season_id, note=f'Downloading page {page}', expected_status={400})
        yield from [self.url_result(item_url, HighspotsTVIE) for item_url in traverse_obj(
            get_elements_html_by_class('browse-item-link', webpage), (..., {extract_attributes}, 'href'))]

    def _real_extract(self, url):
        season_id = self._match_id(url)
        season_num = self._match_valid_url(url).group('season') or 1
        season_title = season_id.replace('-', ' ').title()

        return self.playlist_result(
            OnDemandPagedList(functools.partial(self._fetch_page, url, season_id), self._PAGE_SIZE),
            f'{season_id}-season-{season_num}', f'{season_title} - Season {season_num}')