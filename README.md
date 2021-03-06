# struct_relation_graph
## 设计目标
- 用于将C语言中结构体定义转化为图形

## 用法
### 编译
```
lex graph.txt  # 生成lex.yy.c文件
gcc lex.yy.c -o parse -ll  # 生成parse可执行文件
```
注：第一次使用需要编译，其它情况在不修改graph.txt的情况下，不需要作此操作。
### 建议操作步骤
- 先将要整理的结构体定义复制到一个文件中，文件后缀是.c或.h,并存放test目录中
- 执行命令
```

$ python parse-struct.py -d test

```
注：parse-struct.py中定义了parse的位置，需要修改为实际路径后才能正常使用

- 为结构体添加注释说明
先在desc_config中添加注释内容，格式是 
```
struct_name=功能说明 
```
然后执行脚本：
```
$ python append_desc.py

```
### 示例
```
$ python parse-struct.py -d example/
out file is example/kvm_types.h-struct-result.txt
out file is example/kvm_host.h-struct-result.txt
------> threa are anonymous structs,please rename them !!!!!!!!!
------> threa are anonymous structs,please rename them !!!!!!!!!
------> threa are anonymous structs,please rename them !!!!!!!!!
------> threa are anonymous structs,please rename them !!!!!!!!!
------> threa are anonymous structs,please rename them !!!!!!!!!
total file is 10
--list set([8, 1, 4, 0])
# 查看当前目录下的graph.png
```
注：此工具对于结构体定义中包含匿名结构体定义时，该结构体定义会被忽略，故出现提示‘------> threa are anonymous structs,please rename them !!!!!!!!!’,需要手工将结构体定义修改掉。（其实这样并不会影响关系图的效果）
## 已知问题
- 不兼容结构体定义内包含匿名结构体定义的情况,工具会自动替换掉匿名结构体定义语句为'struct anonymous abc;'
- 不解析宏定义的条件，直接忽视其意义

# 参考
- https://blog.csdn.net/peterbig/article/details/74614949

