from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.

def index(request):
    return HttpResponse("我是子应用的index页面")


def addUser(request):
    # 增加数据
    # 1. save
    # user = User(name="laosan",age=19,gender="nan",height=100,birthday="2019-07-01")
    # user.save()
    # 2. save
    user = User()
    user.name = "laowu"
    user.age = 29
    user.gender = 'nv'
    user.height = 100.00
    user.save()

    # create
    # User.objects.create(name="laosan",age=19,gender="nan",height=100,birthday="2019-07-01")

    params = dict(name="laosan", age=19, gender="nan", height=100, birthday="2019-07-01")
    data = User.objects.create(**params)

    return HttpResponse("增加数据")


def getData(request):
    # 查询
    # all方法
    # data = User.objects.all()
    # # print (data)
    # print (data[0])
    # print (data[0].name)
    # print (data[0].age)
    # for one in data:
    #     print (one)  ## 对象
    #     print (one.name) ## 对象中的属性

    ## get方法
    # data = User.objects.get(id=1)
    # data = User.objects.get(name="laosan")
    # print (data)
    # filter
    # select * from user where name = "xxxx" and age=12;
    # data = User.objects.filter(name="laosan",age=19)
    # print (data)
    # for one in data:
    #     print (one.id)
    # first()
    # data = User.objects.filter(name="laosan").first()
    # print (data)
    # last()
    # data = User.objects.filter(name="laosan").last()
    # print (data)
    # exclude()
    # data = User.objects.exclude(name="laosan",age=19)
    # print (data)
    # for one in data:
    #     print(one.name)

    # data = User.objects.exclude(name="laosan").first()
    # print (data)
    # order_by
    ## 升序
    # data = User.objects.order_by("name","age")
    # data = User.objects.all().order_by("name","age")
    # data = User.objects.exclude(name="laowang").order_by("name","age")
    # print (data)
    # data = User.objects.order_by("name","age").exclude(name="laowang")
    # print (data)
    # ## 逆序
    # data = User.objects.order_by("-id")
    # print(data)
    # reverse
    # data = User.objects.all().order_by("id")
    # print (data)
    data = User.objects.all().order_by("id").reverse()
    # print (data)

    # values
    # data = User.objects.all().values()
    # print (data)
    # for one in data:
    #     print (one["gender"])
    # data = User.objects.all().values("name")
    # print (data)
    # data = User.objects.all().values("name","age")
    # print (data)
    # # exists
    # flag = User.objects.filter(name="xxxxxxxxxxx").exists()
    # print(flag)
    # count
    # num = User.objects.filter(name="laosan").count()
    # print (num)

    # 切片 [1:10]
    #  sql   limit 1 3
    data = User.objects.all()[1:3]
    print(data)

    return HttpResponse("查询数据")


def updateUser(request):
    # 更新操作

    # # save
    # # 1.需要查询数据
    # user = User.objects.filter(id=2).first()
    # # 2.修改实例对象的属性的值
    # user.age= 100
    # # 3. 保存数据  save方法
    # user.save()

    #
    # user = User.objects.get(id=3)
    # user.age = 199
    # user.save()

    user = User.objects.filter(name='laosan')  ## 返回queryset

    for one in user:
        one.age = 20
        one.save()
    # user.save()  ##  报错实例 queryset 没有save方法

    # update
    User.objects.filter(id=4).update(age=95)
    User.objects.filter(name="laosan").update(age=96)
    ## update 方式属于queryset的方法，  如果为对象，不能使用update
    # User.objects.filter(name="laosan").first().update(age=73)   报错实例

    return HttpResponse("更新数据")


def deleteUser(request):
    # 删除数据
    # delete

    # User.objects.filter(id=4).delete()
    User.objects.filter(name="laosan").delete()
    return HttpResponse("删除数据")


def doubleLine(request):
    data = User.objects.filter(id__lt=3).values("name", "id")  ### 取 id < 3 的数据
    print(data)
    data = User.objects.filter(id__lte=3).values("name", "id")  ### 取 id 小于等于 3 的数据
    print(data)
    data = User.objects.filter(id__gt=3).values("name", "id")  ### 取 id 大于 3 的数据
    print(data)

    data = User.objects.filter(id__in=[1, 2, 3, 4, 5, 6]).values("name", "id")  ## 取id 为 1，2,3,4,5,6的数据
    print(data)
    data = User.objects.filter(id__in=[9, 8]).values("name", "id")  ##
    print(data)

    data = User.objects.exclude(id__in=[8, 9]).values("name", "id")  ### 取 id不在 8和9 中的数据
    print(data)
    data = User.objects.filter(name__contains='wa').values("name", "id")  ## 大小写敏感
    print(data)
    data = User.objects.filter(name__icontains="wa").values("name", "id")  ## 大小写不敏感
    print(data)
    data = User.objects.filter(name__startswith="lao").values("name", "id")  ## 大小写敏感  以指定字符开头
    print(data)
    data = User.objects.filter(name__istartswith="lao").values("name", "id")  ## 大小写不敏感   以指定字符开头
    print(data)
    print("-------------------------------------")

    data = User.objects.filter(id__range=(3, 7)).values("name", "id")  #### range  前闭后闭的区间
    print(data)
    data = User.objects.filter(id__range=[3, 7]).values("name", "id")
    print(data)

    return HttpResponse("双下划线语法")


