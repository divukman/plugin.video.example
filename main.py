# -*- coding: utf-8 -*-
# Module: default
# Author: Dimitar Vukman
# Created on: 04SEP2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html


import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin

_url = sys.argv[0]
_handle = int(sys.argv[1])

					 
TV_CHANNELS = [{	
					'name': 'Nova TV',
                     'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/us_postal-screenshot.jpg',
                     'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/us_postal.mp4',
					 'genre': 'TV'
				}, 
				{
					'name': '24 Kitchen',
                    'thumb': 'http://www.24kitchen.rs/bundles/aciliacarassius/themes/kitchen/sites/all/themes/theme24kitchen/logo.png',
					'video': 'http://109.175.6.122:4936/udp/239.0.0.29:1234',
					'genre': 'Food'
                }]					 

def get_tv_channels():
	return TV_CHANNELS
				
				
def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def list_tv_channels():   
    tv_channels = get_tv_channels()   
    for tv_channel in tv_channels:     
        list_item = xbmcgui.ListItem(label=tv_channel['name'])     
        list_item.setInfo('video', {'title': tv_channel['name'], 'genre': tv_channel['genre']})
        list_item.setArt({'thumb': tv_channel['thumb'], 'icon': tv_channel['thumb'], 'fanart': tv_channel['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=tv_channel['video'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)   
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)    
    xbmcplugin.endOfDirectory(_handle)


def play_video(path): 
    play_item = xbmcgui.ListItem(path=path)    
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):  
    params = dict(parse_qsl(paramstring))    
    if params:
        if params['action'] == 'play':        
            play_video(params['video'])
        else:          
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:       
        list_tv_channels()

		
if __name__ == '__main__': 
    router(sys.argv[2][1:])
