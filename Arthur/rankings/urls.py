from django.conf.urls.defaults import *

urlpatterns = patterns('Arthur.rankings',
    url(r'^planets/$', 'planets.planets'),
    url(r'^planets/(?P<page>\d+)/$', 'planets.planets'),
    url(r'^planets/(?P<sort>\w+)/$', 'planets.planets'),
    url(r'^planets/(?P<sort>\w+)/(?P<page>\d+)/$', 'planets.planets'),
    url(r'^planets/(?P<race>\w+)/(?P<sort>\w+)/$', 'planets.planets'),
    url(r'^planets/(?P<race>\w+)/(?P<sort>\w+)/(?P<page>\d+)/$', 'planets.planets', name="planets"),
    url(r'^galaxy/(?P<x>\d+)[. :\-](?P<y>\d+)/$', 'galaxy.galaxy', name="galaxy"),
    url(r'^galaxies/$', 'galaxies.galaxies'),
    url(r'^galaxies/(?P<page>\d+)/$', 'galaxies.galaxies'),
    url(r'^galaxies/(?P<sort>\w+)/$', 'galaxies.galaxies'),
    url(r'^galaxies/(?P<sort>\w+)/(?P<page>\d+)/$', 'galaxies.galaxies', name="galaxies"),
    url(r'^alliance/(?P<name>\w+)/$', 'alliance.alliance'),
    url(r'^alliance/(?P<name>\w+)/(?P<page>\d+)/$', 'alliance.alliance'),
    url(r'^alliance/(?P<name>\w+)/(?P<sort>\w+)/$', 'alliance.alliance'),
    url(r'^alliance/(?P<name>\w+)/(?P<sort>\w+)/(?P<page>\d+)/$', 'alliance.alliance'),
    url(r'^alliance/(?P<name>\w+)/(?P<race>\w+)/(?P<sort>\w+)/$', 'alliance.alliance'),
    url(r'^alliance/(?P<name>\w+)/(?P<race>\w+)/(?P<sort>\w+)/(?P<page>\d+)/$', 'alliance.alliance', name="alliance"),
    url(r'^alliances/$', 'alliances.alliances'),
    url(r'^alliances/(?P<page>\d+)/$', 'alliances.alliances'),
    url(r'^alliances/(?P<sort>\w+)/$', 'alliances.alliances'),
    url(r'^alliances/(?P<sort>\w+)/(?P<page>\d+)/$', 'alliances.alliances', name="alliances"),
)
