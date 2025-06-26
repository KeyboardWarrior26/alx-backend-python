#!/usr/bin/python3
import sys

# Import the lazy_paginate function from your 2-lazy_paginate.py file
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate

try:
    # Call the generator with page size 100
    for page in lazy_paginator(100):
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()

