from django.http import HttpResponse
import pusher, simplejson
from django.shortcuts import render_to_response
import simulation.settings as settings

def tracking(request):
    return render_to_response("tracking.html")

def endPoint(request):
    pusher.app_id = settings.PUSHER_APP_ID
    pusher.key = settings.PUSHER_KEY
    pusher.secret = settings.PUSHER_SECRET
    
    p = pusher.Pusher()
    p['test_channel'].trigger('condor_channel', ['hi'])
    return HttpResponse("Done")