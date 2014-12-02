# Patchwork - automated patch tracking system
# Copyright (C) 2014 Intel Corporation
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

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from patchwork.models import Project, Series, SeriesRevision

class SeriesListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'patchwork/series-list.html', {
            'project': get_object_or_404(Project, linkname=kwargs['project']),
        })

class SeriesView(View):
    def get(self, request, *args, **kwargs):
        series = get_object_or_404(Series, pk=kwargs['series'])
        revision = get_object_or_404(SeriesRevision,
                                     series=series,
                                     version=series.version)
        return render(request, 'patchwork/series.html', {
            'series': series,
            'project': series.project,
            'cover_letter': revision.cover_letter,
            'patches': revision.patches.all(),
        })
