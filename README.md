<p align="center">
  <img alt="PyChronos Logo" src="https://github.com/abbott/pychronos/blob/main/logo.png?raw=true" width="80" />
</p>
<h1 align="center">
  PyChronos
</h1>
<p align="center">
A small Docker container to run and schedule Python scripts
</p>

<!-- 
[![Build Status](https://travis-ci.com/simse/chronos.svg?branch=master)](https://travis-ci.com/simse/chronos)

Replace with local lab build endpoint
-->

## About
PyChronos is a simple application to execute Python scripts in response to certain events. Each script will be assigned a virtual environment and folder, allowing Pip dependencies to be installed without conflicting with other scripts. The current Python version is 3.9.

PyChronos is not intended for larger Python scripts that are meant to run forever, or listen on ports (yet!).

## Installation
You may install PyChronos via Docker.
```
docker pull abbott/pychronos
```
And then run:
```
docker run -p 5000:5000 -v CONFIG_PATH:/pychronos abbott/pychronos
```

## Security
Please do not expose PyChronos to the public internet. At the moment there is zero security against unauthorised access, and attackers *would* be able to execute malicious code on your server quite easily.

## Features
- Beautiful and functional web UI
- Fast and lightweight
- Ability to create individual virtual environments
- Interval triggers (e.g. every 10 seconds)
- CRON triggers (e.g. every 5th day of the month)
- `stdout` and `stderr` output capture
- Live script output capture (so you know it's still working)

<!-- ## Feature requests
Trivial requests will usually be added quickly. Larger requests will take a little longer. I am, after all, still a busy university student. -->

## Screenshots
You can find screenshots [right here](https://imgur.com/a/PQdH5ro).

## Bug reporting
If you found a bug, open an issue on GitHub.

## Legacy
This project is a fork of "Chronos" developed by Simon Sorensen (@simse), and archived Apr 10, 2023. https://github.com/simse/chronos

The fork was renamed to "PyChronos" because many unrelated projects exist under the name "Chronos" or similar.
