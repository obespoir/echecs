

​	echecs是一款个人基于obEspoir框架开发的多人自定义麻将，该麻将和传统的各类app地方麻将不同，其能够最大化支持人数、牌花色、胡牌玩法等各类自定义配置，以类分子的规则思路尽量使用一套服务端代码可以适配出几十几百款地方麻将，改变当前开发周期极长的传统麻将后台开发模式。


# 一. 安装部署

## 1. 对接obespoir框架修改部分

### 1）配置文件

三种类型的节点(proxy, route, service)每种启动一个节点，当然也可以启动多个，每个节点自己的配置文件；

示例配置文件在echecs_espoir/下，分别为proxy_config.json, route_config.json, service_config.json，配置的核心配置项有：

```json
"host": "监听的主机地址",
"type": "名称",
"api_path": "api加载库路径",   // api 路径，如proxy节点为proxy.include_libs， include_libs中加载自定义的接口库
"available_way": "local",   // 高可用性配置使用哪种方式存储： local（本地文件存储）, mongo(mongodb存储)

"remote_ports": [     // 希望与之建立rpc连接的远程节点配置
    {
        "host": "127.0.0.1",
        "port":  21002,
        "token": "helloworldiloveyou~1234567890123",
        "encode": 0,
        "type": "route"                      // 节点类型(字符串标识)
    }
],
"websocket": {          // 节点websocket服务相关配置
    "port": 20000,
    "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 websocket通信
    "encode": 0,                                      // 是否启用加密
    "timeout": 300,                                   //多久连接超时（单位为秒）
    "no_state": {            // 无状态的消息ID
      "range": [[0, 100000]],
        "special": []       // like "game": [110119]
    }
},
"http": {              // 节点监听的http服务相关配置
    "port": 20001,
    "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 httpserver web通信
    "encode": 0                                       // 是否启用加密
},
"rpc": {         // 节点监听的rpc服务相关配置
    "port": 20002,
    "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 rpc通信
    "encode": 0,                                      // 是否启用加密
    "type": "proxy",                                   // 节点类型
    "reconnect_time": 5                              // 连接断开时重连时间间隔，默认最多重试3次
}
```

### 2）自定义接口

​	针对于不同的websocket，http, rpc消息，不同产品的业务请求一般差异较大，游戏内部自定义的消息处理接口，可以放在对应的proxy, route, service目录下（当然也可以放其他地方，只需要更改上文配置中的api_path即可）。

​	如route节点目录下有：

​		include_libs.py : 集中import服务端自定义的消息处理接口，进行接口注册

​		rpc_handler.py: 自定义的rpc消息处理接口

​		http_handler.py: 自定义的http消息处理接口

​		ws_handler.py: 自定义的http消息处理接口

​	proxy, service节点与此类似。

## 2. 部署及启动

### 1）项目目录

​	麻将项目服务端代码分为两个部分，一部分负责游戏逻辑（websocket长连接方式）；另一部分为大厅逻辑，采用的是基于tornado框架的web服务。

​	代码分别为：

​	echecs_espoir:    游戏主体代码（基于obEspoir框架， websocket长连接）

​	echecs_hall:  游戏大厅代码 （基于tornado框架，http web服务）

​	客户端代码为：

​	echecs_client:  客户端js代码  （基于egret框架，js代码由框架的ts语言发布打包自动生成）

### 2）启动步骤

#### 	echecs_hall

​	启动echecs_hall前需要修改echecs_hall/config.jni配置（mysql和redis的连接地址），然后启动：

```shell
python manager.py     # 启动主程序
python test/test_api.py     # 只在第一次执行，作用是初始化游戏需要的配置（test_init_room_cfg），写入mysql数据库
```

#### 	echecs_espoir

​		注意如果在pycharm中打开该项目，建议最好echecs_hall和echecs_espoir分开打开，这样不会包路径问题（运行时可以找到，多个项目时pycharm本身提示可能会出问题）

​		启动命令如下：

```shell
python start_proxy.py
python start_route.py
python start_service.py
```

#### 	echecs_client

​	因为该游戏demo版本目前是通过浏览器访问的，此处暂时使用nginx做一个简单的http前端服务器代理，nginx示例配置如下：

```ini
server {
        listen       8083 default_server;
        listen       [::]:8083 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        #include /etc/nginx/default.d/*.conf;

        location / {
            root   /data/source/echecs_client;      #
            index index.php index.html index.htm;   #
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
```

