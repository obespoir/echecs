# echecs_web_services
棋牌框架的web服务

# 文件结构说明:


# Bluprint 蓝图模块说明
蓝图最基本的意图就是将不同的功能处理模块分在不同的py文件里面编写,通过各自定义的url前缀进行访问
1. 在app.views下建立自己的文件夹
2. 在自己新建立的文件夹的`__init__.py`中初始化蓝图,例如:
```
admin = Blueprint("admin", url_prefix="/admin")
```
3. 建立处理相应功能的`.py`文件,并使用蓝图装饰器装饰你的处理类,例如:
```
@admin.route("/index", name="index")
class HomeHandler(BaseHandler):
    def get(self):
        return self.write("index!")
```
4. 在自己新建立的文件夹的`__init__.py`中引入的的`.py`文件,例如:
```
admin = Blueprint("admin", url_prefix="/admin")
import login_handler
import status_handler
```