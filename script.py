import sys, os, urllib
import xbmc, xbmcgui,re, xbmcplugin, xbmcaddon
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'site-packages'))

from traktorbeam import log, sync

__addon__       = xbmcaddon.Addon()
__addondir__    = __addon__.getAddonInfo('path')

traktAddon = xbmcaddon.Addon('script.trakt')
sys.path.insert(0, traktAddon.getAddonInfo('path'))

# from trakt import Trakt
# from traktapi import traktAPI as traktAPI_super

# class traktAPI(traktAPI_super):

#     def __init__(self):
#         traktAPI_super.__init__(self)

#     def getCalendar(self):
#         with Trakt.configuration.oauth.from_response(self.authorization):
#             with Trakt.configuration.http(retry=True, timeout=90):
#                 Trakt.client.http.configure('calendar')
#                 response = Trakt.client.http.get('my/shows')
#                 log.info(response.json())
#         return


# trakt = traktAPI()

# trakt.getCalendar()

# log.info(trakt)

def parseArgs():
    args = {
        'action': None
    }
    if 2 < len(sys.argv):
        split = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for part in split:
            splitsplit = part.split('=')
            args[splitsplit[0]] = urllib.unquote_plus(splitsplit[1])

    return args

def add_shows():
    #name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url
    #plugin://plugin.video.pulsar/show/275557/season/2/episode/10/links
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.genesis/?action=play&tvdb=94571&season=6&episode=1&show=Community)')
    # log.info("add shows")
def add_movies():
    log.info("add movies")

def getTorrents(args):
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.pulsar/%(type)s/%(id)s/season/%(season)s/episode/%(episode)s/links)' % args, True)

def getStreams(args):
    xbmc.executebuiltin('RunPlugin(plugin://plugin.video.genesis/?action=play&tvdb=%(id)s&season=%(season)s&episode=%(episode)s&show=%(title)s)' % args, True)

actions = [
    'Torrents',
    'Streams'
]

methods = {
    0: getTorrents,
    1: getStreams
}

menuActions = [
    'Sync trakt.tv new episodes now',
    'Sync trakt.tv watchlist now',
    'Add trakt.tv TV show collection',
    'Add trakt.tv movie collection',
    'Sync IMDb watchlist now',
    'Add IMDb user list'
    ]

menuMethods = {
    0: sync.trakt_syncEpisodes,
    1: sync.trakt_syncWatchlist,
    2: add_shows,
    3: add_movies,
    4: sync.imdb_syncWatchlist,
    5: sync.imdb_syncUserList
}

#user = settings.settings.getSetting('user')
#password = settings.settings.getSetting('password')

args = parseArgs()

if 'type' in args:
    ret = xbmcgui.Dialog().select('TraktorBeam', actions + ['Cancel'])
    if ret in methods:
        methods.get(ret)(args)
        xbmcplugin.addDirectoryItems(int(sys.argv[1]), range(0), totalItems=0)
        xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True, updateListing=False, cacheToDisc=True)
    else:
        log.info("action cancelled")

else:

    ret = xbmcgui.Dialog().select('TraktorBeam', menuActions + ['Cancel'])

    if ret in menuMethods:
        menuMethods.get(ret)()
    else:
        log.info("action cancelled")
