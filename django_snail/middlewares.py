import logging
import random
import re
import time
import typing

from django.conf import settings
from django.http.request import HttpRequest

logger = logging.getLogger('django-snail')

def mls_to_s(ms):
    return ms / 1000


def mls_to_mcs(mls):
    return mls * 1000


def mcs_to_mls(mcs):
    return mcs / 1000


def s_to_mls(s):
    return s * 1000

class DjangoSnailException(Exception):
    pass

class SnailRule:
    def __init__(self, match_url, match_headers, ms_min, ms_max):
        self.match_url = match_url
        self.match_headers = match_headers
        self.ms_min = ms_min
        self.ms_max = ms_max

    @property
    def throttle_range(self):
        if self.ms_min is not None and self.ms_max is not None:
            return (self.ms_min, self.ms_max)
        raise DjangoSnailException("Invalid throttle ms params")

    def is_match(self, request: HttpRequest) -> bool:
        url = request.build_absolute_uri()
        if self.match_url:
            pattern = re.compile(self.match_url)
            if not (pattern.search(url)):
                return False
        if self.match_headers:
            if not self.match_headers == request.headers:
                return False
        return True

def sleep_in_ms(ms):
    time.sleep(mls_to_s(ms))

class InvalidSnailThrottleMsRangeHeader(Exception):
    pass


class SnailMiddleware:
    """ Middleware that throttle responses """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        header_throttle_range = self._check_header(request)
        if header_throttle_range:
            if header_throttle_range[0] == header_throttle_range[1]:
                wait_ms = header_throttle_range[0]
            else:
                wait_ms = random.choice(list(range(*header_throttle_range)))
            sleep_in_ms(wait_ms)
        else:
            snail_rules = getattr(settings,'SNAIL_RULES',[])
            snail_rule: SnailRule
            for snail_rule in snail_rules:
                if snail_rule.is_match(request):
                    sleep_in_ms(random.choice(list(range(*snail_rule.throttle_range))))

        response = self.get_response(request)
        return response

    @classmethod
    def _check_header(cls, request: HttpRequest) -> typing.Optional[tuple]:
        if 'SnailThrottleMsRange' in request.headers.keys():
            raw_request_val = request.headers['SnailThrottleMsRange']
            val_split = raw_request_val.split(',')
            if val_split.__len__() == 1:
                return int(val_split[0]), int(val_split[0])
            elif val_split.__len__() == 2:
                return int(val_split[0]), int(val_split[1])
            raise InvalidSnailThrottleMsRangeHeader(
                f"Invalid SnailThrottleMsRangeHeader header value: '{raw_request_val}'")
