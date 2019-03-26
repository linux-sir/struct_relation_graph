# struct_relation_graph
## 设计目标
用于将C语言中结构体定义转化为图形
## 用法
### 编译
```
lex graph.txt  # 生成lex.yy.c文件
gcc lex.yy.c -o parse -ll  # 生成parse可执行文件
```
注：第一次使用需要编译，其它情况在不修改graph.txt的情况下，不需要作此操作。
### 建议操作步骤
- 先将要整理的结构体定义复制到一个文件中，文件后缀是.c或.h
- 执行命令
```
$ python parse-struct.py -d dest.c
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
- 不兼容结构体定义内包含匿名结构体定义的情况

# 参考
- https://blog.csdn.net/peterbig/article/details/74614949

