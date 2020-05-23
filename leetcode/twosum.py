#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
def find(arr, target, start):
	one=two=i1=i2= None
	print('start=', start)
	for i in range(len(arr)):
		if(i > start and  one is None and arr[i] < target):
			one = arr[i]
			two = target -one
			i1= i
		elif(two == arr[i]):
			i2 = i

	if(i2 is None):
		return find(arr,target,i1)
	else:
		return (one,two,i1,i2)

nums = [9,8,7,6,5,3,2,1]
target =9

res = find(nums,target,-1)

print("----")
for i in res:
	print(i)






