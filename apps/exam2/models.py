from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import date




EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[^\W_]+(-[^\W_]+)?$', re.U)

class UserManager(models.Manager):
    def login_validator(self, postData):
        print "Start Login Manager"
        errors = {}
        if len(User.objects.filter(username=postData['username'])) > 0:
            user = self.filter(username=postData['username'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['regPW'] = "Password is incorrect"
                print "End Login Manager - Password Invalid"
                return errors
            else:
                print "End Login Manager - Validated"
                return user
        else:
            errors['username'] = "username not registered"
            print "username errors: ", errors
            print "End Login Manager"
            return errors

    def reg_validator(self, postData):
        print "Start Reg Manager"
        errors = {}
        if len(User.objects.filter(username=postData['username'])) > 0:
            errors['email2'] = "Username already registered"
            # print "errors at email2", errors
        if len(postData['name']) < 3:
            errors['name'] = "Name must be at least three characters"
            # print "errors name:", errors
        if len(postData['username']) < 3:
            errors['username'] = "Username must be at least three characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
            # print "errors at password:", errors
        if postData['password'] != postData['confirmPW']:
            errors['confirm'] = "Password does not match confirm password"
            # print "errors at confirm:", errors
        if errors:
            # print "Total errors:", errors
            return errors
        else:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))
            print hashed
            new_user = self.create(
                name=postData['name'],
                username=postData['username'],
                password=hashed,
            )
            print "new_user:", new_user
        print "End Reg Manager"
        return new_user

    # def date_validator(self):
    # return date.today() > self.date
        
        

    def create_validator(self, postData, id):
        print "Start Create validator"
        print "date.today():", date.today()
        # 2018-02-02
        print "postData['start_date']:", unicode(postData['start_date'])
        # 1991-01-01
        print "postData['end_date']:", postData['end_date']
        # 1992-01-01
        # dateValue = date( 2010, 5, 15 )   
        # print "dateValue", dateValue
        start_date = unicode(postData['start_date'])
        date_today = unicode(date.today())
        end_date = unicode(postData['end_date'])
        errors = {}
        if len(postData['description']) < 1:
            errors['description'] = "Please provide a description"
        if len(postData['destination']) < 1:
            errors['destination'] = "Please provide a destination"
        if len(postData['start_date']) < 8:
            errors['start_date'] = "Please provide a start date"
        if len(postData['end_date']) < 8:
            errors['end_date'] = "Please provide an end date"
        if start_date <= date_today:
            errors['start_date'] = "Start date must be in the future"
        if end_date < start_date:
            errors['end_date'] = "End date must be after the start date"
        if errors:
            print "Total Errors: ", errors
            print "End Create Validator - Errors" 
            return errors
        
        new_trip = self.create(
            destination=postData['destination'],
            description=postData['description'],
            user=User.objects.get(id=int(id)),
            start_date=postData['start_date'],
            end_date=postData['end_date'],
        )
        print "End Create Validator", new_trip
        return new_trip

class User(models.Model):
    print "Start User Model"
    name = models.CharField(max_length=255, blank=False)
    username = models.CharField(max_length=255, blank=False)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

    print "End User Model"
    def __unicode__(self):
        return "id: " + str(self.id) + ", name: " + str(self.name) + ", username: " + str(self.username) + ", password: " + str(self.password) + ", created_at: " + str(self.created_at)

# User.objects.create(name="Alpha", username="Alpha-Username", password=bcrypt.hashpw(('aaaaaaaa'.encode()), bcrypt.gensalt(5)))
# <User: id: 16, name: Alpha, username: Alpha-Username, password: $2b$05$t1eteLK62j7SBX86jO2bou4QsBkmyCMq/r00xJ94qgIK/dzgM20eC>

# User.objects.create(name="Bravo", username="Bravo-Username", password=bcrypt.hashpw(('bbbbbbbb'.encode()), bcrypt.gensalt(5)))
# <User: id: 17, name: Bravo, username: Bravo-Username, password: $2b$05$RPLyuS52ZipTPoCikm6XzOMCa5Cq5r9xIKwRPbvPwg3SvJKOM9AA2>

class Trip(models.Model):
    print "Start User Model"
    destination = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, related_name="trips", null=True)
    trip_users = models.ManyToManyField(User, related_name="trip_trips")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    objects = UserManager()
    print "End User Model"  
    def __unicode__(self):
        return "id: " + str(self.id) + ", destination: " + str(self.destination) + ", description: " + str(self.description) + ", user: " + str(self.user) + ", start_date: " + str(self.start_date) + ", end_date: " + str(self.end_date)

# Trip.objects.create(destination="Hong Kong", description="We're goin to the great wall", user=User.objects.get(id=16), start_date="2018-03-03", end_date="2018-04-04")

# <Trip: id: 2, destination: Hong Kong, description: We're goin to the great wall, user: id: 16, name: Alpha, username: Alpha-Username, password: $2b$05$t1eteLK62j7SBX86jO2bou4QsBkmyCMq/r00xJ94qgIK/dzgM20eC, created_at: 2018-02-02, start_date: 2018-03-03, end_date: 2018-04-04>


