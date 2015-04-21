"""Unit tests for Sun Position calculations

to run:  ./pylaunch.sh test_SunPosition.py
verbose: ./pylaunch.sh test_SunPosition.py -v
filter:  ./pylaunch.sh test_SunPosition.py -v test_EoT_404MLC_2015_03_20T12_00
debug:   ./pylaunch.sh -m pdb test_SunPosition.py

next until import module:

(Pdb) n
> /Users/lrm/src/Astronomy/Transforms/test_SunPosition.py(25)<module>()
-> import SunPosition
(Pdb) b SunPosition.SunPosition.EquationOfTime
Breakpoint 1 at /Users/lrm/src/Astronomy/Transforms/SunPosition.py:17


"""

import math
import time
import unittest

import coords
import SunPosition

from Transforms import EclipticEquatorial
from Transforms import EquatorialHorizon
from Transforms import utils


class SunPositionsTests(unittest.TestCase):
    """Test Sun Position calculations"""

    def setUp(self):
        """Set up test parameters."""

        self.places = 12

        self.mlc404 = utils.latlon2spherical(a_latitude=coords.angle(37, 24),
                                             a_longitude=coords.angle(-122, 4, 56))


    def test_stick_shadow_2015_03_21(self):
        """Test matches sun angle measured from a stick's shadow

        Stick not straight, shadow not level.

        Note time zone.
        """

        a_datetime = coords.datetime('2015-03-21T12:57:00-08')

        ecliptic_longitude, R = SunPosition.SolarLongitude(a_datetime)

        sun_ec = coords.spherical(R, coords.angle(90), ecliptic_longitude)
        sun_eq = EclipticEquatorial.toEquatorial(sun_ec, a_datetime)
        sun_hz = EquatorialHorizon.toHorizon(sun_eq, self.mlc404, a_datetime)

        self.assertAlmostEqual(196.74093494548637, utils.get_azimuth(sun_hz).value, self.places)
        self.assertAlmostEqual(51.50253975117711, utils.get_altitude(sun_hz).value, self.places)


    def test_sextant_2015_03_27(self):
        """Test against sextant measurement

        The sun angle is measured with a sextant using a swimming pool
        as an artificial horizon.

        A light wind blurred the reflected image, sextant calibration rough

        Sextant reading 70:10 => 35:05 (35.0833333333) degrees altitude (/=2)

        Note time zone.

        TODO improve precision, but problem largely in sextant user
        """

        a_datetime = coords.datetime('2015-03-27T16:24:00-07')

        ecliptic_longitude, R = SunPosition.SolarLongitude(a_datetime)

        sun_ec = coords.spherical(R, coords.angle(90), ecliptic_longitude)
        sun_eq = EclipticEquatorial.toEquatorial(sun_ec, a_datetime)
        sun_hz = EquatorialHorizon.toHorizon(sun_eq, self.mlc404, a_datetime)
        self.assertAlmostEqual(243.07115892922118, utils.get_azimuth(sun_hz).value, self.places)

        sextant_alt = coords.angle(utils.parse_angle_arg('70:10').value/2)
        self.assertAlmostEqual(sextant_alt.value, utils.get_altitude(sun_hz).value, delta=1)


    def test_sextant_2015_04_20(self):
        """Test against sextant measurement

        The sun angle is measured with a sextant using a swimming pool
        as an artificial horizon.

        A light wind blurred the reflected image, sextant calibration rough

        Sextant reading 44:32 => 22:15:60 (22.2666666667) degrees altitude (/=2)

        Note time zone.

        TODO improve precision, but problem largely in sextant user
        """

        a_datetime = coords.datetime('2015-04-20T17:52:00-07')

        ecliptic_longitude, R = SunPosition.SolarLongitude(a_datetime)

        sun_ec = coords.spherical(R, coords.angle(90), ecliptic_longitude)
        sun_eq = EclipticEquatorial.toEquatorial(sun_ec, a_datetime)
        sun_hz = EquatorialHorizon.toHorizon(sun_eq, self.mlc404, a_datetime)
        self.assertAlmostEqual(267.90829781482097, utils.get_azimuth(sun_hz).value, self.places)

        sextant_alt = coords.angle(utils.parse_angle_arg('44:32').value/2)
        self.assertAlmostEqual(sextant_alt.value, utils.get_altitude(sun_hz).value, delta=1)


    @unittest.skip('todo')
    def test_EoT_2015_01_01T12_00(self):
        """Test Equation of time 2015-01-01T12:00:00

        validate with http://www.esrl.noaa.gov/gmd/grad/solcalc/
        """

        a_datetime = coords.datetime('2015-01-02T12:00:00-08')
        eot = SunPosition.EquationOfTime(a_datetime)

        # NOAA says -3.59 minutes
        self.assertAlmostEqual(-3.4317446135022323, eot.value, self.places)


    @unittest.skip('todo')
    def test_EoT_2015_02_11T12_00(self):
        """Test Equation of time 2015-02-11T12:00:00

        first local minimum of the year

        validate with http://www.esrl.noaa.gov/gmd/grad/solcalc/
        """

        a_datetime = coords.datetime(2015, 02, 11, 12)
        eot = SunPosition.EquationOfTime(a_datetime)

        # NOAA says -14.24 minutes
        self.assertAlmostEqual(-14.212711856485711, eot.value*60, self.places)


    @unittest.skip('todo')
    def test_EoT_2015_03_20T12_00(self):
        """Test Equation of time 2015-03-20T12:00:00

        validate with http://www.esrl.noaa.gov/gmd/grad/solcalc/
        """

        a_datetime = coords.datetime(2015, 03, 20, 12)
        eot = SunPosition.EquationOfTime(a_datetime)

        # NOAA says -7.44 minutes
        self.assertAlmostEqual(-7.563513810377245, eot.value*60, self.places)


    @unittest.skip('todo')
    def test_EoT_2015_05_14T12_00(self):
        """Test Equation of time 2015-05-14T12:00:00

        first local maximum of the year

        validate with http://www.esrl.noaa.gov/gmd/grad/solcalc/
        """

        a_datetime = coords.datetime(2015, 05, 14, 12)
        eot = SunPosition.EquationOfTime(a_datetime)

        # NOAA says 3.65 minutes
        self.assertAlmostEqual(3.6588472510257475, eot.value*60, self.places)


    @unittest.skip('todo')
    def test_EoT_2015_07_26T12_00(self):
        """Test Equation of time 2015-07-26T12:00:00

        second local minimum of the year

        validate with http://www.esrl.noaa.gov/gmd/grad/solcalc/
        """

        a_datetime = coords.datetime(2015, 07, 26, 12)
        eot = SunPosition.EquationOfTime(a_datetime)

        # NOAA says -6.54 minutes
        self.assertAlmostEqual(-6.5354183954768175, eot.value*60, self.places)



    @unittest.skip('todo')
    def test_EoT_2015_11_03T12_00(self):
        """Test Equation of time 2015-11-03T12:00:00

        second local maximum of the year

        validate with http://www.esrl.noaa.gov/gmd/grad/solcalc/
        """

        a_datetime = coords.datetime(2015, 11, 03, 12)
        eot = SunPosition.EquationOfTime(a_datetime)

        # NOAA says 16.48 minutes
        self.assertAlmostEqual(16.43786410739647, eot.value*60, self.places)





if __name__ == '__main__':
    unittest.main()
