from .imggaming import ImgGamingBaseIE


class TNAWrestlingIE(ImgGamingBaseIE):
    _VALID_URL = ImgGamingBaseIE._VALID_URL_TEMPL % r'watch\.tnawrestling\.com'
    _NETRC_MACHINE = 'tnawrestling'
    _REALM = 'impactplus'
