# Patchwork - automated patch tracking system
# Copyright (C) 2008 Jeremy Kerr <jk@ozlabs.org>
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

from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='patch_tags')
def patch_tags(patch, tag):
    count = getattr(patch, tag.attr_name)
    count_str = str(count) if count else ''
    class_str = "tag-%s" % tag.abbrev if count else ''
    title = '%d %s' % (count, tag.name)
    return mark_safe('<td class="%s"><span title="%s">%s</span></td>' %
                     (class_str, title, count_str))


@register.filter
@stringfilter
def msgid(patch):
    return patch.strip('<>')
