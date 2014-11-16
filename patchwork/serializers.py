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
from rest_framework import serializers

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
