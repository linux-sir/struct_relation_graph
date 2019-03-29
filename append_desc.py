#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re



def get_description():
    """TODO: 向dot文件中追加node的描述信息 

    :arg1: TODO
    :returns: TODO

    """
    if not os.path.exists("desc_config"):
        print "desc_config is not exists !!!!!"
        return
    fconfig = open("desc_config")
    lines = fconfig.readlines()
    desc_dict = {}
    for line in lines:
        if '=' in line and "#" not in line:
            config = line.split('=')
            if len(config) == 2:
                desc_dict[config[0].strip()] = config[1].strip().replace('\n','')
    return desc_dict            
            

def get_node_name(lines):
    """TODO: 从graph中获取node0和Name的对应关系
    :returns: TODO

    """
    node_name_dict = {}
    for line in lines:
        if '------' in line and '[' in line:
            name = line.split('------')[1].strip()
            node = line.split('[')[0]
            node_name_dict[name] = node
    return node_name_dict        
def add_description():
    """TODO: Docstring for add_description.

    :arg1: TODO
    :returns: TODO

    """
    desc_list = get_description()
    fdot = open('graph')
    lines = fdot.readlines()
    lines = lines[:-1] # 去掉最后一行的'}'
    fdot.close()
    node_name_dict = get_node_name(lines)
    for name in desc_list:
        if node_name_dict.has_key(name):
            node = node_name_dict[name]
            desc = desc_list[name]
            #print 'name:',name,'node:',node,'desc:',desc
            line = node+'desc[label = \"' + desc + '\" shape=plaintext];\n'
            lines.append(line)
            line = node+'desc -> \"'+ node + '\":f0[ color=\"green\"]\n'
            lines.append(line)


    #print lines
    lines.append('}\n')
    fdot = open('graph.tmp','w')
    fdot.writelines(lines)
    fdot.close()
    os.system('dot -Tpng graph.tmp -o graph.png')
    os.remove('graph.tmp')
    print '------> graph.png'

    
            






if __name__ == '__main__':
    add_description()
