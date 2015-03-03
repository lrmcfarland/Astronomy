#!/usr/bin/env python

"""Transforms coordinates to/from Ecliptic, Equatorial


ASSUMES: The x-axis points to vernal equinox. Positive rotations are right hand rule,
Y x Z = X, i.e. counter clockwise looking down X.


References:

Celestial Coordinate System
    http://en.wikipedia.org/wiki/Celestial_coordinate_system#Transformation_of_coordinates
    http://en.wikipedia.org/wiki/Celestial_coordinate_system#Equatorial_.E2.86.90.E2.86.92_horizontal
    http://aa.usno.navy.mil/publications/docs/Circular_163.pdf

Equatorial Coordinate System
    http://en.wikipedia.org/wiki/Equatorial_coordinate_system

Ecliptic Coordinate System
    http://en.wikipedia.org/wiki/Ecliptic
    http://en.wikipedia.org/wiki/Ecliptic_coordinate_system
    http://en.wikipedia.org/wiki/Axial_tilt

Validation:
    http://lambda.gsfc.nasa.gov/toolbox/tb_coordconv.cfm

"""

import math
import coords

import GMST
import utils


class Error(Exception):
    pass


# x axis points to vernal equinox (the first point of Aries in this epoch)
equinox_axis = coords.rotator(coords.Ux)

# obliquity of the ecliptic terms are from http://en.wikipedia.org/wiki/Axial_tilt
obe = list()
obe.append(coords.angle(23, 26, 21.45))
obe.append(coords.angle(-1)*coords.angle(0, 0, 46.815)) # TODO no unary minus in boost wrappers
obe.append(coords.angle(-1)*coords.angle(0, 0, 0.0006))
obe.append(coords.angle(0, 0, 0.00181))
# TODO more terms, updated



def eps(a_datetime):
    """Calculates the obliquity of the ecliptic given the datetime"""
    T = utils.JulianCentury(a_datetime)
    the_eps = 0
    for i in xrange(len(obe)):
        the_eps += obe[i].value * math.pow(T, i)
    return the_eps


def _xform(an_object, a_datetime, a_direction):
    """Transforms a vector to/from equatorial/ecliptic coordinates.

    Args:
    an_object: the vector to transform. May be Cartesian or spherical.
    a_datetime: the time of the transformation
    a_direction: +1 to equatorial, -1 to ecliptic

    Returns a vector in the transformed coordinates
    """

    if not isinstance(an_object, coords.spherical):
        raise Error('object must be in spherical coordinates')

    the_rotatee = coords.Cartesian(an_object)

    the_rotated = equinox_axis.rotate(the_rotatee, coords.angle(a_direction * eps(a_datetime)))

    if isinstance(an_object, coords.spherical):
        return coords.spherical(the_rotated)
    else:
        return the_rotated


def toEcliptic(an_object, a_datetime):
    """Transforms an_object from equatorial to ecliptic coordinates

    Returns a Cartesian vector in eliptic coordinates
    """
    return _xform(an_object, a_datetime, -1.0)


def toEquatorial(an_object, a_datetime):
    """Transforms an_object from ecliptic to equatorial coordinates

    Returns a Cartesian vector in equatorial coordinates
    """
    return _xform(an_object, a_datetime, 1.0)


# ================
# ===== main =====
# ================


if __name__ == '__main__':

    # -------------------------
    # ----- parse options -----
    # -------------------------

    import optparse

    defaults = {'toEcliptic' : False}

    usage = '%prog [options] <RA as deg:min:sec> <dec as deg:min:sec> <a datetime>'

    parser = optparse.OptionParser(usage=usage)

    parser.add_option('--toEcliptic',
                      action='store_true', dest='toEcliptic',
                      default=defaults['toEcliptic'],
                      help='to ecliptic [%default]')

    options, args = parser.parse_args()

    # ----- validate -----

    if len(args) < 3:
        parser.error('missing object and/or datetime.')

    RA = utils.parse_angle_arg(args[0])
    dec = utils.parse_angle_arg(args[1])

    an_object = utils.radec2spherical(a_right_ascension=RA, a_declination=dec)

    a_datetime = coords.datetime(args[2])

    # TODO validate toEcliptic/toEquatorial option logic

    # ---------------------
    # ----- transform -----
    # ---------------------

    if options.toEcliptic == True:
        result = toEcliptic(an_object, a_datetime)

    else:
        result = toEquatorial(an_object, a_datetime)


    print result

    # TODO add print options for output in RA and Dec