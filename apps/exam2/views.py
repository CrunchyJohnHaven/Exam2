from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.contrib import messages

def index(request):
    print "Start Index Route"
    if "logged" in request.session:
        print "End Index Route - Logged in Session"
        return redirect('/quotes')
    print "End Index Route - Logged Not In Session"
    return render(request, 'exam2/login.html')

def success(request):
    print "Start Success Route"
    this_user = User.objects.get(id=request.session['logged'])
    
    # THIS USER: id: 10, name: Charlie, alias: C-Alias, email: c@gmail.com, password: $2b$05$cwTQhxdpK2Wxyp8Gc43Bq..LNyX/OfmDEx80hHj52a4LF1V6hGyQG, DOB: 1991-01-01
    
    faves = this_user.faved_quotes.all()
    
    # FAVES: <QuerySet [<Quote: id: 8, content: vaef vaef adg , author: aervaefvaefv, user: id: 8, name:  Alpha, alias: A-Alias, email: a@gmail.com, password:     $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>]>

    # users = User.objects.exclude(id=request.session['logged'])

    # <QuerySet [<User: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>, <User: id: 9, name: Bravo, alias: B-Alias, email: b@gmail.com, password: $2b$05$4HeGFu/sZU8M5RriZe3OPealqLK5HoKkLOwg2CJVIA8lvltwvCG6C, DOB: 1991-02-02>]>

   
    
    print "Quotes: ", 
    if "logged" in request.session:
        context = {
            'user': this_user,
            'faves': faves,
            'quotes': Quote.objects.all()
        }
        # print "context: ", context


        return render(request, 'exam2/welcome.html', context)
    return redirect('/main')

def users(request, id):
    if 'logged' not in request.session:
        return redirect('/main')

    this_user = User.objects.get(id=int(id))
    my_quotes = Quote.objects.filter(user=this_user)
    context = {
        'user': this_user,
        'quotes': my_quotes,
        # 'faves': this_user.faved_quotes.all()
    }

    return render(request, 'exam2/users.html', context)


def reg(request):
    print "Start Reg Route"
    if "logged" in request.session:
        print "End Reg Route - Already Logged"
        return redirect('/quotes')
    result = User.objects.reg_validator(request.POST)
    if isinstance(result, dict):
        # print "is a dict (errors):", result
        for tag, error in result.iteritems():
            messages.error(request, error)
        return redirect('/main')
    else:
        # print "result (new_user):", result
        result = int(result.id)
        request.session['logged'] = result
        # print "request.session['logged]:", request.session['logged']
        # print "not a dict (new_user):", User.objects.get(id=request.session['logged'])
        print "End Reg Route - Registered"
        return redirect('/quotes')

def login(request):
    print "Start Login Route"
    if "logged" in request.session:
        return redirect('/quotes')
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
            return redirect('/quotes')

def logout(request):
    print "Start Logout Route"
    try:
        del request.session['logged']
    except KeyError:
        pass
    print "End Logout Route"
    return redirect('/main')

def add(request):
    u = User.objects.get(id = request.session['logged'])
    q = Quote.objects.get(id = request.POST['quote'])
    u.faved_quotes.add(q)
    # print "All faved: ", u.faved_quotes.all()
    return redirect('/quotes')

# quote.id
# request.POST:  <QueryDict: {u'quote': [u'3'], u'csrfmiddlewaretoken': [u'l4n1V3kvvQArP1B4WYr9Niw1nnVvOFEwsgdlGO5TaD2ytzefWnUb7YaY0oaT9e30']}

# user.id - 

# user:  id: 10, name: Charlie, alias: C-Alias, email: c@gmail.com, password: $2b$05$cwTQhxdpK2Wxyp8Gc43Bq..LNyX/OfmDEx80hHj52a4LF1V6hGyQG, DOB: 1991-01-01

# quote:  id: 1, content: The bell it tolls for thee, author: Ernest Hemingway, user: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01

def create(request, id):
    print "Start Create Route"
    print "Request.POS: ", request.POST
    print "Request.id: ", int(id)
    result = Quote.objects.create_validator(request.POST, int(id))
    if isinstance(result, dict):
        # print "result is dict (errors)"
        for tag, error in result.iteritems():
            messages.error(request, error)
        print "End Login Route - Invalid"
        return redirect('/quotes')
    else:
        u = User.objects.get(id = request.session['logged'])
        q = Quote.objects.get(id = int(result.id))
        u.faved_quotes.add(q)

    print "End Create Route"
    return redirect('/users/' + str(id))

def remove(request, id):
    print "Request.id", int(id)
    
    u = User.objects.get(id = request.session['logged'])
    print "u: ", u  
    print "This_user's quotes: ", Quote.objects.filter(id=int(id)) 
    q = u.faved_quotes.get(id = int(id))
    print "q: ", q
    q.faved_users.remove(u)
    print "u.faved.all AFTER DELETE", u.faved_quotes.all() 
    print "This_user's quotes: ", Quote.objects.filter(id=int(id))  
    return redirect('/quotes')

# <QueryDict: {u'content': [u'bbbbbb'], u'csrfmiddlewaretoken': [u'CjAIB8NmgzaOEBSHxuSyHD7RJW4mbVrXJvq2mTyKVmCVi9vSxTlA1jLOmXjKwuQr'], u'author': [u'aaaa']}>
# u:  id: 10, name: Charlie, alias: C-Alias, email: c@gmail.com, password: $2b$05$cwTQhxdpK2Wxyp8Gc43Bq..LNyX/OfmDEx80hHj52a4LF1V6hGyQG, DOB: 1991-01-01


# q:  id: 3, content: I've never seen a wild thing feel sorry for itself, a bird will fall frozen from a bough without ever having felt sorry for itself, author: D.H Lawrence, user: id: 9, name: Bravo, alias: B-Alias, email: b@gmail.com, password: $2b$05$4HeGFu/sZU8M5RriZe3OPealqLK5HoKkLOwg2CJVIA8lvltwvCG6C, DOB: 1991-02-02


# u.faved_quotes.add(q)
# u.faved_quotes.all()

# <QuerySet [<Quote: id: 1, content: The bell it tolls for thee, author: Ernest Hemingway, user: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>]>