from django.core.urlresolvers import get_resolver

# returns a map of admin method name->url 
# (all currently registered views that start with analyse/admin/).
# Don't use named groups in admin methods
def get_admin_methods():
    admin_methods = {}
    for key in get_resolver(None).reverse_dict.keys():
        url = str(get_resolver(None).reverse_dict[key][1])
        if url.startswith('analyse/admin/'):
            admin_methods[key.__name__] = url
    return admin_methods