​	启动nginx后，即可在浏览器端通过nginx所在的服务器ip和端口进入游戏了，效果图如下：

![login](doc/login.jpg)

大厅界面：

![大厅界面](doc/大厅界面.jpg)

牌局界面：

![牌局界面](doc/牌局界面.jpg)

系统提示界面：

![提示界面](doc/提示界面.jpg)

邮件界面：

![邮件界面](doc/邮件界面.jpg)

# 二. obEspoir游戏框架介绍

obEspoir框架此处制作简单介绍，详情请参考：

github:  https://github.com/obespoir/obEspoir.git

码云：https://gitee.com/jamon/obEspoir.git

## 1. 框架架构及通信流程

​	obespoir 是一款个人独立开发的彻底分布式的开源游戏框架，主要基于python3.7 进行开发，采取了 asyncio,uvloop 等异步编程技术，保障高性能的同时，从框架层面彻底解决生产环境中单节点或服务的高可用需求问题。

该框架的主要特点如下：

1. 支持动态热更新：通过嵌入 http 接口实现游戏内各类型节点的实时更新，支持配置文件和数据库等多种方式；
2. 自适应高可用：框架中的每一个节点可根据需求动态添加或删除，任何节点发生故障无需停服，框架会自动发现合适的节点维持业务运行；
3. 性能卓越：基于异步 asyncio, uvloop 等优秀三方库开发，并发性能接近于 golang, c等编译型语言, 普通单机并发可达到万数量级；
4. 安全可靠：节点间根据配置进行分层权限管理，有效应对 DDOS 瘫痪全局节点；高效 rpc 通信加密机制，防止数据伪造及篡改；
5. 跨平台：提供 websocket 连接服务，支持客户端 h5 游戏引擎开发，一份代码适用移动端，PC 端，浏览器等各终端。

​	在麻将游戏中，应用obEspoir框架后的游戏总体分布式架构图如下：

![kuangjia](doc/kuangjia.jpg)

​		client： 客户端，即玩家用户，游戏中客户端和服务端之间的连接是长连接，客户端和服务端的proxy节点进行连接；

​		proxy：服务端的代理节点，其主要任务是负责消息打包和解包，加解密，然后将合法的消息转发向后端节点。proxy节点地址对公网开发(客户端通过域名和端口连接)；

​		route: 服务端的消息分发节点（路由节点）。该节点根据消息请求id将不同的消息分发到不同的子节点中进行处理，如长沙麻将分发到长沙麻将的游戏节点处理，广东麻将分发到广东麻将节点处理，该类型节点一般不对公网开放；

​		service: 游戏节点，各类型的游戏，如csmj(长沙麻将)，gdmj(广东麻将), xzmj(血战)等。此类节点为游戏主逻辑节点。

## 2. 框架示例demo

框架详细说明可参考： https://gitee.com/jamon/obEspoir.git

### 1） 使用环境

```wiki
1. 代码基于python3.7进行开发，请预先装好相应环境；
2. 有使用到三方库ujson, pymongo(如果配置不用mongo可不装)
```

### 2）使用说明

安装步骤：

```shell
pip3 install -i https://pypi.python.org/simple obEspoir
```

引入该框架需要对接以下几处地方：

### 3)  配置文件

​	配置文件采用json格式，每一个节点（进程）有一个自己的配置文件，配置文件里包括该节点监听的各类端口，日志的目录，连接的数据库地址，连接加密密码、路由信息等等。

​	其中rpc接口部分需要配置哪些消息需要转发，又需要转发往哪些节点，支持两种方式：：

```json
"route": {                     //配置消息转发的路由
            "range": {
                "route": [[0, 5000]], "service": [[5001, 1000000]]
            },
            "special": {
                "route":  [1000] // like "proxy": [110119]
            }
        }
1. 消息ID范围：range中说明哪些范围段内的消息往哪类型节点发，比如上述[0,5000] 发往route类型节点（如果本节点就是route类型，则本地处理），[5001, 10000]内的消息发往service类型节点;
2. 具体的消息ID：special中可以具体写明哪些指定的消息发往哪个节点，如1000消息发往route处理，如果该部分和range冲突，以special配置优先；
```

总体配置信息参考如下：

proxy类型节点：

