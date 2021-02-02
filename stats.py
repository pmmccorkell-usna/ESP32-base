#21 October 2019
#US Naval Academy, Robotics and Control TSD
#Patrick McCorkell

import math

def stdev(samples):
	n = len(samples)
	avg=mean(samples)
	stdev_list=[]
	for i in range(n):
		stdev_list.append(math.pow((samples[i]-avg),2))
	stdev=(math.sqrt(mean(stdev_list)))
	dict={
		'stdev':stdev,
		'mean':avg
		}
	return dict

def mean(samples):
	n=len(samples)

	sum=0
	mean=0
	i=0
	for i in range(n):
		sum+=samples[i]
	mean=sum/n
	return mean

#	stackoverflow.com/questions/1604464/twos-complement-in-python
def twos_comp(val,bits):
	if(val&(1<<(bits-1))):
		val=val-(1<<bits)
	return val

def sig_digits(val,digits):
	abs_val=math.fabs(val)
	return_val=round(val, digits-(1+math.floor(math.log10(abs_val))))
	return return_val
