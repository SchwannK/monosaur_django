from django.core.urlresolvers import get_resolver

# returns a map of admin method name->url 
# (all currently registered views that start with analyse/admin/).
# Don't use named groups in admin methods
def get_admin_methods():
    admin_methods = []
    for key in get_resolver(None).reverse_dict.keys():
        url = str(get_resolver(None).reverse_dict[key][1])
        if url.startswith('analyse/admin/'):
            url = url.replace('analyse/', '')
            admin_methods.append({'name' : key.__name__, 'url' : url})
    print(str(admin_methods))
    return admin_methods
