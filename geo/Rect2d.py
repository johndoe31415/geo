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

class Rect2d(object):
	def __init__(self, v1, v2, v3, v4):
		self._v1 = v1
		self._v2 = v2
		self._v3 = v3
		self._v4 = v4

	@classmethod
	def basic(cls, base, width, height):
		return cls(base, base + Vector2d(width, 0), base + Vector2d(width, height), base + Vector2d(0, height))

	@property
	def v1(self):
		return self._v1

	@property
	def v2(self):
		return self._v2

	@property
	def v3(self):
		return self._v3

	@property
	def v4(self):
		return self._v4

	@property
	def center(self):
		return (self.v1 + self.v3) / 2

	def __getitem__(self, index):
		if index == 0:
			return self.v1
		elif index == 1:
			return self.v2
		if index == 2:
			return self.v3
		elif index == 3:
			return self.v4
		else:
			raise KeyError("Unsupported point index")

	def transform(self, matrix):
		return Rect2d(matrix.transform(self.v1), matrix.transform(self.v2), matrix.transform(self.v3), matrix.transform(self.v4))

	def __iter__(self):
		yield self.v1
		yield self.v2
		yield self.v3
		yield self.v4

	def __repr__(self):
		return "Rect<%s, %s, %s, %s>" % (self.v1, self.v2, self.v3, self.v4)
