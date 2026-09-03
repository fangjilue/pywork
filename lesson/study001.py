#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import random

for i in range(0, 35):
  tmp1 = random.randint(1000, 9999)
  tmp2 = random.randint(1000, 9999)
  print('%s * %s = %s' % (tmp1,tmp2,tmp1*tmp2))