"""Unit tests for Right Ascension, declination, Ecliptic and Equatorial transforms

to run:  ./pylaunch.sh test_EclipticEquatorial.py
verbose: ./pylaunch.sh test_EclipticEquatorial.py -v
filter:  ./pylaunch.sh test_EclipticEquatorial.py EclipticEquatorialTests.test_lat_0_long_15
debug:   ./pylaunch.sh -m pdb test_EclipticEquatorial.py EclipticEquatorialTests.test_lat_0_long_15

(Pdb) n # until import

(Pdb) n
> /Users/lrm/src/Astronomy/Transforms/test_EclipticEquatorial.py(17)<module>()
-> import EclipticEquatorial
(Pdb) n
> /Users/lrm/src/Astronomy/Transforms/test_EclipticEquatorial.py(18)<module>()
-> import utils

(Pdb) b EclipticEquatorial.EclipticEquatorial._xform
Breakpoint 1 at /Users/lrm/src/Astronomy/Transforms/EclipticEquatorial.py:76
(Pdb) c
> /Users/lrm/src/Astronomy/Transforms/EclipticEquatorial.py(88)_xform()
-> if isinstance(an_object, coords.spherical):

"""

import math
import time
import unittest

import coords
import EclipticEquatorial
import utils

class EclipticEquatorialTests(unittest.TestCase):
    """Test ecliptic equatorial coordinate transformations

    Validated against http://lambda.gsfc.nasa.gov/toolbox/tb_coordconv.cfm
    """

    def setUp(self):
        """Set up test parameters."""

        self.places = 5 # precision limited by LAMBDA-tools reporting


    def test_first_point_of_Aries(self):
        """Test J2000 first point of Aries"""

        j2000 = coords.datetime('2000-01-01T00:00:00')
        an_object = coords.spherical(coords.Ux)

        an_object_ec = EclipticEquatorial.toEcliptic(an_object, j2000)
        self.assertAlmostEqual(0, utils.get_latitude(an_object_ec), self.places)
        self.assertAlmostEqual(0, utils.get_longitude(an_object_ec), self.places)

        an_object_eq = EclipticEquatorial.toEquatorial(an_object, j2000)
        self.assertAlmostEqual(0, utils.get_latitude(an_object_eq), self.places)
        self.assertAlmostEqual(360, utils.get_longitude(an_object_eq), self.places)


    def test_North_Pole(self):
        """Test J2000 North Pole"""

        j2000 = coords.datetime('2000-01-01T00:00:00')
        an_object = coords.spherical(1, coords.declination(90), coords.angle(0))

        an_object_ec = EclipticEquatorial.toEcliptic(an_object, j2000)
        self.assertAlmostEqual(66.56071, utils.get_latitude(an_object_ec), self.places)
        self.assertAlmostEqual(90, utils.get_longitude(an_object_ec), self.places)

        an_object_eq = EclipticEquatorial.toEquatorial(an_object, j2000)
        self.assertAlmostEqual(66.56071, utils.get_latitude(an_object_eq), self.places)
        self.assertAlmostEqual(270.00000, utils.get_longitude(an_object_eq), self.places)


    def test_lat_0_long_15(self):
        """Test J2000 Latitude 0, Longitude 15"""

        j2000 = coords.datetime('2000-01-01T00:00:00')
        an_object = coords.spherical(1, coords.declination(0), coords.angle(15))

        an_object_ec = EclipticEquatorial.toEcliptic(an_object, j2000)
        self.assertAlmostEqual(-5.90920, utils.get_latitude(an_object_ec), self.places)
        self.assertAlmostEqual(13.81162, utils.get_longitude(an_object_ec), self.places)

        an_object_eq = EclipticEquatorial.toEquatorial(an_object, j2000)
        self.assertAlmostEqual(5.90920, utils.get_latitude(an_object_eq), self.places)
        self.assertAlmostEqual(13.81162, utils.get_longitude(an_object_eq), self.places)


    def test_lat_0_long_345(self):
        """Test J2000 Latitude 0, Longitude 345"""

        j2000 = coords.datetime('2000-01-01T00:00:00')
        an_object = coords.spherical(1, coords.declination(0), coords.angle(345))

        an_object_ec = EclipticEquatorial.toEcliptic(an_object, j2000)
        self.assertAlmostEqual(5.90920, utils.get_latitude(an_object_ec), self.places)
        self.assertAlmostEqual(346.18838, utils.get_longitude(an_object_ec), self.places)

        an_object_eq = EclipticEquatorial.toEquatorial(an_object, j2000)
        self.assertAlmostEqual(-5.90920, utils.get_latitude(an_object_eq), self.places)
        self.assertAlmostEqual(346.18838, utils.get_longitude(an_object_eq), self.places)


    def test_lat_45_long_100(self):
        """Test J2000 Latitude 45, Longitude 100"""

        j2000 = coords.datetime('2000-01-01T00:00:00')
        an_object = coords.spherical(1, coords.declination(45), coords.angle(100))

        an_object_ec = EclipticEquatorial.toEcliptic(an_object, j2000)
        self.assertAlmostEqual(21.82420, utils.get_latitude(an_object_ec), self.places)
        self.assertAlmostEqual(97.60065, utils.get_longitude(an_object_ec), self.places)

        an_object_eq = EclipticEquatorial.toEquatorial(an_object, j2000)
        self.assertAlmostEqual(67.78257, utils.get_latitude(an_object_eq), self.places)
        self.assertAlmostEqual(108.94923, utils.get_longitude(an_object_eq), self.places)


    def test_lat_n30_long_n30(self):
        """Test J2000 Latitude -30, Longitude -30"""

        j2000 = coords.datetime('2000-01-01T00:00:00')
        an_object = coords.spherical(1, coords.declination(-30), coords.angle(-30))

        an_object_ec = EclipticEquatorial.toEcliptic(an_object, j2000)
        self.assertAlmostEqual(-16.64844, utils.get_latitude(an_object_ec), self.places)
        self.assertAlmostEqual(321.51905, utils.get_longitude(an_object_ec), self.places)

        an_object_eq = EclipticEquatorial.toEquatorial(an_object, j2000)
        self.assertAlmostEqual(-39.12273, utils.get_latitude(an_object_eq), self.places)
        self.assertAlmostEqual(345.18327, utils.get_longitude(an_object_eq), self.places)


    def test_lat_n60_long_200(self):
        """Test J2015 Latitude -60, Longitude 200"""

        j2015 = coords.datetime('2015-01-01T00:00:00')
        an_object = coords.spherical(1, coords.declination(-60), coords.angle(200))

        an_object_ec = EclipticEquatorial.toEcliptic(an_object, j2015)
        self.assertAlmostEqual(-46.59844, utils.get_latitude(an_object_ec), self.places)
        self.assertAlmostEqual(226.85843, utils.get_longitude(an_object_ec), self.places)

        an_object_eq = EclipticEquatorial.toEquatorial(an_object, j2015)
        self.assertAlmostEqual(-59.60899, utils.get_latitude(an_object_eq), self.places)
        self.assertAlmostEqual(158.23870, utils.get_longitude(an_object_eq), self.places)


    def test_lat_20_long_n10(self):
        """Test J2015 Latitude 20, Longitude -10"""

        j2015 = coords.datetime('2015-01-01T00:00:00')
        an_object = coords.spherical(1, coords.declination(20), coords.angle(-10))

        an_object_ec = EclipticEquatorial.toEcliptic(an_object, j2015)
        self.assertAlmostEqual(22.25346, utils.get_latitude(an_object_ec), self.places)
        self.assertAlmostEqual(359.15333, utils.get_longitude(an_object_ec), self.places)

        an_object_eq = EclipticEquatorial.toEquatorial(an_object, j2015)
        self.assertAlmostEqual(14.41240, utils.get_latitude(an_object_eq), self.places)
        self.assertAlmostEqual(342.84035, utils.get_longitude(an_object_eq), self.places)


if __name__ == '__main__':
    unittest.main()