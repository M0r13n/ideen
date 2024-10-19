#!/usr/bin/env python3

import getpass
import sys

from pamela import authenticate, PAMError

if __name__ == "__main__":
    user = getpass.getuser()
    password = getpass.getpass()
    service = 'some-service'

    try:
        authenticate(user, password, service=service)
    except PAMError as e:
        sys.exit(e)

    print('[DONE]')
