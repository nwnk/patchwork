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

import feedparser
from django.test import TestCase
from patchwork.tests.utils import defaults, TestSeries
from patchwork.models import Series

def rss_relative_url(project):
    return "/project/%s/rss/" % project.linkname

class RssTest(TestCase):
    fixtures = ['default_states', 'default_actions']

    def setUp(self):
        series = TestSeries(n_patches=4)
        series.insert()
        all_series = Series.objects.all()
        self.assertEquals(all_series.count(), 1)
        self.series = all_series[0]

    def testNewSeries(self):
        response = self.client.get(rss_relative_url(defaults.project))
        feed = feedparser.parse(response.content)
        self.assertEqual(len(feed.entries), 1)
        entry = feed.entries[0]
        self.assertTrue(entry['title'].startswith('New:'))
        self.assertEqual(entry['patchwork_action'], 'series-new-revision')
        self.assertEqual(entry['patchwork_revision-api-url'],
                         'http://testserver/api/1.0/series/%d/revisions/1/' %
                         self.series.pk)
