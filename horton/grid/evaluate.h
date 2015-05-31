// Horton is a development platform for electronic structure methods.
// Copyright (C) 2011-2015 The Horton Development Team
//
// This file is part of Horton.
//
// Horton is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// Horton is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, see <http://www.gnu.org/licenses/>
//
//--

// UPDATELIBDOCTITLE: Evaluation of splines on grids

#ifndef HORTON_GRID_EVALUATE_H
#define HORTON_GRID_EVALUATE_H


#include "horton/cell.h"
#include "horton/grid/cubic_spline.h"
#include "horton/grid/uniform.h"


void eval_spline_cube(CubicSpline* spline, double* center, double* output,
                      UniformGrid* ugrid);

void eval_spline_grid(CubicSpline* spline, double* center, double* output,
                      double* points, Cell* cell, long npoint);

void eval_decomposition_grid(CubicSpline** splines, double* center,
                             double* output, double* points, Cell* cell,
                             long nspline, long npoint);
#endif
