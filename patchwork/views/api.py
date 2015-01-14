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

from django.contrib.auth.models import User
from patchwork.models import Project, Series, SeriesRevision
from rest_framework import viewsets, mixins, generics, filters, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from patchwork.serializers import ProjectSerializer, SeriesSerializer, \
                                  RevisionSerializer, UserSerializer

class MaintainerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read only for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # editable for maintainers
        user = request.user
        if not user.is_authenticated():
            return False
        return obj.project.is_editable(user)

class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # user data can be sensitive, only the user itself can access this
        # information
        return obj == request.user

class UserViewSet(viewsets.ViewSet):
    permission_classes = (UserPermission, )
    model = User

    def list(self, request):
        self = User.objects.get(pk=request.user.pk)
        serializer = UserSerializer(self)
        return Response(serializer.data)

class SeriesListMixin:
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    paginate_by = 20
    paginate_by_param = 'perpage'
    max_paginate_by = 100
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('name', 'n_patches', 'submitter__name', 'reviewer__name',
                        'submitted', 'last_updated')

class SeriesReviewsViewSet(mixins.ListModelMixin,
                           SeriesListMixin,
                           viewsets.GenericViewSet):
    permission_classes = (UserPermission, )

    def get_queryset(self):
        filter_kwargs = { 'reviewer': self.request.user }

        # Ensure queryset is re-evaluated on each request.
        queryset = self.queryset.filter(**filter_kwargs)
        return queryset

class ProjectViewSet(viewsets.ViewSet):
    permission_classes = (MaintainerPermission, )
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
                        SeriesListMixin,
                        viewsets.GenericViewSet):
    permission_classes = (MaintainerPermission, )

    def get_queryset(self):
        filter_kwargs = { 'project__linkname': self.kwargs['project_pk'] }

        # Ensure queryset is re-evaluated on each request.
        queryset = self.queryset.filter(**filter_kwargs)
        return queryset

class SeriesViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (MaintainerPermission, )
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

class RevisionViewSet(viewsets.ViewSet):
    permission_classes = (MaintainerPermission, )
    model = SeriesRevision

    def retrieve(self, request, series_pk=None, pk=None):
        rev = get_object_or_404(SeriesRevision, series=series_pk, version=pk)
        serializer = RevisionSerializer(rev)
        return Response(serializer.data)
