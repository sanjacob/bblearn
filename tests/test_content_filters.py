"""BlackboardSync Tests"""

# Copyright (C) 2023, Jacob Sánchez Pérez

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import pytest
from collections import namedtuple
from blackboard.filters import BWFilter


@pytest.mark.parametrize(
    ('items', 'whitelist', 'expected'),
    (
        (['a', 'b', 'c', 'd'], ['a', 'b'], ['a', 'b']),
        (['a', 'b', 'c', 'd'], ['a', 'b', 'x', 'y'], ['a', 'b']),
        (['a', 'b', 'c', 'd'], ['x'], []),
        (['a', 'b', 'c', 'd'], ['a'], ['a']),
        (['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']),
    )
)
def test_bwfilter_whitelist(items, whitelist, expected):
    f = BWFilter(whitelist=whitelist)
    assert list(f.filter(None, items)) == expected

@pytest.mark.parametrize(
    ('items', 'blacklist', 'expected'),
    (
        (['a', 'b', 'c', 'd'], ['a', 'b'], ['c', 'd']),
        (['a', 'b', 'c', 'd'], ['a', 'b', 'x', 'y'], ['c', 'd']),
        (['a', 'b', 'c', 'd'], ['x'], ['a', 'b', 'c', 'd']),
        (['a', 'b', 'c', 'd'], ['a'], ['b', 'c', 'd']),
        (['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], []),
    )
)
def test_bwfilter_blacklist(items, blacklist, expected):
    f = BWFilter(blacklist=blacklist)
    assert list(f.filter(None, items)) == expected

P = namedtuple('P', ['x'])

@pytest.mark.parametrize(
    ('items', 'whitelist', 'expected'),
    (
        ([P('a'), P('b'), P('c')], ['a'], [P('a')]),
        ([P('a'), P('b'), P('c')], ['x'], []),
        ([P('a'), P('b'), P('c')], ['a', 'b', 'c', 'd'], [P('a'), P('b'), P('c')]),
    )
)
def test_bwfilter_whitelist_attr(items, whitelist, expected):
    f = BWFilter(whitelist=whitelist)
    assert list(f.filter(lambda p: p.x, items)) == expected

@pytest.mark.parametrize(
    ('items', 'blacklist', 'expected'),
    (
        ([P('a'), P('b'), P('c')], ['a'], [P('b'), P('c')]),
        ([P('a'), P('b'), P('c')], ['x'], [P('a'), P('b'), P('c')]),
        ([P('a'), P('b'), P('c')], ['a', 'b', 'c', 'd'], []),
    )
)
def test_bwfilter_blacklist_attr(items, blacklist, expected):
    f = BWFilter(blacklist=blacklist)
    assert list(f.filter(lambda p: p.x, items)) == expected

@pytest.mark.parametrize(
    ('items', 'whitelist', 'blacklist', 'expected'),
    (
        (['a', 'b', 'c'], ['a'], ['b', 'c'], ['a']),
        (['a', 'b', 'c'], ['x'], ['a'], []),
        (['a', 'b', 'c'], ['a', 'b', 'c', 'd'], ['c'], ['a', 'b', 'c']),
    )
)
def test_bwfilter_bothlists(items, whitelist, blacklist, expected):
    f = BWFilter(blacklist=blacklist, whitelist=whitelist)
    assert list(f.filter(None, items)) == expected
