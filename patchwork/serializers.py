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
from patchwork.models import Project, Series, SeriesRevision, Patch
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', )

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'linkname', 'listemail', 'web_url', 'scm_url',
                  'webscm_url')

class SeriesSerializer(serializers.ModelSerializer):
    submitter__name = serializers.CharField(source='submitter.name',
                                            read_only=True)
    reviewer__name = serializers.CharField(source='reviewer.name',
                                           read_only=True)

    class Meta:
        model = Series
        fields = ('id', 'name', 'n_patches', 'submitter', 'submitter__name',
                  'submitted', 'last_updated', 'version', 'reviewer',
                  'reviewer__name')
        read_only_fields = ('n_patches', 'submitter', 'submitted',
                            'last_updated', 'version')

class PatchSerializer(serializers.ModelSerializer):
    submitter__name = serializers.CharField(source='submitter.name',
                                            read_only=True)
    state__name = serializers.CharField(source='state.name', read_only=True)
    class Meta:
        model = Patch
        fields = ('name', 'msgid', 'date', 'submitter', 'submitter__name',
                  'state', 'state__name', 'archived', 'content')
        read_only_fields = ('name', 'msgid', 'date', 'submitter', 'archived',
                            'content')


class RevisionSerializer(serializers.HyperlinkedModelSerializer):
    patches = PatchSerializer(many=True, read_only=True)

    class Meta:
        model = SeriesRevision
        fields = ('version', 'cover_letter', 'patches')
        read_only_fields = ('version', 'cover_letter')
