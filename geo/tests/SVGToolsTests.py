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

import unittest
from ..SVGTools import SVGTools
from .. import Vector2d, TransformationMatrix

class SVGToolsTests(unittest.TestCase):
	def assertMatrixEqual(self, m1, m2, places = 7):
		self.assertAlmostEqual(m1.a, m2.a, places = places)
		self.assertAlmostEqual(m1.b, m2.b, places = places)
		self.assertAlmostEqual(m1.c, m2.c, places = places)
		self.assertAlmostEqual(m1.d, m2.d, places = places)
		self.assertAlmostEqual(m1.e, m2.e, places = places)
		self.assertAlmostEqual(m1.f, m2.f, places = places)

	def test_matrix(self):
		self.assertEqual(SVGTools.parse_transform("matrix(1,0,0,1,0,0)"), TransformationMatrix.identity())
		self.assertEqual(SVGTools.parse_transform("""matrix(1,    0,		0,1 ,0
						,
			0   )"""), TransformationMatrix.identity())

	def test_translate(self):
		m = SVGTools.parse_transform("translate(123,-456)")
		self.assertMatrixEqual(m, TransformationMatrix(1, 0, 0, 1, 123, -456), places = 3)

	def test_rotate1(self):
		m = SVGTools.parse_transform("rotate(-10)")
		self.assertMatrixEqual(m, TransformationMatrix(0.985, -0.17364818, 0.17364818, 0.98480775, 0, 0), places = 3)

	def test_rotate3(self):
		m = SVGTools.parse_transform("rotate(-10 123 456)")
		self.assertMatrixEqual(m, TransformationMatrix(0.985, -0.174, 0.174, 0.985, -77.315, 28.286), places = 3)

	def test_skewX(self):
		m = SVGTools.parse_transform("skewX(123)")
		self.assertMatrixEqual(m, TransformationMatrix(1, 0, -1.540, 1, 0, 0), places = 3)

	def test_skewY(self):
		m = SVGTools.parse_transform("skewY(1.234)")
		self.assertMatrixEqual(m, TransformationMatrix(1, 0.022, 0, 1, 0, 0), places = 3)

	def test_scale(self):
		m = SVGTools.parse_transform("scale(2 3)")
		self.assertMatrixEqual(m, TransformationMatrix(2, 0, 0, 3, 0, 0), places = 3)

	def test_mdn(self):
		m = SVGTools.parse_transform("""
			rotate(-10 50 100)
		""")
		self.assertMatrixEqual(m, TransformationMatrix(0.985, -0.174, 0.174, 0.985, -16.605, 10.202), places = 3)

		m = SVGTools.parse_transform("""
			rotate(-10 50 100)
			translate(-36 45.5)
		""")
		self.assertMatrixEqual(m, TransformationMatrix(0.985, -0.174, 0.174, 0.985, -44.157, 61.262), places = 3)

		m = SVGTools.parse_transform("""
			rotate(-10 50 100)
			translate(-36 45.5)
			skewX(40)
			scale(1 0.5)
		""")
		self.assertMatrixEqual(m, TransformationMatrix(0.98480775, -0.17364818, 0.5, 0.41954982, -44.157292, 61.261721), places = 6)
