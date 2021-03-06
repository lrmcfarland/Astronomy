#!/usr/bin/env python

"""The Astronomical Algorithms Implemented in C++ and Python Web UI using Flask

To run: ./bin/pylaunch.sh aai.py

with rotating logging: ./pylaunch.sh aai.py -l debug --loghandler rotating --logfilename ./logs/aai-flask.log
"""

import argparse
import flask
import logging
import logging.handlers



home_page = flask.Blueprint('home_blueprint', __name__, template_folder='templates')



@home_page.route("/")
def home():
    """Application's home"""

    return flask.render_template('home.html')


@home_page.route("/lunar_daily_altitude_chart")
def lunar_daily_altitude_chart():
    """Plot the moon's altitude for the observer's location"""

    return flask.render_template('lunar_daily_altitude_chart.html')


@home_page.route("/solar_azimuth_map")
def solar_azimuth_map():
    """Plot the sun's azimuth for the observer's location"""

    return flask.render_template('solar_azimuth_map.html')


@home_page.route("/solar_daily_altitude_chart")
def solar_daily_altitude_chart():
    """Plot the sun's altitude for the observer's location"""

    return flask.render_template('solar_daily_altitude_chart.html')


@home_page.route("/transform_observations")
def transform_observations():
    """Transform observation coordinates at observer's location"""

    return flask.render_template('transform_observations.html')


@home_page.route("/transform_times")
def transform_times():
    """Transform various time formats like deg:min:sec to decimal degrees"""

    return flask.render_template('transform_times.html')


@home_page.route("/accuracy")
def accuracy():
    """Accuracy page"""

    return flask.render_template('accuracy.html')


