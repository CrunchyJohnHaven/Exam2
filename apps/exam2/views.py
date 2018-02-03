from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.contrib import messages
import datetime
from datetime import date

def index(request):
    print "Start Index Route"
    if "logged" in request.session:
        print "End Index Route - Logged in Session"
        return redirect('/travels')
    print "End Index Route - Logged Not In Session"
    return render(request, 'exam2/login.html')

def success(request):
    print "Start Success Route"
    if "logged" in request.session:
        this_user = User.objects.get(id=request.session['logged'])
        # print "THIS_USER.created_AT:",this_user.created_at
        # THIS_USER.created_AT: 2018-02-02 20:25:00.280046+00:00
        print "DATETIME.DATETIME.NOW():", datetime.datetime.now()
        # 2018-02-02 21:10:35.610152
        # print "this_user.trip_trips.all()", this_user
        # print Trip.objects.all()

        context = {
            'user': this_user,
            'my_trips': this_user.trip_trips.all(),
            'other_trips': Trip.objects.all(),
        }
        # print "context: ", context

        messages.success(request, "You have logged in.")
        return render(request, 'exam2/welcome.html', context)
    return redirect('/main')
    # ///////
# THIS USER: id: 10, name: Charlie, alias: C-Alias, email: c@gmail.com, password: $2b$05$cwTQhxdpK2Wxyp8Gc43Bq..LNyX/OfmDEx80hHj52a4LF1V6hGyQG, DOB: 1991-01-01
# faves = this_user.faved_travels.all()
# users = User.objects.exclude(id=request.session['logged'])
# 'faves': faves,
# 'travels': Quote.objects.all()
# ////////////
def users(request, id):
    if 'logged' not in request.session:
        return redirect('/main')
        
    this_user = User.objects.get(id=request.session['logged'])
    this_trip = Trip.objects.get(id=int(id))
    # my_travels = Quote.objects.filter(user=this_user)
    context = {
        'user': this_user,
        'my_trips': this_user.trip_trips.all(),
        'trip': this_trip,
        'users': this_trip.trip_users.all()

        # 'travels': my_travels,
        # 'faves': this_user.faved_quotes.all()
    }

    return render(request, 'exam2/users.html', context)


def reg(request):
    print "Start Reg Route"
    if "logged" in request.session:
        print "End Reg Route - Already Logged"
        return redirect('/travels')
    result = User.objects.reg_validator(request.POST)
    if isinstance(result, dict):
        for tag, error in result.iteritems():
            messages.error(request, error)
        return redirect('/main')
    else:
        result = int(result.id)
        request.session['logged'] = result
        print "End Reg Route - Registered"
        return redirect('/travels')

def login(request):
    print "Start Login Route"
    if "logged" in request.session:
        return redirect('/travels')
        print "End Login Route - Session"
    else:
        print "request.POST:", request.POST
        result = User.objects.login_validator(request.POST)
        # print "result: ", result
        if isinstance(result, dict):
            # print "result is dict (errors)"
            for tag, error in result.iteritems():
                messages.error(request, error)
            print "End Login Route - Invalid"
            return redirect('/main')
        else:
            # print "result is not dict (valid):", result
            request.session['logged'] = int(result.id)
            return redirect('/travels')

def logout(request):
    print "Start Logout Route"
    try:
        del request.session['logged']
    except KeyError:
        pass
    messages.error(request, "You have logged out.")
    print "End Logout Route"
    return redirect('/main')

def add(request, id):
    print "Start Add route"
    u = User.objects.get(id = request.session['logged'])
    q = Trip.objects.get(id = int(id))
    u.trip_trips.add(q)
    print "End Add Route"
    print "All trip_trips: ", u.trip_trips.all()
    return redirect('/travels')
    # ///////
   
    
    # 
    # ///////

def create(request, id):
    print "Start Create Route"
    print "ID: ", int(id)
    print "REQUEST.POST:", request.POST
    result = Trip.objects.create_validator(request.POST, int(id))
    if isinstance(result, dict):
        print "is dict"
        for tag, error in result.iteritems():
            print "error"
            messages.error(request, error)
        print "End Create Route - Errors"
        return redirect('/travels/add')
    id = str(result.id)
    print "End Create Route - Created"
    return redirect('/add/'+ id)
    
# /////////
# ID:  17
# REQUEST.POST: <QueryDict: {u'csrfmiddlewaretoken': [u'nTz99RTGOD9WkIhrEaUdRsUgpl83wQU39iPQB4mDicnrX9nMjHIsTNqQI1B0J5Na'], u'destination': [u'dest1'], u'description': [u'desc1'], u'end_date': [u'2918-01-03'], u'start_date': [u'2018-02-01']}>




# ////////
#     print "Request.POS: ", request.POST
#     print "Request.id: ", int(id)
#     result = Quote.objects.create_validator(request.POST, int(id))
#     if isinstance(result, dict):
#         # print "result is dict (errors)"
#         for tag, error in result.iteritems():
#             messages.error(request, error)
#         print "End Login Route - Invalid"
#         return redirect('/travels')
#     else:
#         u = User.objects.get(id = request.session['logged'])
#         # q = Quote.objects.get(id = int(result.id))
#         # u.faved_travels.add(q)
# /////////////

def remove(request, id):
    print "Start Remove Route"
    print "ID:", int(id)
    print "REQUEST.POST:", request.POST
    u = User.objects.get(id = request.session['logged'])
    q = u.trip_trips.get(id = int(id))
    q.trip_users.remove(u)
    print "End Create Route"
    return redirect('/travels')

def page1(request, id):
    print "Start Page1 Route"
    print "REQUEST.POST:", request.POST
    # print "ID:", int(id)
    return render(request, 'exam2/page1.html')

def page2(request):
    print "Start Page2 Route"
    print "REQUEST.POST:", request.POST
    context = {
        'user': User.objects.get(id=request.session['logged'])
    }
    return render(request, 'exam2/page2.html', context)
# ///////
    # u = User.objects.get(id = request.session['logged'])
    # print "u: ", u  
    # print "This_user's travels: ", Quote.objects.filter(id=int(id)) 
    # q = u.faved_travels.get(id = int(id))
    # print "q: ", q
    # q.faved_users.remove(u)
    # print "u.faved.all AFTER DELETE", u.faved_quotes.all() 
    # print "This_user's quotes: ", Quote.objects.filter(id=int(id))  
#////////

# <QueryDict: {u'content': [u'bbbbbb'], u'csrfmiddlewaretoken': [u'CjAIB8NmgzaOEBSHxuSyHD7RJW4mbVrXJvq2mTyKVmCVi9vSxTlA1jLOmXjKwuQr'], u'author': [u'aaaa']}>
# u:  id: 10, name: Charlie, alias: C-Alias, email: c@gmail.com, password: $2b$05$cwTQhxdpK2Wxyp8Gc43Bq..LNyX/OfmDEx80hHj52a4LF1V6hGyQG, DOB: 1991-01-01


# q:  id: 3, content: I've never seen a wild thing feel sorry for itse
# 
# 
# lf, a bird will fall frozen from a bough without ever having felt sorry for itself, author: D.H Lawrence, user: id: 9, name: Bravo, alias: B-Alias, email: b@gmail.com, password: $2b$05$4HeGFu/sZU8M5RriZe3OPealqLK5HoKkLOwg2CJVIA8lvltwvCG6C, DOB: 1991-02-02


# u.faved_quotes.add(q)
# u.faved_quotes.all()

# <QuerySet [<Quote: id: 1, content: The bell it tolls for thee, author: Ernest Hemingway, user: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>]>

