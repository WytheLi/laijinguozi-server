from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Person, Province, City


# Create your views here.


class PersonView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = 1
        province_id = 1
        city_id = 1
        # 1、查询用户的出生省市区
        p1 = Person.objects.get(pk=user_id)     # `SELECT "example_person"."id", "example_person"."name", "example_person"."hometown_id", "example_person"."living_id" FROM "example_person" WHERE "example_person"."id" = 1`
        p1.name
        p1.hometown.name    # `SELECT "example_city"."id", "example_city"."name", "example_city"."province_id" FROM "example_city" WHERE "example_city"."id" = 3`
        p1.hometown.province.name   # `SELECT "example_province"."id", "example_province"."name" FROM "example_province" WHERE "example_province"."id" = 1`

        p2 = Person.objects.select_related('hometown__province').get(pk=user_id)    # `SELECT "example_person"."id", "example_person"."name", "example_person"."hometown_id", "example_person"."living_id", "example_city"."id", "example_city"."name", "example_city"."province_id", "example_province"."id", "example_province"."name" FROM "example_person" INNER JOIN "example_city" ON ("example_person"."hometown_id" = "example_city"."id") INNER JOIN "example_province" ON ("example_city"."province_id" = "example_province"."id") WHERE "example_person"."id" = 1`
        p2.name
        p2.hometown.name
        p2.hometown.province.name

        # 2、查询用户的出生信息 & 居住信息
        p3 = Person.objects.select_related('hometown__province').select_related('living__province').get(pk=user_id)     # `SELECT "example_person"."id", "example_person"."name", "example_person"."hometown_id", "example_person"."living_id", "example_city"."id", "example_city"."name", "example_city"."province_id", "example_province"."id", "example_province"."name", T4."id", T4."name", T4."province_id", T5."id", T5."name" FROM "example_person" INNER JOIN "example_city" ON ("example_person"."hometown_id" = "example_city"."id") INNER JOIN "example_province" ON ("example_city"."province_id" = "example_province"."id") INNER JOIN "example_city" T4 ON ("example_person"."living_id" = T4."id") INNER JOIN "example_province" T5 ON (T4."province_id" = T5."id") WHERE "example_person"."id" = 1`
        p3.name, p2.hometown.name, p2.hometown.province.name

        # 3、查询用户旅游过的城市
        cities = p1.visitation.all()    # `SELECT "example_city"."id", "example_city"."name", "example_city"."province_id" FROM "example_city" INNER JOIN "example_person_visitation" ON ("example_city"."id" = "example_person_visitation"."city_id") WHERE "example_person_visitation"."person_id" = 1`
        [(city.province.name, city.name) for city in cities]

        p4 = Person.objects.prefetch_related("visitation__province").get(pk=1)      # 通过向上递进的查询，在内存中构建一张结果表，后续直接在结果表中拿结果
        cities = p4.visitation.all()    # 未执行SQL
        [(city.province.name, city.name) for city in cities]    # 未执行SQL

        # 4、related_name参数
        # 4.1、查询省份下的所有城市（一对多的关系）
        province = Province.objects.get(pk=province_id)
        province.cities.all()   # 以City为主表，查询属于province_id的所有城市

        # 4.2、查询某个城市旅游过的人
        city = City.objects.get(pk=city_id)
        city.visitor.all()  # 以Person为主表，关联Relation表，查询所有在city_id旅游过的人

        return Response({'code': 200, 'msg': 'success.'})