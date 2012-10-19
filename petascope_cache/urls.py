
from views.main import main,   index, cached_request

routes = [
    ((main, ''),
        ('/wcps', index),
        ('/wcps_cache', cached_request)
    )
]
