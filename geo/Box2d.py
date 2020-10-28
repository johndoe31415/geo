#	geo - Simple Python-native geometry library.
#	Copyright (C) 2016-2020 Johannes Bauer
#
#	This file is part of geo.
#
#	geo is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	geo is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with geo; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>
#

from .Vector2d import Vector2d

class Box2d(object):
	def __init__(self, base, dimensions):
		self._base = base
		self._dimensions = dimensions

	@classmethod
	def create_from_edges(cls, v0, v1):
		base = Vector2d(min(v0.x, v1.x), min(v0.y, v1.y))
		dimensions = abs(v1 - v0)
		return cls(base = base, dimensions = dimensions)

	@property
	def base(self):
		return self._base

	@property
	def dimensions(self):
		return self._dimensions

	@property
	def v0(self):
		return self._base

	@property
	def v1(self):
		return self._base + self._dimensions

	@property
	def center(self):
		return self.v0 + (self._dimensions / 2)

	def transform(self, matrix):
		v0t = matrix.transform(self.v0)
		v1t = matrix.transform(self.v1)
		return self.create_from_edges(v0t, v1t)

	def __iter__(self):
		yield self._base
		yield self._base + Vector2d(self._dimensions.x, 0)
		yield self._base + self._dimensions
		yield self._base + Vector2d(0, self._dimensions.y)

	def __repr__(self):
		return "Box<base %s, dim %s>" % (self.base, self.dimensions)
