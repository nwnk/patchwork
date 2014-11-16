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

from patchwork.models import Project, Series
from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from patchwork.serializers import ProjectSerializer, SeriesSerializer

class ProjectViewSet(viewsets.ViewSet):
    model = Project

    def list(self, request):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Project.objects.get(name=pk)
        serializer = ProjectSerializer(queryset)
        return Response(serializer.data)

class SeriesListViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    paginate_by = 20
    paginate_by_param = 'perpage'
    max_paginate_by = 100

    def get_queryset(self):
        filter_kwargs = { 'project__linkname': self.kwargs['project_pk'] }

        # Ensure queryset is re-evaluated on each request.
        queryset = self.queryset.filter(**filter_kwargs)
        return queryset
