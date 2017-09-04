# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])


VIDEOS = {'TV': [{'name': '24 Kitchen',
                       'thumb': 'http://www.24kitchen.rs/bundles/aciliacarassius/themes/kitchen/sites/all/themes/theme24kitchen/logo.png',
                       'video': 'http://109.175.6.122:4936/udp/239.0.0.29:1234',
                       'genre': 'Food'},
                      {'name': 'Nova TV',
                       'thumb': 'https://upload.wikimedia.org/wikipedia/en/4/4e/Novatv_hr.png',
                       'video': 'http://www.vidsplay.com/wp-content/uploads/2017/04/alligator.mp4',
                       'genre': 'Croatian TV'}
                      ],
            'Cars': [{'name': 'Postal Truck',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/us_postal-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/us_postal.mp4',
                      'genre': 'Cars'},
                     {'name': 'Traffic',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/traffic1-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/traffic1.mp4',
                      'genre': 'Cars'},
                     {'name': 'Traffic Arrows',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/traffic_arrows-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/traffic_arrows.mp4',
                      'genre': 'Cars'}
                     ],
            'Food': [{'name': 'Chicken',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/bbq_chicken-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/bbqchicken.mp4',
                      'genre': 'Food'},
                     {'name': 'Hamburger',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/hamburger-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/hamburger.mp4',
                      'genre': 'Food'},
                     {'name': 'Pizza',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/pizza-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/pizza.mp4',
                      'genre': 'Food'}
                     ]}
					 
TV_CHANNELS = [{'name': 'Nova TV',
                      'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/05/us_postal-screenshot.jpg',
                      'video': 'http://www.vidsplay.com/wp-content/uploads/2017/05/us_postal.mp4'
				}, 
				{'name': '24 Kitchen',
                       'thumb': 'http://www.24kitchen.rs/bundles/aciliacarassius/themes/kitchen/sites/all/themes/theme24kitchen/logo.png',
                       'video': 'http://109.175.6.122:4936/udp/239.0.0.29:1234',
                }]					 


def get_tv_channels():
	return TV_CHANNELS.iterkeys()
	
	
def my_router(paramstring):  
    params = dict(parse_qsl(paramstring))    
    if params:
        if params['action'] == 'listing':         
            list_videos(params['category'])
        elif params['action'] == 'play':        
            play_video(params['video'])
        else:          
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:       
        list_categories()	
				
def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    return VIDEOS.iterkeys()


def get_videos(category):
    return VIDEOS[category]


def list_categories():
    categories = get_categories()
    for category in categories:
        list_item = xbmcgui.ListItem(label=category)
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})     
        list_item.setInfo('video', {'title': category, 'genre': category})      
        url = get_url(action='listing', category=category)    
        is_folder = True       
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)   
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):   
    videos = get_videos(category)   
    for video in videos:     
        list_item = xbmcgui.ListItem(label=video['name'])     
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=video['video'])
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
        if params['action'] == 'listing':         
            list_videos(params['category'])
        elif params['action'] == 'play':        
            play_video(params['video'])
        else:          
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:       
        list_categories()


if __name__ == '__main__': 
    my_router(sys.argv[2][1:])
