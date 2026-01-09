from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

from vendor_app.models import Vendor

def get_or_set_current_location(request): #  already user have olocation
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng,lat
    elif 'lat' in request.GET: # this section run when user 1st time open and pass location then it take from url and set to session
        lat= request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng,lat
    else:
        return None




def home(request):
    if get_or_set_current_location(request)is not None: 
      
        #  whenever we are passing location to  POINT  alway pass 
        # longitude 1st then pass lattitude it's pre define like (lng,lat) 
        pnt = GEOSGeometry("POINT(%s %s)" % (get_or_set_current_location(request)))
        

        vendor = Vendor.objects.filter(
                                user_profile__location__distance_lte=(pnt, D(km=30))
                                ).annotate(distance_u=Distance('user_profile__location',pnt)).order_by('distance_u')
                                #    distance_u id used difine in annotate 

        for v in vendor:
            v.kms = round(v.distance_u.km,1)
            print(v.vendor_name,v.user_profile.address)

    else:
        vendor = Vendor.objects.filter(is_approved=True,user__is_active=True)[:8]
    context = {
        'vendors':vendor,
    }
    return render(request,"home.html",context)