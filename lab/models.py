class Host:

    ALLOWED_KEYS = [
        'name',
        'status',
        'uptime',
        'users',
        'load'
    ]

    def __init__(self, **kwargs):
        for k,v in kwargs:
            if k in ALLOWED_KEYS:
                setattr(self, k, v)
