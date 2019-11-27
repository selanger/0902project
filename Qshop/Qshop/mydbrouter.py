## 重写 数据库的路由配置

##    db_for_read   读要使用的库
##    db_for_write    写要使用的库

import random
class Router(object):
    def db_for_read(self, model, **hints):
        # return "slave"


        db_list = ["slave2","slave"]
        return random.choice(db_list)



    def db_for_write(self, model, **hints):

        # return "default"

        db_list = ["master1", "default"]
        return random.choice(db_list)