# Trip.objects.create(destination="The Zoo", description="We're goin to the zoo", user=User.objects.get(id=17), start_date="2018-03-03", end_date="2018-04-04")
# <Trip: id: 3, destination: The Zoo, description: We're goin to the zoo, user: id: 17, name: Bravo, username: Bravo-Username, password: $2b$05$RPLyuS52ZipTPoCikm6XzOMCa5Cq5r9xIKwRPbvPwg3SvJKOM9AA2, created_at: 2018-02-02, start_date: 2018-03-03, end_date: 2018-04-04>

# u = User.objects.get(id=17)
# q = Trip.objects.get(id=2)
# u.trip_trips.add(q)

# u.trip_trips.all()

# <QuerySet [<Trip: id: 2, destination: Hong Kong, description: We're goin to the great wall, user: id: 16, name: Alpha, username: Alpha-Username, password: $2b$05$t1eteLK62j7SBX86jO2bou4QsBkmyCMq/r00xJ94qgIK/dzgM20eC, created_at: 2018-02-02, start_date: 2018-03-03, end_date: 2018-04-04>]>
































# this_quote = Quote.objects.get(id=2)
# this_user = User.objects.get(id=6)
# this_quote.favored_users.add(this_user)
# /////////////////////////
# class User(models.Model):
# 	title = models.CharField(max_length=255)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)
# class Quote(models.Model):
# 	name = models.CharField(max_length=255)
# 	users = models.ManyToManyField(User, related_name="quotes")
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)



# <User: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>
# a = User.objects.get(id=8)
# a.delete()

# User.objects.create(name="Bravo", alias="B-Alias", email="b@gmail.com", password=bcrypt.hashpw(('bbbbbbbb'.encode()), bcrypt.gensalt(5)), DOB="1991-02-02")

# <User: id: 9, name: Bravo, alias: B-Alias, email: b@gmail.com, password: $2b$05$4HeGFu/sZU8M5RriZe3OPealqLK5HoKkLOwg2CJVIA8lvltwvCG6C, DOB: 1991-02-02>
# b = User.objects.get(id=9)
# b.delete

# Quote.objects.create(content="The bell it tolls for thee", author="Ernest Hemingway", user=User.objects.get(id=8))

# <Quote: id: 1, content: The bell it tolls for thee, author: Ernest Hemingway, user: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>

# a = Quote.objects.get(id=1)
# a.delete()
# /////////////////////////////
#Quote.objects.create(content="I've never seen a wild thing feel sorry for itself, a bird will fall frozen from a bough without ever having felt sorry for itself", author="D.H Lawrence", user= User.objects.get(id=9))

# <Quote: id: 3, content: I've never seen a wild thing feel sorry for itself, a bird will fall frozen from a bough without ever having felt sorry for itself, author: D.H Lawrence, user: id: 9, name: Bravo, alias: B-Alias, email: b@gmail.com, password: $2b$05$4HeGFu/sZU8M5RriZe3OPealqLK5HoKkLOwg2CJVIA8lvltwvCG6C, DOB: 1991-02-02>

# u = User.objects.get(id=8)

# <User: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>

# q = Quote.objects.get(id=3)

# u.faved_quotes.add(q)
# u.faved_quotes.all()
# <QuerySet [<Quote: id: 3, content: I've never seen a wild thing feel sorry for itself, a bird will fall frozen from a bough without ever having felt sorry for itself, author: D.H Lawrence, user: id: 9, name: Bravo, alias: B-Alias, email: b@gmail.com, password: $2b$05$4HeGFu/sZU8M5RriZe3OPealqLK5HoKkLOwg2CJVIA8lvltwvCG6C, DOB: 1991-02-02>]>



# <Quote: id: 1, content: The bell it tolls for thee, author: Ernest Hemingway, user: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>

# u = User.objects.last

# <User: id: 9, name: Bravo, alias: B-Alias, email: b@gmail.com, password: $2b$05$4HeGFu/sZU8M5RriZe3OPealqLK5HoKkLOwg2CJVIA8lvltwvCG6C, DOB: 1991-02-02>

# u.faved_quotes.add(q)
# u.faved_quotes.all()

# <QuerySet [<Quote: id: 1, content: The bell it tolls for thee, author: Ernest Hemingway, user: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>]>

# this_user = User.objects.get(id=9)
# this_user.faved_quotes.all()
# {{ in a template - this_user.quotes.all }}

# <QuerySet [<Quote: id: 1, content: The bell it tolls for thee, author: Ernest Hemingway, user: id: 8, name: Alpha, alias: A-Alias, email: a@gmail.com, password: $2b$05$EVBNiDIDzGajcjH.WaYZI.4vuzy.dy2dydPP/BiZOvl85KDSwORpi, DOB: 1991-01-01>]>

# this_quote = Quote.objects.get(id=1)
# this_user = User.objects.get(id=9)

# this_quote.faved_users.all()
# <QuerySet [<User: id: 9, name: Bravo, alias: B-Alias, email: b@gmail.com, password: $2b$05$4HeGFu/sZU8M5RriZe3OPealqLK5HoKkLOwg2CJVIA8lvltwvCG6C, DOB: 1991-02-02>]>

# this_book.publishers.all()