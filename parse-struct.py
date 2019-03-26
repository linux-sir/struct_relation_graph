#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
 
import os
import sys
import string
import getopt
import copy
 
 
parse_tool = '/home/magc/workspace/lex/parse'  #this is lex tools path, please modify in you os
 
 
FILE_TYPE=['.c', '.h']
RESULT_STRUCT=[]
count = 0
frame_height = 30
frame_weight = 300
frame_space = 100
 
 
 
 
def file_type_ok(fileName):
    global FILE_TYPE
    for x in FILE_TYPE:
        if fileName.endswith(x):
            return True
    return False
 
 
def do_parse(fileName):
    if 'struct-result.txt' in fileName:
        return
 
 
    if file_type_ok(fileName):
        cmd = '%s %s' %(parse_tool, fileName)
        os.system(cmd)
 
 
 
def filter_struct_name(name):
    str_head=name
    str_head=str_head.replace('{', '')
    str_head=str_head.replace('\t', ' ')
    str_head=str_head.strip()
    return str_head
 
 
def filter_struct_ele(name):
    str_ele=name
    str_ele=str_ele.replace('{', '')
    str_ele=str_ele.replace('\t', ' ')
    str_ele=str_ele.strip()
    return str_ele
 
 
 
 
def judge_element_is_fun(name):
    if '(' in name and ')' in name:
        return True
    return False
 
 
def judge_element_is_strut(name):
    if ('struct ' in name) and not ('(' in name and ')' in name):
        return True
 
 
    return False
 
 
def get_struct_element_name(name):
    str = name
    keys =['const ', ]
    for x in keys:
        str = str.replace(x,'')
    if 'struct ' in str:
        str = str.replace('struct ', '')
    str = str.strip()
    if str.find(' ')!=-1 and str[:str.index(' ')]:
        str = str[:str.index(' ')]
    elif str.find('\t')!=-1 and str[:str.index('\t')]:
        str = str[:str.index('\t')]
    else:
        return None
    return str
 
 
def get_struct_name(data):
    ret = {}
    index = 0
    for m in data:
        name = m[0]
        name = name.replace('struct ', '')
        name = name.strip()
        if name in ret:
            pass
        else:
            ret[name]=[index]
            index +=1
        for n in m[1:]:
            if 'struct ' in n:
                #n = n.replace('struct ', '')
                n = n.replace(';','')
                n = n.strip()
                ret[name].append(n)
    return ret
 
 
def get_struct(fileName):
    global RESULT_STRUCT
    #print fileName
    if 'struct-result.txt' in fileName:
        handle = open(fileName)
        lines = handle.readlines()
        handle.close()
        os.remove(fileName)
        one_struct=[]
        for line in lines:
            if 'TTT_HEAD:' in line:
                if len(one_struct) != 0:
                    RESULT_STRUCT.append(one_struct)
                    one_struct = []
                str_head = line[line.index('TTT_HEAD:')+len('TTT_HEAD:'):-1]
                str_head = filter_struct_name(str_head)
                one_struct.append(str_head)    
            elif 'TTT_ELE:' in line:
                str_ele = line[line.index('TTT_ELE:')+len('TTT_ELE:'):-1]
                str_ele = filter_struct_ele(str_ele)
                one_struct.append(str_ele)
            else:
                continue
 
 
def walk_dir(dirName, do_work):
    global count;
 
 
    if(not os.path.isdir(dirName)):
        #print dirName
        count +=1
        do_work(dirName)
        return 
 
 
    files = os.listdir(dirName)
    
    for oneFile in files:
        temp = os.path.join(dirName, oneFile)
        if(os.path.isdir(temp)):
            walk_dir(temp, do_work)
        else:
           #print(temp)
           count += 1
           do_work(temp)
      
            
def draw_graph(data):
    fobj = open('./graph', 'w+')
    str_head = 'digraph G { \n \
node [shape=record,height=.1]; \n'
    fobj.write(str_head)
 
 
       #fobj.write(str)
 
 
    str_ship=''
    str_filter=set()
    for x in data:
        index = 1
        for y in data[x][1:]:
            if judge_element_is_strut(y):
                ele_struct_name = get_struct_element_name(y)
                if ele_struct_name is not None and ele_struct_name in data:
                    if '*' not in y:
                        str='node%d: f%d->"node%d":f%d[dir=none color="red"];\n' %(data[x][0],index,data[ele_struct_name][0],0)
                    else:
                        str='node%d: f%d->"node%d":f%d;\n' %(data[x][0],index,data[ele_struct_name][0],0)
                    str_filter.add(data[x][0])
                    str_filter.add(data[ele_struct_name][0])
                    str_ship +=str
            index +=1
      
    print '--list',str_filter          
    str_node=''
    for x in data:
        if data[x][0] not in str_filter:
            continue
        str='node%d[label ="{<f0> ------ %s ------' %(data[x][0], x)
        index = 1
        for y in data[x][1:]:
            if not judge_element_is_fun(y):
                str+='|<f%d>%s' %(index,y)
            index +=1
        str +='}"];\n'
        str_node+=str;
 
 
    fobj.write(str_node)
    fobj.write(str_ship)
            
    fobj.write('}\n')
    fobj.close()
              
 
    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:", ["dir="])
    except:
        print("para error" + ' ' + str(sys.argv[1:]))
        sys.exit(1)
 
 
    dirPath = []
 
 
    for opt, arg in opts:
        if opt in ('-d', '--dir'):
            dirPath = arg.split(':')
            continue
        else:
            print('para error')
            sys.exit(1)
 
 
    for dir in dirPath:
        walk_dir(dir, do_parse)
        walk_dir(dir, get_struct)
 
 
    print 'total file is %d' %count
 
 
    struct_dit = get_struct_name(RESULT_STRUCT)
	
    draw_graph(struct_dit)
 
 
    os.system('dot -Tpng graph -o graph.png')
    #draw_pic(RESULT_STRUCT)
 
 
if __name__ == '__main__':
    main()
