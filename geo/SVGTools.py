#	geo - Simple Python-native geometry library.
#	Copyright (C) 2020-2020 Johannes Bauer
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

import re
import math
from .TransformationMatrix import TransformationMatrix
from .Vector2d import Vector2d

class SVGTools():
	_OPERATION_RE = re.compile(r"[ \t\n]*(?P<op>[A-Za-z]+)\(\s*(?P<args>[^\)]+)\)(?P<remainder>.*)", flags = re.MULTILINE | re.DOTALL)
	_ARG_SPLIT_RE = re.compile(r"[, \t\n]+")

	@classmethod
	def parse_transform(cls, transform_string):
		matrices = [ ]
		while True:
			match = cls._OPERATION_RE.fullmatch(transform_string)
			if match is None:
				if transform_string.strip("\t\n ") != "":
					raise ValueError("Unparsable trailing data in SVG transformation string: %s" % (transform_string))
				break
			match = match.groupdict()
			args = cls._ARG_SPLIT_RE.split(match["args"].strip("\n\t "))
			args = [ float(arg) for arg in args ]
			if (match["op"] == "matrix") and len(args) == 6:
				matrices.append(TransformationMatrix(*args))
			elif (match["op"] == "translate") and len(args) == 2:
				matrices.append(TransformationMatrix.translate(Vector2d(*args)))
			elif (match["op"] == "scale") and len(args) == 2:
				(scale_x, scale_y) = args
				matrices.append(TransformationMatrix(scale_x, 0, 0, scale_y, 0, 0))
			elif (match["op"] == "rotate") and len(args) == 1:
				phi = args[0] / 180 * math.pi
				matrices.append(TransformationMatrix.rotate(-phi))
			elif (match["op"] == "rotate") and len(args) == 3:
				phi = args[0] / 180 * math.pi
				cor = Vector2d(args[1], args[2])
				matrices.append(TransformationMatrix.rotate(-phi, cor = cor))
			elif (match["op"] == "skewX") and len(args) == 1:
				phi = args[0] / 180 * math.pi
				matrices.append(TransformationMatrix(1, 0, math.tan(phi), 1, 0, 0))
			elif (match["op"] == "skewY") and len(args) == 1:
				phi = args[0] / 180 * math.pi
				matrices.append(TransformationMatrix(1, math.tan(phi), 0, 1, 0, 0))
			else:
				raise ValueError("Unable to find match for: %s" % (str(match)))
			transform_string = match["remainder"]

		matrix = TransformationMatrix.identity()
		for transform in reversed(matrices):
			matrix *= transform
		return matrix
