import sys, os, xbmcaddon
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'site-packages'))

from traktorbeam import log, sync
from traktorbeam.helpers import selectAction

selectAction('TraktorBeam',[
    ('Sync trakt.tv new episodes now',sync.trakt_syncEpisodes),
    ('Sync trakt.tv watchlist now',sync.trakt_syncWatchlist),
    ('Sync IMDb watchlist now',sync.imdb_syncWatchlist),
    ('Add IMDb user list',sync.imdb_syncUserList),
    ('TraktorBeam settings',xbmcaddon.Addon().openSettings),
])