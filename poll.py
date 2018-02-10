import threading
import requests

def poll(poll_stop):
    # Poll the server
    # Figure out later
    requests.get('http://dev-isthekrispykremehotlighton.herokuapp.com/api/last-open')
    if not poll_stop.is_set():
        # call again in five pinutes
        threading.Timer(60*5, poll, [poll_stop]).start()

poll_stop = threading.Event()
poll(poll_stop)
# stop the thread when needed
#poll_stop.set()