```json
{
    "log_level": "debug",                                        // 日志级别
    "name": "proxy_1",                                           // 节点名称
    "log_dir": "logs/obEspoir/",                           // 项目运行日志存放目录（不同测试环境目录不同）

    "host": "127.0.0.1",
    "type": "proxy",
    "api_path": "proxy.include_libs",   // api 路径, 项目启动时导入自定义的各类api模块的地方
    "available_way": "local",   // 高可用性配置使用哪种方式存储： local（本地文件存储，默认方式）, mongo(mongodb存储)
    "mongo_uri":"mongodb://test:xxxx@xxxx.mongodb.rds.aliyuncs.com:3717,xxxx.mongodb.rds.aliyuncs.com:3717/admin",       // 如果使用了MongoDB作为存储，则该项需要配置
    "remote_ports": [       //需要连接的远程rpc端口信息
        {
            "host": "127.0.0.1",
            "port":  21002,
            "token": "helloworldiloveyou~1234567890123",
            "encode": 0,
            "type": "route"                      // 节点类型(字符串标识)
        }
    ],
    "websocket": {           // 本地监听的websocket端口配置
        "port": 20000,
        "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 websocket通信
        "encode": 0,                                      // 是否启用加密
        "timeout": 300,                                   //多久连接超时（单位为秒）
        "no_state": {            // 无状态的消息ID
          "range": [[0, 100000]],
            "special": []       // like "game": [110119]
        }
    },
    "http": {						// 本地监听的http端口信息
        "port": 20001,
        "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 httpserver web通信
        "encode": 0                                       // 是否启用加密
    },
    "rpc": {           // 本地监听的rpc端口信息
        "port": 20002,
        "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 rpc通信
        "encode": 0,                                      // 是否启用加密
        "type": "proxy",                                   // 节点类型
        "reconnect_time": 5                              // 连接断开时重连时间间隔，默认最多重试3次
    }
}
```

route路由类型节点参考配置（大多和proxy相同）：

```json
{
    "log_level": "debug",                                        // 日志级别
    "name": "route_1",                                     // 项目名称
    "log_dir": "logs/obEspoir/",                            // 项目运行日志存放目录（不同测试环境目录不同）

    "host": "127.0.0.1",
    "type": "route",
    "api_path": "route.include_libs",   // api 路径
    "http": {
        "port": 21001,
        "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 httpserver web通信
        "encode": 0                                       // 是否启用加密
    },
    "rpc": {
        "port": 21002,
        "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 rpc通信
        "encode": 0,                                      // 是否启用加密
        "type": "game",                                   // 节点类型

        // rpc会收到三类消息：待本地处理消息、待转发的消息、待直接推送到websocket client的消息
        "route": {                     //配置消息转发的路由
            "range": {
                "route": [[0, 5000]], "service": [[5001, 1000000]]
            },
            "special": {
                "route":  [1000] // like "proxy": [110119]
            }
        }
    },

    "remote_ports": [
        {
            "host": "127.0.0.1",
            "port":  20002,
            "token": "helloworldiloveyou~1234567890123",
            "encode": 0,
            "type": "proxy"                      // 节点类型(字符串标识)
        },
        {
            "host": "127.0.0.1",
            "port":  22002,
            "token": "helloworldiloveyou~1234567890123",
            "encode": 0,
            "type": "service"                      // 节点类型(字符串标识)
        }
    ]


}
```

service业务节点参考配置(大多和proxy相同)：

```json
{
    "log_level": "debug",                                        // 日志级别
    "name": "service_1",                                     // 项目名称
    "log_dir": "logs/obEspoir/",                            // 项目运行日志存放目录（不同测试环境目录不同）

    "host": "127.0.0.1",
    "type": "service",
    "api_path": "service.include_libs",   // api 路径
    "http": {
        "port": 22001,
        "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 httpserver web通信
        "encode": 0                                       // 是否启用加密
    },
    "rpc": {
        "port": 22002,
        "token": "helloworldiloveyou~1234567890123",      // 32位秘钥 rpc通信
        "encode": 0,                                      // 是否启用加密
        "type": "service",                                   // 节点类型

        // rpc会收到三类消息：待本地处理消息、待转发的消息、待直接推送到websocket client的消息
        "route": {                     //配置消息转发的路径
            "range": {
                "service": [[5001, 1000000]]
            },
            "special": {
                            // like "proxy": [110119]
            }
        }
    },

    "remote_ports": [
        {
            "host": "127.0.0.1",
            "port":  21002,
            "token": "helloworldiloveyou~1234567890123",
            "encode": 0,
            "type": "route"                      // 节点类型(字符串标识)
        }
    ]


}
```

