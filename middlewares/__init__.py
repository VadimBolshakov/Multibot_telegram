from .filters import PrivateFilter
from .langmiddleware import ACLMiddleware
from .middleware import ManageMiddleware
from .getrandomstr import get_random_string


def setup_middlewares_filters(dp, password, foul_file, db, logger):
    """Set up the all middlewares and filters."""
    dp.filters_factory.bind(PrivateFilter)
    dp.middleware.setup(ManageMiddleware(logger=logger, db=db, password=password, foul_file=foul_file))


def setup_middleware_i18n(dp, domain, locales_dir, db):
    """Set up the middleware."""
    i18n = ACLMiddleware(domain=domain, path=locales_dir, db=db)
    dp.middleware.setup(i18n)
    return i18n
