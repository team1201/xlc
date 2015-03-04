转换 Excel 文档成为 CSV 和 LUA 格式
===================================

- 作者： zm [zrong](http://zengrong.net)
- 创建： 2014-12-09
- 修改： 2015-03-04 将模块名称从 hhlc 改为 xlc。

# 安装

第一次使用时，必须先进行安装以保证依赖库存在。可以使用下面的方式调用 pip 来安装依赖库：

    pip install -r [依赖库配置文件地址]

Windows 系统，若 pip 命令不可用，可使用下面的命令：

    python.exe -m pip install -r [依赖库配置文件地址]

依赖库文件可以是本地文件或者 url，下面两个地址都可用：

	../client/requirements.txt
	http://192.168.18.18/project/1201/tool/requirements.txt

# 使用

## 作为库使用

### 引用 xlc 库

    import xlc

### 参数说明

- xls  
Excel 文件和配置文件目录
- export  
最终文件的输出目录
- tmpl  
模版文件的目录
- command  
执行的命令, list类型, 传空list表示转换所有配置文件
- ptype  
指定转换配置文件的类型, 如 all/csv/lua

    xlc.main(xls, export, command, ptype)
    
### 转换所有配置文件到export路径

    xlc.main(
        "D:\\works\\hhl\\projects\\config\\xls",
	    "D:\\works\\hhl\\projects\\config\\export", 
	    "D:\\works\\hhl\\projects\\config\\templates", 
	    [],
	    "all"
	)
    
### 转换指定的一个或多个配置文件到export路径

    xlc.main(
	    "D:\\works\\hhl\\projects\\config\\xls",
	    "D:\\works\\hhl\\projects\\config\\export", 
	    "D:\\works\\hhl\\projects\\config\\templates", 
	    ["hero", "skill"],
	    "all"
	)
    
### 转换指定类型的配置文件, 并指定导出路径

    xlc.main(
	    "D:\\works\\hhl\\projects\\config\\xls",
	    "D:\\works\\hhl\\projects\\config\\export", 
	    "D:\\works\\hhl\\projects\\config\\templates", 
	    ["hero", "skill"],
	    "lua"
	)
