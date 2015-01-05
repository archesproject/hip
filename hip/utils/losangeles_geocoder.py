'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from django.conf import settings
import urllib
import urllib2
import json

def find_candidates(search_string):
    query_args = { 'searchText': search_string }
    encoded_args = urllib.urlencode(query_args)

    url = 'http://egis3.lacounty.gov/Geocortex/Essentials/Essentials/REST/sites/GISViewer/search?layers=&envelope=&maxResults=&contains=false&returnCountOnly=false&returnGeometry=true&returnHighlights=false&returnIdsOnly=false&f=pjson&' + encoded_args
    response = json.loads(urllib2.urlopen(url).read())
    results = []
    for feature in response['features']:
        results.append({
            'id': feature['id'],
            'text': feature['attributes']['SitusFullAddress'] + ' (APN: ' + feature['attributes']['APN'] + ')',
            'geometry': {
                "type": "Polygon",
                "coordinates": feature['geometry']['rings']
            },
            'score': feature['score']
        })
        
    return results
