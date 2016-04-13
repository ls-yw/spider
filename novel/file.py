#coding:utf8
'''
Created on 2016年4月13日

@author: user
'''


class File(object):


    def write(self,preg):
        print preg
        with open('log.txt', 'w') as f:
            f.write('preg：')
            f.write(preg)


