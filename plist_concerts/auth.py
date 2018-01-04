import webbrowser

def goToSpotify(auth_url):
    webbrowser.open(auth_url, new=1)
    return 1
