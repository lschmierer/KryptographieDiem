from tocas import Restklassenring

import prime


def _restklassenring_ist_endlicher_koerper(k, prime_test=prime.miller_rabin):
    return prime_test(k.modulus)


Restklassenring.ist_endlicher_koerper = _restklassenring_ist_endlicher_koerper
