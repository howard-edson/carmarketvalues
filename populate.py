import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmv_project.settings")
from cmv_app.models import Region, Search
from django.contrib.auth.models import User
import random

def populate():
    
    users=[add_user("user1", 123),add_user("user2",123),add_user("user3",123)]
    
    regions=[add_region("seattle")]
    
    for (user,region) in zip(users,regions):
        for i in range(6):
            s=Search(user=user,**random_generators())
            s.save()
            print "search is ",s
            print "region is ", region
            s.regions.add(region)
            s.save()
        
    
    # Print out what we have added to the user.
    for c in Search.objects.all():
        print c

def add_user(name,password):
    user, created = User.objects.get_or_create(username=name)
    if created:
        user.set_password(password)
        user.save()
    return user

def add_region(name):
    r=Region.objects.get_or_create(name=name)
    return r[0]

def random_generators():
    vehicle_choice=random.choice([("honda","crv"),("toyota","corolla"),
                                 ("nissan","leaf"),("ford","mustang")])
    kwargs={
    'min_year':random.randrange(1985,1990),
    'max_year':random.randrange(1991,2013),
    'min_price':random.randint(5,30) * 100,
    'max_price':random.randint(40,100) * 100,
    'vehicle_make':vehicle_choice[0],
    'vehicle_model':vehicle_choice[1],
     'pic_only':random.choice([True,False]),
     'search_title_only':random.choice([True,False]), 
     'seller_type':random.choice(Search.SELLER_TYPE_CHOICES)[0]
    }
    
    return kwargs
    
# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmv_project.settings')
    populate()
