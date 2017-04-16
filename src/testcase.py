# coding=utf-8

from bl.easytest import Test

path = r'C:\Users\2065\Desktop\7018_new\file_att_7018_new.et2'

t = Test(path)

t.calculate()

t.create_report('output')
