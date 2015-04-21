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

from datetime import datetime
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Max, Min
from arches.app.models import models
from arches.app.views.search import get_paginator
from arches.app.views.search import build_search_results_dsl as build_base_search_results_dsl
from arches.app.models.concept import Concept
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.search.search_engine_factory import SearchEngineFactory
from arches.app.search.elasticsearch_dsl_builder import Bool, Match, Query, Nested, Terms, GeoShape, Range
from django.utils.translation import ugettext as _

def home_page(request):
    lang = request.GET.get('lang', settings.LANGUAGE_CODE)
    min_max_dates = models.Dates.objects.aggregate(Min('val'), Max('val'))

    data = {
        'important_dates': {
            'branch_lists': [],
            'domains': {
                'important_dates' : Concept().get_e55_domain('BEGINNING_OF_EXISTENCE_TYPE.E55') + Concept().get_e55_domain('END_OF_EXISTENCE_TYPE.E55'),
                'date_operators' : [{
                    "conceptid": "0",
                    "entitytypeid": "DATE_COMPARISON_OPERATOR.E55",
                    "id": "0",
                    "language,id": settings.LANGUAGE_CODE,
                    "text": _("Before"),
                    "valuetype": "prefLabel",  
                    "sortorder": "",
                    "collector": "",
                    "children": []
                },{
                    "conceptid": "1",
                    "entitytypeid": "DATE_COMPARISON_OPERATOR.E55",
                    "id": "1",
                    "language,id": settings.LANGUAGE_CODE,
                    "text": _("On"),
                    "valuetype": "prefLabel",  
                    "sortorder": "",
                    "collector": "",
                    "children": []
                },{
                    "conceptid": "2",
                    "entitytypeid": "DATE_COMPARISON_OPERATOR.E55",
                    "id": "2",
                    "language,id": settings.LANGUAGE_CODE,
                    "text": _("After"),
                    "valuetype": "prefLabel",  
                    "sortorder": "",
                    "collector": "",
                    "children": []
                }]
            }
        }
    }

    return render_to_response('search.htm', {
            'main_script': 'search',
            'active_page': 'Search',
            'min_date': min_max_dates['val__min'].year if min_max_dates['val__min'] != None else 0,
            'max_date': min_max_dates['val__max'].year if min_max_dates['val__min'] != None else 1,
            'timefilterdata': JSONSerializer().serialize(data)
        }, 
        context_instance=RequestContext(request))

def search_results(request):
    query = build_search_results_dsl(request)
    results = query.search(index='entity', doc_type='') 
    total = results['hits']['total']
    page = 1 if request.GET.get('page') == '' else int(request.GET.get('page', 1))

    all_entity_ids = ['_all']
    if request.GET.get('include_ids', 'false') == 'false':
        all_entity_ids = ['_none']
    elif request.GET.get('no_filters', '') == '':
        full_results = query.search(index='entity', doc_type='', start=0, limit=1000000, fields=[])
        all_entity_ids = [hit['_id'] for hit in full_results['hits']['hits']]

    return get_paginator(results, total, page, settings.SEARCH_ITEMS_PER_PAGE, all_entity_ids)

def build_search_results_dsl(request):
    temporal_filters = JSONDeserializer().deserialize(request.GET.get('temporalFilter', None))

    query = build_base_search_results_dsl(request)  
    boolfilter = Bool()

    if 'filters' in temporal_filters:
        for temporal_filter in temporal_filters['filters']:
            terms = Terms(field='date_groups.conceptid', terms=temporal_filter['date_types__value'])
            boolfilter.must(terms)

            date_value = datetime.strptime(temporal_filter['date'], '%d/%m/%Y').isoformat()

            if temporal_filter['date_operators__value'] == '1': # equals query
                range = Range(field='date_groups.value', gte=date_value, lte=date_value)
            elif temporal_filter['date_operators__value'] == '0': # greater than query 
                range = Range(field='date_groups.value', lt=date_value)
            elif temporal_filter['date_operators__value'] == '2': # less than query
                range = Range(field='date_groups.value', gt=date_value)

            if 'inverted' not in temporal_filters:
                temporal_filters['inverted'] = False

            if temporal_filters['inverted']:
                boolfilter.must_not(range)
            else:
                boolfilter.must(range)

            query.add_filter(boolfilter)

    return query