from .vhx import (
    VHXIE,
    VHXSeasonIE
)


class HighspotsTVIE(VHXIE):
    _VALID_URL = VHXIE._VALID_URL_TEMPL % r'(?:www\.)?highspots\.tv'
    _NETRC_MACHINE = 'highspots'
    _LOGIN_URL = 'https://www.highspots.tv/login'
    _URL_BASE = 'https://www.highspots.tv/'


class HighspotsTVSeasonIE(VHXSeasonIE):
    _PAGE_SIZE = 24
    _VALID_URL = VHXSeasonIE._VALID_URL_TEMPL % r'(?:www\.)?highspots\.tv'
