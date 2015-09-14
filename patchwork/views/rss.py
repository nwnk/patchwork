# Patchwork - automated patch tracking system
# Copyright (C) 2015 Intel Corporation
#
# This file is part of the Patchwork package.
#
# Patchwork is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Patchwork is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Patchwork; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import urlparse

from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from patchwork.models import Project, SeriesLog


class RSSFeed(Feed):
    actions = {
        'series-new': {
            'title': 'New',
            'description': '<p>%(submitter)s posted a new series: ' \
                           '<a href="%(series_url)s">%(series_title)s</a></p>'
        },
        'series-new-revision': {
            'title': 'Update',
            'description': '<p>%(submitter)s updated: ' \
                           '<a href="%(series_url)s">%(series_title)s</a></p>'
        },
    }

    def get_object(self, request, project_id):
        self._base_url = request.build_absolute_uri('/')
        return get_object_or_404(Project, linkname=project_id)

    def _url(self, path):
        return urlparse.urljoin(self._base_url, path)

    def title(self, project):
        return "Patchwork RSS feed for %s" % project.name

    def link(self, project):
        return reverse('patchwork.views.project.project',
                       kwargs={ 'project_id': project.linkname })

    def description(self, project):
        return "Follow %s development through a bespoke, locally crafted " \
               "RSS feed!" % project.name

    def items(self, project):
        return SeriesLog.objects.filter(series__project=project) \
               .order_by('-action_time')[:25]

    def _refine_action(self, item):
        action = item.action.name
        if action == 'series-new-revision' and item.series.version == 1:
            action = 'series-new'
        return action

    def item_title(self, item):
        action = self._refine_action(item)
        return "%s: %s" % (self.actions[action]['title'], item.series.name)

    def item_description(self, item):
        action = self._refine_action(item)
        return self.actions[action]['description'] % {
            'submitter': item.series.submitter,
            'series_url': self.item_link(item),
            'series_title': item.series.name,
        }

    def item_link(self, item):
        return self._url(item.series.get_absolute_url())

    def item_pubdate(self, item):
        return item.action_time
