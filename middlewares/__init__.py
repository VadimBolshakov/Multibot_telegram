from create import PASSWORD, I18N_DOMAIN, LOCALES_DIR, FOUL_FILE
from .filters import AdminFilter, PrivateFilter
from .langmiddleware import ACLMiddleware
from .middleware import ManageMiddleware


def setup_middlewares_filters(dp):
    """Setup the all middlewares and filters."""
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(PrivateFilter)
    dp.middleware.setup(ManageMiddleware(password=PASSWORD, foul_file=FOUL_FILE))


def setup_middleware_i18n(dp):
    """Setup the middleware."""
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)

    return i18n
