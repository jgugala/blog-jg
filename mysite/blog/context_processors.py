def get_user(request):
    user = request.user
    return {
        'user': user
    }