def foreignAdd(request):
    #  增加数据
    #  先增加publish表数据
    # Publish.objects.create(name="北京出版社",address="北京")
    # Publish.objects.create(name="山东出版社",address="山东")
    # Publish.objects.create(name="中公出版社",address="中公")

    #  增加book数据
    # 第一种
    # Book.objects.create(name="python基础",publish_id=1)
    # 第二种
    # publish = Publish.objects.get(name="北京出版社")
    # Book.objects.create(name="python开发", publish_id=publish.id)
    # 第三种
    # publish = Publish.objects.get(name="山东出版社")
    # Book.objects.create(name="pythonWeb",publish=publish)
    # 第四种
    # Book.objects.create(name="pythonWeb", publish=Publish.objects.get(name="中公出版社"))

    ##  正向  从外键所在表到关联表的操作叫正向操作
    # book =Book()
    # book.name = "python数据分析"
    # book.publish = Publish.objects.get(name="中公出版社")
    # book.save()

    ##  反向  从关联表到外键所在的表的操作叫反向操作
    # publish_obj = Publish.objects.get(name="中公出版社")
    # publish_obj.book_set.create(name="python爬虫")

    pub_obj = Publish.objects.create(name="东北出版社", address="东北")
    pub_obj.book_set.create(name="python技术")

    return HttpResponse("一对多增加操作")


def foreignGet(request):
    # 查询
    # 查北京出版社的书籍
    # pub = Publish.objects.get(name="北京出版社")
    # # book = Book.objects.filter(publish_id=pub.id).values("name")
    # book = Book.objects.filter(publish=pub).values("name")
    # print (book)

    ## 查询 python基础的出版社名字
    # book = Book.objects.filter(name="python基础").first()
    # pub = Publish.objects.get(id=book.publish_id)
    # print(pub.name)

    # 正向查询 从 book -》 publish
    # 查 python基础 属于 出版社
    # book = Book.objects.get(name="python基础")
    # # pubname = book.publish.name
    # # print (pubname)
    # pub = book.publish   ## 对象
    # print (pub)

    # 反向查询  从 pub -> book
    ## 查北京出版社的书
    # pub = Publish.objects.get(name="北京出版社")
    # data = pub.book_set.all().values("name")    ###  queryset
    # print (data)

    # 反向查询  从 pub -> book
    ## 查询 北京出版社 出版的 python基础
    # pub = Publish.objects.get(name="北京出版社")
    # data = pub.book_set.filter(name__contains="python").count()
    # print (data)

    #  查询 python基础的出版社出版的所有书籍
    book = Book.objects.get(name="python基础")  ### 查找对象
    pub = book.publish  ## 正向操作  找到该书的出版社
    book_all = pub.book_set.values()  ## 反向操作，找到这个出版社出版的所有书籍
    print(book_all)

    # 查询 python基础的出版社出版的所有书籍
    book_all = Book.objects.get(name="python基础").publish.book_set.values("name")

    return HttpResponse("一对多查询操作")


def foreignUpdate(request):
    # 修改数据   update save
    # 1.save  将python基础的出版社修改为 山东出版社
    # # book= Book.objects.get(name="python基础")
    # pub = Publish.objects.get(name="山东出版社")
    # # book.publish = pub
    # # book.save()
    # #
    # #2. update
    # Book.objects.filter(name="python基础").update(publish=pub)

    # 反向
    ## 修改 publish 下面的书
    ## 北京出版社 增加 好多本书
    pub = Publish.objects.get(name="北京出版社")
    book = Book.objects.filter(name="python基础").first()
    book1 = Book.objects.filter(name="pythonWeb").first()

    pub.book_set.set([book, book1])

    return HttpResponse("一对多修改操作")


def foreignDelete(request):
    # 先删除 外键所在的表
    "python基础"
    # Book.objects.filter(name="python基础").first().delete()
    #
    # # 删除关联表

    book = Book.objects.filter(name="python爬虫").first()
    book.delete()  ## 删除书

    Publish.objects.filter(id=book.publish_id).delete()

    return HttpResponse("一对多删除操作")


def choiceDemo(request):
    # teacher= Teacher(name="老王",gender=1)
    # teacher.save()

    teacher = Teacher.objects.get(id=1)
    print(teacher.gender)
    print(teacher.get_gender_display())

    return HttpResponse("choice demo")


