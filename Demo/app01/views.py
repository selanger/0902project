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
    #2. save
    user =User()
    user.name = "laowu"
    user.age = 29
    user.gender='nv'
    user.height = 100.00
    user.save()

    # create
    # User.objects.create(name="laosan",age=19,gender="nan",height=100,birthday="2019-07-01")

    params = dict(name="laosan",age=19,gender="nan",height=100,birthday="2019-07-01")
    data=User.objects.create(**params)





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
    print (data)

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

    data = User.objects.filter(id__lt = 3).values("name","id")    ### 取 id < 3 的数据
    print (data)
    data = User.objects.filter(id__lte = 3).values("name","id")   ### 取 id 小于等于 3 的数据
    print (data)
    data = User.objects.filter(id__gt = 3).values("name","id")   ### 取 id 大于 3 的数据
    print (data)

    data = User.objects.filter(id__in = [1,2,3,4,5,6]).values("name","id")   ## 取id 为 1，2,3,4,5,6的数据
    print (data)
    data = User.objects.filter(id__in = [9,8]).values("name","id")   ##
    print (data)

    data = User.objects.exclude(id__in = [8,9]).values("name","id")   ### 取 id不在 8和9 中的数据
    print(data)
    data = User.objects.filter(name__contains='wa').values("name","id")   ## 大小写敏感
    print (data)
    data = User.objects.filter(name__icontains="wa").values("name","id")  ## 大小写不敏感
    print (data)
    data = User.objects.filter(name__startswith="lao").values("name","id")   ## 大小写敏感  以指定字符开头
    print (data)
    data = User.objects.filter(name__istartswith="lao").values("name","id")  ## 大小写不敏感   以指定字符开头
    print (data)
    print ("-------------------------------------")

    data = User.objects.filter(id__range = (3,7)).values("name","id")    #### range  前闭后闭的区间
    print (data)
    data = User.objects.filter(id__range = [3,7]).values("name","id")
    print (data)

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

    pub_obj = Publish.objects.create(name="东北出版社",address="东北")
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
    pub = Publish.objects.get(name="北京出版社")
    data = pub.book_set.filter(name__contains="python").count()
    print (data)

    return HttpResponse("一对多查询操作")

def foreignUpdate(request):
    return HttpResponse("一对多修改操作")

def foreignDelete(request):
    return HttpResponse("一对多删除操作")


















