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

#> x := Matrix([[a,b,0],[c,d,0],[e,f,1]]);
#                                                                                   [a    b    0]
#                                                                                   [           ]
#                                                                              x := [c    d    0]
#                                                                                   [           ]
#                                                                                   [e    f    1]
#
#> y := Matrix([[a_,b_,0],[c_,d_,0],[e_,f_,1]]);
#                                                                                  [a_    b_    0]
#                                                                                  [             ]
#                                                                             y := [c_    d_    0]
#                                                                                  [             ]
#                                                                                  [e_    f_    1]
#
#> evalm(x&*y);
#                                                                 [  a a_ + b c_         a b_ + b d_       0]
#                                                                 [                                         ]
#                                                                 [  c a_ + d c_         c b_ + d d_       0]
#                                                                 [                                         ]
#                                                                 [e a_ + f c_ + e_    e b_ + f d_ + f_    1]

from math import sin, cos
from .Vector2d import Vector2d

class TransformationMatrix(object):
	def __init__(self, a, b, c, d, e, f):
		self._a = a
		self._b = b
		self._c = c
		self._d = d
		self._e = e
		self._f = f

	@property
	def a(self):
		return self._a

	@property
	def b(self):
		return self._b

	@property
	def c(self):
		return self._c

	@property
	def d(self):
		return self._d

	@property
	def e(self):
		return self._e

	@property
	def f(self):
		return self._f

	@property
	def aslist(self):
		return [ self.a, self.b, self.c, self.d, self.e, self.f ]

	def transform(self, vec2d):
		return Vector2d(
			self.a * vec2d.x + self.c * vec2d.y + self.e,
			self.b * vec2d.x + self.d * vec2d.y + self.f,
		)

	def __eq__(self, other):
		abs_diff_sum = sum(abs(x - y) for (x, y) in zip(self.aslist, other.aslist))
		return abs_diff_sum < 1e-6

	def __mul__(self, other):
		return TransformationMatrix(
			self.a * other.a + self.b * other.c,
			self.a * other.b + self.b * other.d,
			self.c * other.a + self.d * other.c,
			self.c * other.b + self.d * other.d,
			self.e * other.a + self.f * other.c + other.e,
			self.e * other.b + self.f * other.d + other.f,
		)

	@property
	def is_identity(self):
		return self == self.identity()

	@classmethod
	def identity(cls):
		return cls.scale(1)

	@classmethod
	def scale(cls, scale_factor):
		return cls(scale_factor, 0, 0, scale_factor, 0, 0)

	@classmethod
	def translate(cls, vec2d):
		return cls(1, 0, 0, 1, vec2d.x, vec2d.y)

	@classmethod
	def rotate(cls, phi, cor = None):
		if cor is None:
			# No center of rotation given, rotate around origin
			return cls(cos(phi), -sin(phi), sin(phi), cos(phi), 0, 0)
		else:
			return cls.translate(-cor) * cls.rotate(phi) * cls.translate(cor)

	def __repr__(self):
		return str(self)

	@staticmethod
	def _float_format(value):
		value = "%.3f" % (value)
		if value.endswith(".000"):
			value = value[:-4]
		return value

	def __str__(self):
		if self.is_identity:
			values = "identity"
		else:
			values = (self.a, self.b, self.c, self.d, self.e, self.f)
			values = ", ".join(self._float_format(value) for value in values)
		return "Matrix<%s>" % (values)
