from main.api.callback import HttpResponseForbidden


def authorized_access(user_types=None, msg="Not authorized to access resource"):
    def decorating_function(func):
        def wrapped_function(request, *args, **kwargs):
            authorized = False
            # can add more types to it, maybe allow anonymous_user
            if "authorized_user" in user_types and not authorized:
                authorized = request.user.is_authenticated
            if not authorized:
                return HttpResponseForbidden(content=msg)

            return func(request, *args, **kwargs)

        return wrapped_function

    return decorating_function
