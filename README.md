配置文件
======

* 文档作者： zm
* 最后更新： 2014-12-09

该Python库用于保存和转换黄鹤楼项目中的配置文件。

# 安装

第一次使用时，必须先进行安装以保证依赖库存在。

    pip install -r requirements.txt

Mac OS X 系统，可能要使用 pip3：

    pip3 install -r requirements.txt

Windows 系统，若 pip 命令不可用，可使用下面的命令：

    py -m pip install -r requirements.txt

# 使用

## 作为库使用

    # 引用hhlc库
    import hhlc

    # 参数说明
    hhlc.main(xls, export, command, ptype)
    * xls
    Excel 文件和配置文件目录
    * export
    最终文件的输出目录
    * command
    执行的命令, list类型, 传空list表示转换所有配置文件
    * ptype
    指定转换配置文件的类型, 如all/csv/lua
    
    # 转换所有配置文件到export路径
    hhlc.main(
        "D:\\works\\hhl\\projects\\config\\xls",
	    "D:\\works\\hhl\\projects\\config\\export", 
	    [],
	    "all"
	)
    
    # 转换指定的一个或多个配置文件到export路径
    hhlc.main(
	    "D:\\works\\hhl\\projects\\config\\xls",
	    "D:\\works\\hhl\\projects\\config\\export", 
	    ["hero", "skill"],
	    "all"
	)
    
    # 转换指定类型的配置文件, 并指定导出路径
    hhlc.main(
	    "D:\\works\\hhl\\projects\\config\\xls",
	    "D:\\works\\hhl\\projects\\config\\export", 
	    ["hero", "skill"],
	    "all"
	)