### 4) 示例自定义接口

​	实际的应用中我们可以根据需要定制不同节点的接口服务，包括rpc接口消息处理，http接口消息处理，websocket接口消息处理。最后将自定义的三类接口文件在配置文件中的“api_path”对应的文件中导入即可，如：

![image-自定义接口导入.jpg](/Users/jamon/data/source/obEspoir/doc/自定义接口导入.jpg)

#### a. http接口

​	每个节点都可以对外提供http服务，收到不同的http服务请求，然后调用不同的处理方法，比如可以做服务端热更新，或者用来不同模块间实时更新用户个人信息。

​	参考自定义接口文件http_handler.py写法：

```python
from aiohttp import web

from obespoir.httpserver.route import HttpHandler
from obespoir.server.server import Server


@HttpHandler("/")
async def index(request):
    return web.Response(body="hello", content_type="text/html")


@HttpHandler("/update_remote_rpc_config")
async def update_remote_rpc_config(request):
    await Server().update_remote_rpc_config()
    return web.Response(body="ok~", content_type="text/html")
```

#### b. rpc接口

​	每个节点同时也可以对外支持rpc服务，收到不同的rpc调用请求，调用不同的处理方法，实际处理的自定义接口，参考写法如下(rpc_handler.py，文件名和include_libs.py中import路径保持一致即可)：

```python
from obespoir.base.common_define import NodeType
from obespoir.base.ob_handler import BaseHandler, RegisterEvent
from obespoir.rpcserver.push_lib import push_message
from obespoir.share.ob_log import logger


@RegisterEvent(100002)
class LoginHandler(BaseHandler):

    async def execute(self, *args, **kwargs):
        logger.info("login_handler:{}  {}".format(args, kwargs))
        user_id = self.params.get("user_id", -1)
        passwd = self.params.get("passwd", "")
        if -1 == user_id or not passwd:
            return {}
        # ...
        pass
        return {"code": 200, "data": {}}


@RegisterEvent(100130, need_return=False)
class OfflineHandler(BaseHandler):

    async def execute(self, *args, **kwargs):
        logger.info("offline: {}, {}".format(args, kwargs))
        pass
        return {"code": 200}


@RegisterEvent(10000, need_return=True)
class HeartBeatHandler(BaseHandler):

    async def execute(self, *args, **kwargs):
        logger.info("heartbeat: {}, {}".format(args, kwargs))
        pass
        return {"code": 200}
```

#### c. websocket接口

​	理论上每个节点都可以对外提供websocket服务（实际中一般只有proxy节点才会配置），收到websocket消息请求后，具体的接口处理方法和逻辑由用户自己决定，接口参考写法（ws_handler.py）如下：

```python
import asyncio
import ujson

from websockets.exceptions import ConnectionClosed

from obespoir.share.singleton import Singleton
from obespoir.share.ob_log import logger
from obespoir.base.common_define import NodeType
from obespoir.base.ob_protocol import DataException
from obespoir.base.global_object import GlobalObject
from obespoir.websocketserver.route import webSocketRouteHandle
from obespoir.rpcserver.push_lib import push_message


@webSocketRouteHandle
async def forward_0(command_id, data, session_id):
    """
    消息转发
    :param command_id: int
    :param data: json
    :param session_id: string
    :return: None
    """
    print("forward_0", command_id, data, type(data), data, session_id)
    if not isinstance(data, dict):
        try:
            data = ujson.loads(data)
            print("data type :", type(data))
        except Exception:
            logger.warn("param data parse error {}".format(data))
            return {}
    data.update({"message_id": command_id})
    await push_message(NodeType.ROUTE, command_id, data, session_id=session_id, to=None)
```

# 三. 后续

​	限于时间原因，当前上述麻将代码中只有服务端支持自定义配置，client代码为二人麻将代码，服务端通过配置文件配成二人即可。

​	麻将服务端代码详细代码讲解，后续将陆续以文档方式更新上传，有兴趣的读者可以联系作者~

​	联系方式：

​		邮箱： jamonhe@qq.com

​		微信： jamonhe

![weixin](doc/weixin.jpeg)