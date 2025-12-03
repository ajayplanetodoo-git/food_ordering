'''
This is helper function to detectec user role
'''
def detectuser(user):
    if user.role == 1:
        redirectUrl = 'vendashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "custdashboard"
        return redirectUrl
    elif user.role == None:
        redirectUrl = "/admin"
        return redirectUrl