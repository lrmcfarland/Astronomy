# Astronomical Algorithms Implemented

Astronomical Algorithms Implemented (AAI) is a collection of my
implementations of various algorithms I found on line and in books, in
particular [Astronomical
Algorithms](http://www.willbell.com/math/mc1.htm) by [Jean
Meeus](https://en.wikipedia.org/wiki/Jean_Meeus)

I use this to collect what I learned about various programming problems into
a coherent whole in service of an application.

I started with some object oriented ideas about using C++ to build a
[Coordinates library](https://github.com/lrmcfarland/Coordinates)
I also used it to learn Scott Meyer's Effective C++ and other
programming techniques.
I use the operator overloading feature of C++
to abstract away the vector arithmetic and focus on the physics.
The other goal is to provide examples of unit testing
for C++ and python.

I also saw a natural use operator overloading with of a simple three
element vector used in classical physics.
I also wrapped these C++ objects in python using
[Boost](https://github.com/lrmcfarland/Coordinates/tree/master/Python/Boost),
[SWIG](https://github.com/lrmcfarland/Coordinates/tree/master/Python/SWIG)
and also
["manually"](https://github.com/lrmcfarland/Coordinates/tree/master/Python/Manual)
i.e. using only python.
With Python, I can use microframeworks like
[flask](https://en.wikipedia.org/wiki/Flask_(web_framework)) to
provide a browser UI.
That also opens the door for HTML, CSS,
JavaScript, JSON, JQuery and Google charts and an [AAI REST
API](https://github.com/lrmcfarland/AAI/blob/master/www/api.py).

I found this to be a very flexible development environment.
- I can run the [flask microframework](http://flask.pocoo.org/) from my OS X command line with the python debugger.
- add that to a [docker container](https://github.com/lrmcfarland/AAI/blob/master/Dockerfile.flask) running CentOS
- with a [gunicorn](https://gunicorn.org/) server [docker container](https://github.com/lrmcfarland/AAI/blob/master/Dockerfile.gunicorn)
- so it can support aai.starbug.com a service for an [nginx reverse
proxy](https://github.com/lrmcfarland/starbug.com) with transport
layer security
[TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) end
point.

This last step allows the user's browser to send its location information to
AAI for processing.
The AAI server will also accept
location information entered directly as text.



It is still a work in progress.

-lrm 2019 Jan 18




# Build

This section describes how to build the docker container versions of
the AAI server.  The command line version is described in the
[www/README](https://github.com/lrmcfarland/AAI/blob/master/www/README.md).
There are also build instructions in the header of the [docker
files](https://github.com/lrmcfarland/AAI/blob/master/Dockerfile.gunicorn).


This build is a little unusual in that it uses git sub-modules to
recursively checkout the Coordinates (and googletest) libraries it
needs.
So if you don't set the branch name in the docker file, it checks
out master by default.  This can cause confusion if you have not
committed your changes to the branch and are wondering why they
haven't shown up in your container.

TODO It would be easier of it COPY-ed the local changes, but I haven't
finished working through the issues with getting git to ignoring all
the right build artifacts.


## flask

```
docker build -f Dockerfile.flask -t aai_flask .
```


## gunicorn


```
docker build -f Dockerfile.gunicorn -t aai_gunicorn .
```



## create persistent storage for logs



```
docker volume create starbuglogs
```



## create starbugnet for use with nginx


```
docker network create starbugnet
```



# Configure


## flask

The flask configuration [config/aai-flask-testing-config.py](https://github.com/lrmcfarland/AAI/blob/master/www/config/aai-flask-testing-config.py)
It takes the usual [flask configuration
parameters](http://flask.pocoo.org/docs/1.0/config/) and a
GOOGLEMAPS_KEY.
The checked in version does not have a valid GOOGLEMAPS_KEY so the map
won't display until it does, but the web page should come up
and the API will function.
A real deployment should include a real GOOGLEMAPS_KEY and
change the flask SECRET_KEY.

Dockerfile.flask copies these configuration files to the
image when it is built.
I use config/aai-flask-deployment-config.py to store my
real keys and exclude it from the repo by including
it in .gitignore

The aai-flask-testing-config.py is include as an example and
can be used with out a valid GOOGLEMAPS_KEY.
It is also the default if the file location is not
overridden by the command line option or by setting
the AAI_FLASK_CONFIG environment variable, e.g.
with -e as the docker run option.


TODO persistent storage for config?

## gunicorn

The gunicorn config file is here
[AAI/www/config/aai-gunicron-config.py](https://github.com/lrmcfarland/AAI/blob/master/www/config/aai-gunicorn-config.py).
and supports the usual [gunicorn config settings](http://docs.gunicorn.org/en/stable/settings.html).


# Run


## flask

Warning: -p ports must match what is in the flask configuration file.

### default (testing) configuration

```
docker run --name aai_flask_00 --mount source=starbuglogs,target=/opt/starbug.com/logs -d -p 8080:8080 aai_flask
```

### with a deployment configuration

Set the AAI_FLASK_CONFIG environment variable to the location of the
config file in the container.
See
[Dockerfile.flask](https://github.com/lrmcfarland/AAI/blob/master/Dockerfile.flask)
for how to COPY it there.


```
docker run --name aai_flask_00 -e AAI_FLASK_CONFIG='config/aai-flask-deployment-config.py' --mount source=starbuglogs,target=/opt/starbug.com/logs -d -p 8080:8080 aai_flask
```


## gunicorn

Warning: -p ports must match what is in the flask configuration file.


### default (testing) configuration


```
docker run --net starbugnet --name aai_gunicorn_00 --mount source=starbuglogs,target=/opt/starbug.com/logs -d -p 8080:8080 aai_gunicorn
```


### with a deployment configuration

Set the AAI_FLASK_CONFIG environment variable to the location of the
config file in the container.
See
[Dockerfile.gunicorn](https://github.com/lrmcfarland/AAI/blob/master/Dockerfile.flask)
for how to COPY it there.


```
docker run --net starbugnet --name aai_gunicorn_00 --mount source=starbuglogs,target=/opt/starbug.com/logs -d -e AAI_FLASK_CONFIG='config/aai-flask-deployment-config.py' -p 8080:8080 aai_gunicorn
```


# API

The server supports an AAI REST API to process AAI requests, like
like converting degree:minutes:seconds into
decimal degrees.

```
$ curl https://aai.starbug.com/api/v1/dms2dec?dms=12:45
{"dec":"12.75","errors":[]}
```

Or converting RA/Dec coordinates to azimuth/altitude ones given
the observer's location and time.

```
$ curl https://aai.starbug.com/api/v1/radec2azalt?latitude=37.40012123209991\&longitude=-122.08225404051541\&date=2017-12-11\&time=21%3A42%3A05\&timezone=-8\&dst=false\&ra=0\&dec=0

{
  "altitude": 34.91958722761523,
  "azimuth": 237.74055887676423,
  "datetime": "2017-12-11T21:42:05-08",
  "observer": "<spherical><r>1</r><theta>52.5999</theta><phi>-122.082</phi></spherical>"
}

```

and the reverse

```
$ curl https://aai.starbug.com/api/v1/azalt2radec?latitude=37.40012123209991\&longitude=-122.08225404051541\&date=2017-12-11\&time=21%3A42%3A05\&timezone=-8\&dst=false\&azimuth=237.74055887676423\&altitude=34.91958722761523
{
  "datetime": "2017-12-11T21:42:05-08",
  "dec": 1.4210854715202004e-14,
  "observer": "<spherical><r>1</r><theta>52.5999</theta><phi>-122.082</phi></spherical>",
  "ra": 24.0
}
```

It also returns more complex data objects like the [sun's position
over a
day](https://github.com/lrmcfarland/Astronomy/blob/master/Bodies/SunPosition.py)
sun given the observer's location on earth
in latitude, longitude and date-time.

```
curl https://aai.starbug.com/api/v1/sun_position_data\?latitude=37\&longitude=-122\&date=2017-12-11\&time=14\%3A37\%3A54\&timezone=-8\&dst=false

{
  "altitude_data_24h": [
    [
      0,
      -53.12289141057474,
      -29.529772137731925,
      -52.545518554707144,
      -76.3762556772508,
      -75.96224706420884
    ],

...

  ],
  "datetime": "2017-12-11T14:37:54-08",
  "observer": "<spherical><r>1</r><theta>53</theta><phi>-122</phi></spherical>",
  "rising": "2017-12-11T07:12:13.2009-08",
  "setting": "2017-12-11T16:52:24.806-08",
  "sun_date_label": [
    "2017-12-11"
  ],
  "sun_marker_altitude": "19:33:0.925497 (19.5502570824)",
  "sun_marker_azimuth": "218:05:11.8683 (218.086630087)",
  "sun_marker_time": 14.631666675209999,
  "transit": "2017-12-11T12:02:19.0035-08"
}


```

This is still changing frequently.
Use the [api.py source](https://github.com/lrmcfarland/AAI/blob/master/www/api.py) for the latest.



# log files


## AAI flask

Use docker logs aai_flask_00 to see what is happening.
At this time I haven't configured logging to persistent storage like AAI gunicorn.


## AAI gunicorn

In addition to the docker logs, aai_gunicorn log files are available
persistent storage.  The gunicorn files are written to the location
given in the gunicorn config file
[AAI/www/config/aai-gunicron-config.py](https://github.com/lrmcfarland/AAI/blob/master/www/config/aai-gunicorn-config.py).

Use docker exec bash to access the logs in the running container

```
$ docker exec -it aai_gunicorn_00 bash

[starbug@c0d26b279a07 www]$ tail /opt/starbug.com/logs/aai-error.log
[2019-01-17 06:17:45 +0000] [10] [INFO] Starting gunicorn 19.9.0
[2019-01-17 06:17:45 +0000] [10] [INFO] Listening at: http://0.0.0.0:8080 (10)
[2019-01-17 06:17:45 +0000] [10] [INFO] Using worker: sync
[2019-01-17 06:17:45 +0000] [15] [INFO] Booting worker with pid: 15
[2019-01-17 06:17:45 +0000] [20] [INFO] Booting worker with pid: 20
WARNING:root:Using AAI flask test configuration.
[2019-01-17 06:17:45 +0000] [21] [INFO] Booting worker with pid: 21
[2019-01-17 06:17:45 +0000] [22] [INFO] Booting worker with pid: 22
WARNING:root:Using AAI flask test configuration.
WARNING:root:Using AAI flask test configuration.
WARNING:root:Using AAI flask test configuration.

```

or one that just runs the shell

```
$ docker run -it --rm --mount source=starbuglogs,target=/opt/starbug.com/logs --user root --entrypoint /bin/bash aai_gunicorn

```





# Troubleshooting


## build branch

The docker build checks out the AAI source from github.
Check that the docker build branch is correct in the docker file if it
is not master.
With out this, your changes will not show up in the container.
See [Dockerfile.flask](https://github.com/lrmcfarland/AAI/blob/master/Dockerfile.flask#L64)
or [Dockerfile.gunicorn](https://github.com/lrmcfarland/AAI/blob/master/Dockerfile.gunicorn#L69)
just before <i>git submodule update</i>.


## aai-flask-deployment-config.py: no such file or directory

The build fails at

```
COPY failed: stat /var/lib/docker/tmp/docker-builder394900186/www/config/aai-flask-deployment-config.py: no such file or directory
```

Provide a deployment file or comment out this line.


## IOError: [Errno 13] Permission denied: '/opt/starbug.com/logs/aai-error.log'

Flask runs as starbug and gunicorn as root, so they may step
on each others log file.
Chown or delete the file as needed.

TODO why?



# Under development.

## [Equation of Time](https://en.wikipedia.org/wiki/Equation_of_time)

![Equation of Time](https://github.com/lrmcfarland/Astronomy/blob/master/images/eot_2015.png?raw=true)

## [Analemma](https://en.wikipedia.org/wiki/Analemma)

![Analemma](https://github.com/lrmcfarland/Astronomy/blob/master/images/analemma_45N.png?raw=true)

## Lunar Altitude

![Lunar Altitude](https://github.com/lrmcfarland/Astronomy/blob/master/images/lunar_altitude_20150429.png?raw=true)
