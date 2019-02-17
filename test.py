import time


for i in range(20000):
	if i == 0:
		print (f"{i}: this number is zero...")

	elif i % 2 == 0:
		print (f"{i} : this number is even...")

	else:
		print (f"{i} : this number is odd...")

	time.sleep(0.001)