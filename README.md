# Django Snail (Middleware)
<br/>

_Makes your development server configurably slower so you can mimic real production speeds._

- Choose which requests will be throttled
- Choose the time (in miliseconds) of throttling
- Configurable from both sides; Server (Django settings) and Client (on-demand) (Special request headers)
#
![](django-snail-logo.png)

#### Rationale

_I was missing a simple way to slow down my development server when working on frontend JavaScript to be able to see/debug loading animations and see how the code works when it's not in its full speed. That's why I created this simple module._
## Installation

First you need to install the module using `pip`:

`pip install django-snail`

Then add the middleware to `settings.MIDDLEWARE`


#### settings.py

```
MIDDLEWARE = [
    'django_snail.SnailMiddleware',
    ...
]
```

## Configuration

You can either configure the throttling using `SnailRule` instances in the `settings.py` or you can tell the `django-snail` to throttle your requests _on-demand_ by adding `SnailThrottleMsRange` header to your request.

#### Server side throttling

To configure the throttling server-side, you need to instantiate `SnailRule` class. You can use any number of different
rules (the first one only is applied)

```
from django_snail import SnailRule

api_v1_500ms = SnailRule(match_url='/api/v1/', ms_min=500, ms_max=500, match_headers=None)
api_v2_200ms_to_600ms = SnailRule(match_url='/api/v2/', ms_min=200, ms_max=600, match_headers=None)

content_type_application_json_header = {'Content-Type':'application/json'}
content_type_application_json = SnailRule(match_headers=content_type_application_json_header, ms_min=200, ms_max=600)

SNAIL_RULES = [api_v1_500ms, api_v2_200ms_to_600ms, content_type_application_json]
```

And that's it. 
<br/>

#### On-Demand throttling (Client-side)

All the requests that are to be throttled need to contain `SnailThrottleMsRange` header.
The value can be either one integer or two integers separated by comma. 

SnailThrottleMsRange:

```
// this request will be slowed down (throttled) by a random number of miliseconds between 500 and 1000

axios.post('https://url.com', payload, {
    headers: {
    'SnailThrottleMsRange': '500,1000'
    }
  }
)
```