[![Build Status](https://travis-ci.org/alimac/err-request-tracker.svg?branch=master)](https://travis-ci.org/alimac/err-request-tracker)
[![Coverage Status](https://coveralls.io/repos/alimac/err-request-tracker/badge.svg?branch=master&service=github)](https://coveralls.io/github/alimac/err-request-tracker?branch=master)

# Request Tracker plugin for Errbot

[Errbot](http://errbot.net) is a Python-based bot. This is is a plugin for
Errbot that integrates with [RT: Request Tracker](https://www.bestpractical.com/rt/),
an issue tracking system.

## Requirements

This plugin uses [python-rt](https://gitlab.labs.nic.cz/labs/python-rt) -
the Python interface to Request Tracker API.
```
sudo pip install rt
```

## Installation

In a private chat with your bot:
```
!repos install https://github.com/alimac/err-request-tracker.git
```

## Configuration

`err-request-tracker` requires four variables to be configured:

- **REST_URL** - the URL to be used to make REST calls to the RT API (example:
`http://localhost/REST/1.0`)
- **DISPLAY_URL** - the URL to view a ticket (example:
`https://localhost/Ticket/Display.html?id=`)
- **USER** - username used to log in
- **PASSWORD** - password user to log in
- **MINIMUM_TICKET_ID** - optional minimum ticket value for ticket searches
(helps to avoid triggering the bot on every numerical value posted in chat)

An example configuration might look like:

```
!plugin config RT
{ "REST_URL" : "http://rt.example.com/REST/1.0",
  "USER" : "err",
  "PASSWORD" : "foo",
  "DISPLAY_URL" : "https://rt.example.com/Ticket/Display.html?id=" }
```

## Usage

Enter a ticket number in the chat:
```
1173397
is anyone working on 1173397
```

Bot will reply with:
```
Website is down! (https://rt.example.com/Ticket/Display.html?id=1173397) in
General from customer@example.com
```

For backends that support HTML display, the reply might look like:

> [Website is down!](https://rt.example.com/Ticket/Display.html?id=1173397) in
General from customer@example.com
