from pyramid.httpexceptions import HTTPForbidden


def need_permission(account_type):
    '''檢查權限， account_type 可以為 admin, manager, school'''

    def check_permission(func):
        def access_or_forbidden(request):
            if account_type == request.session.get('account_type', None):
                return func(request)
            else:
                return HTTPForbidden()
        return access_or_forbidden
    return check_permission