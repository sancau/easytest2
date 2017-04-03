# coding=utf-8

from bl.easytest import Test

path = r'C:\Users\Испытатель\Desktop\7060 аттестация\протокол7060.et2'

t = Test(path)

t.calculate()

t.create_report('output')
