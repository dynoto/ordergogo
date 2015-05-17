from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.models import Token
from generic.models import Category
from member.models import Member, MemberCategory
from location.models import Address, Area

class Command(BaseCommand):
    def handle(self, *args, **options):
        member = Member.objects.create_superuser(
            username='root',
            password='root',
            email='root@beer.com',
            phone='123'
            )

        bidderone = Member.objects.create_superuser(
            username='bidderone',
            password='bidderone',
            email='bidder@one.com',
            phone='345'
            )

        biddertwo = Member.objects.create_superuser(
            username='biddertwo',
            password='biddertwo',
            email='bidder@two.com',
            phone='456'
            )

        Token.objects.create(user=bidderone)
        Token.objects.create(user=biddertwo)
        token = Token.objects.create(user=member,key='fa97ba8257bd480850c9f72fba6609e28acd619c')

        area = Area.objects.create(
            area_name='Bukit Batok'
            )

        address = Address.objects.create(
            address_name='The Elitist',
            address_line_1='25 Bukit Batok Crescent',
            address_line_2='#09-12',
            postal_code='658101',
            owner=member,
            area =area
            )

        cat_1 = Category.objects.create(title='Robbing')
        cat_2 = Category.objects.create(title='Fishing')


        MemberCategory.objects.create(member=member,category=cat_1)
        MemberCategory.objects.create(member=member,category=cat_2)

        MemberCategory.objects.create(member=bidderone,category=cat_1)
        MemberCategory.objects.create(member=bidderone,category=cat_2)
        MemberCategory.objects.create(member=biddertwo,category=cat_1)

