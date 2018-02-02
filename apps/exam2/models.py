from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[^\W_]+(-[^\W_]+)?$', re.U)

class UserManager(models.Manager):
    def login_validator(self, postData):
        print "Start Login Manager"
        errors = {}
        if len(User.objects.filter(email=postData['email'])) > 0:
            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['regPW'] = "Password is incorrect"
                print "End Login Manager - Password Invalid"
                return errors
            else:
                print "End Login Manager - Validated"
                return user
        else:
            errors['regEmail'] = "Email not registered"
            # print "regEmail errors: ", errors
            print "End Login Manager"
            return errors

    def reg_validator(self, postData):
        print "Start Reg Manager"
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Name must be at least two characters"
            # print "errors name:", errors
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias must be at least two characters"
            # print "errors at alias:", errors
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "email is invalid"
            # print "errrors at email", errors
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
            # print "errors at password:", errors
        if postData['password'] != postData['confirmPW']:
            errors['confirm'] = "Password does not match confirm password"
            # print "errors at confirm:", errors
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email2'] = "Email already registered"
            # print "errors at email2", errors
        if len(postData['DOB']) < 10:
            errors['DOB'] = "Please enter your date of birth"
            # print "DOB error:", errrors
        if errors:
            # print "Total errors:", errors
            return errors
        else:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))
            print hashed
            new_user = {'new_user': 'Alpha'}
            new_user = self.create(
                name=postData['name'],
                alias=postData['alias'],
                email=postData['email'],
                password=hashed,
                DOB =postData['DOB'],
            )
            print "new_user:", new_user
        print "End Reg Manager"
        return new_user


    def create_validator(self, postData, id):
        # print postData
        # print id
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "Author name must be at least 3"
        if len(postData['content']) < 10:
            errors['content'] = "Quote must be at least 10 characters"
        if errors:
            print "Total Errors: ", errors 
            return errors
        else:
            new_quote = self.create(
                content=postData['content'],
                author=postData['author'],
                user=User.objects.get(id=int(id)),

            )
            return new_quote

class User(models.Model):
    print "Start User Model"
    name = models.CharField(max_length=255, blank=False)
    alias = models.CharField(max_length=255, blank=False)
    email = models.URLField(blank=False)
    password = models.CharField(max_length=255)
    DOB = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    print "End User Model"
    def __unicode__(self):
        return "id: " + str(self.id) + ", name: " + str(self.name) + ", alias: " + str(self.alias) + ", email: " + str(self.email) + ", password: " + str(self.password) + ", DOB: " + str(self.DOB)

class Quote(models.Model):
    print "Start User Model"
    content = models.CharField(max_length=255, blank=False)
    author = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, related_name="quotes", null=True)
    faved_users = models.ManyToManyField(User, related_name="faved_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    print "End User Model"  
    def __unicode__(self):
        return "id: " + str(self.id) + ", content: " + str(self.content) + ", author: " + str(self.author) + ", user: " + str(self.user)

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


# User.objects.create(name="Alpha", alias="A-Alias", email="a@gmail.com", password=bcrypt.hashpw(('aaaaaaaa'.encode()), bcrypt.gensalt(5)), DOB="1991-01-01")

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