def ManyAdd(request):
    ## 增加老师
    # Teacher.objects.create(name="老刘",gender=1)
    # Teacher.objects.create(name="老边",gender=1)
    # Teacher.objects.create(name="老张",gender=1)
    # Teacher.objects.create(name="小丽",gender=0)

    # 增加 person
    # Person.objects.create(name="小王",age=17,height=170)

    ## 正向操作
    ## 小二  想学 老刘的课
    # teacher = Teacher.objects.get(name="老刘")
    # teacher.person.create(name="小二",age=18,height=190)
    #
    ## 小三  和 小四 想学 女老师的课
    # teacher = Teacher.objects.filter(gender=0).first()
    # person = Person.objects.create(name="小三",age=19,height=150)
    # person1 = Person.objects.create(name="小四",age=20,height=149)
    # teacher.person.add(person,person1)

    ## 反向操作
    ## 小五 想学 老王的课程
    person = Person.objects.create(name="小五", age=29, height=179)
    teacher = Teacher.objects.filter(name="老王").first()
    person.teacher_set.add(teacher)

    return HttpResponse("多对多增加")


def ManyGet(request):
    # 正向
    # 查询 ；老王老师的学生
    teacher = Teacher.objects.filter(name="小丽").first()
    person = teacher.person.all().values("name")
    print(person)
    # 反向
    person = Person.objects.filter(name="小三").first()
    teacher = person.teacher_set.all().values("name")
    print(teacher)

    return HttpResponse("多对多查询")


def ManyUpdate(request):
    ## 更新
    #   set
    ## 老刘
    # teacher = Teacher.objects.filter(name="老刘").first()
    #     # # teacher.person.set([3,4,5])
    #     #
    #     # p1 = Person.objects.filter(name='小三').first()
    #     # p2 = Person.objects.filter(name="小五").first()
    #     # teacher.person.set([p1,p2])

    # person = Person.objects.filter(name="小三").first()
    # person.teacher_set.set([1,2,3,4])
    # person.teacher_set.set([p1,p2,p3,p4])

    return HttpResponse("多对多修改")


def ManyDelete(request):
    ## 删除  delete
    ## 清空表关系   teacher_person
    ## remove  解除关系
    ## 解除小四 和小丽的关系
    ### 正向
    # teacher = Teacher.objects.filter(name="小丽").first()
    # person = Person.objects.filter(name="小四").first()
    # teacher.person.remove(person)    ###    remove(对象/id)

    ## 反向 解除小丽和小三
    # teacher = Teacher.objects.filter(name="小丽").first()
    # person = Person.objects.filter(name="小三").first()
    # person.teacher_set.remove(teacher)

    ## clear   清空  删除小五的所有的关系
    ## 反向
    person = Person.objects.filter(name='小五').first()
    person.teacher_set.clear()
    ## 正向
    teacher = Teacher.objects.filter(name="老刘").first()
    teacher.person.clear()

    ## delete  删除数据
    Person.objects.filter(name="小三").delete()


    return HttpResponse("多对多删除")



from django.db.models import Sum,Avg,Count,Max,Min,F,Q
def juheView(request):
    ##  聚合函数   返回值 默认key  参数名__聚合函数名
    # data = Person.objects.all().aggregate(Count("id"),Count("name"),Avg("age"))
    ## 将聚合函数返回值  更名  修改的是 返回值中的 key
    data = Person.objects.all().aggregate(Count("id"),Count("name"),xxxxxx = Avg("age"))
    print (data)
    print(data["name__count"])

    return HttpResponse("聚合查询")


import random

def FTest(request):

    # for one in range(10):
    #     book = Book()
    #     book.name = "python%s" % one
    #     book.num = one * random.randint(1,100)
    #     book.sell_num = one
    #     book.publish_id =  1
    #     book.save()

    # book = Book.objects.filter(name__startswith="python").all()
    # for one in book:
    #     one.sell_num = random.randint(1,100)
    #     one.save()

    # F 对象
    ## 比较 库存量小于售出量的书
    ## F对象会将后面的字段的值取出来
    data = Book.objects.filter(num__lt = F("sell_num")+10 ).all().values("name")
    print (data)

    return HttpResponse("F test")

def Qtest(request):

    ## 查询 num 大于 10   sell_num 小于100  的书名
    book= Book.objects.filter(num__gt=10,sell_num__lt =100).all().values()

    ## and
    book = Book.objects.filter(Q(num__gt=10) & Q(sell_num__lt =100)).all().values("name")
    ## or
    book = Book.objects.filter(Q(num__gt=10) | Q(sell_num__lt =100)).all().values("name")
    ## not
    ## 查找 num不大于  10 或者   sell_num 不小于 100 的书名
    book = Book.objects.filter(~Q(num__gt=10) | ~Q(sell_num__lt =100)).all().values("name")
    book = Book.objects.filter(~Q(num__gt=10)).all().values("name")
    book = Book.objects.filter(~Q(num__gt=10) & Q(sell_num__lt =100)).all().values("name")

    return HttpResponse("Q test")