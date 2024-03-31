from .vhx import (
    VHXIE,
    VHXSeasonIE
)


class RevProIE(VHXIE):
    _VALID_URL = VHXIE._VALID_URL_TEMPL % r'(?:www\.)?revproondemand\.com'
    _NETRC_MACHINE = 'revpro'
    _LOGIN_URL = 'https://www.revproondemand.com/login'
    _URL_BASE = 'https://www.revproondemand.com/'


class RevProSeasonIE(VHXSeasonIE):
    _PAGE_SIZE = 24
    _VALID_URL = VHXSeasonIE._VALID_URL_TEMPL % r'(?:www\.)?revproondemand\.com'
