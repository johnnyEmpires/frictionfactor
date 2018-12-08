#!/usr/bin/python3

# this code runs on python3.6!
import math
import random
import time


def fcalc(e, d, re):
	'''
	e : pipe roughness, mm
	d : pipe diameter, mm
	re : reynolds number

	module for computing friction factor
	incremental search is used to find the zero of the equation, see non_laminar_ffactor function
	'''
	# E = relative roughness, e/d, return up to 8th decimal places
	E = round(e/d, 8)
	
	if E == 0:
		#print (f"the relative roughness is {format(E, '.10f')} (smooth pipe), flow is laminar, reynolds number is {re}")
		return ffactor_smooth_pipes(re)

	else:
		if re == 0:
			# no flow
			return 'infinity'

		elif re <= 2300:
			#print (f"the relative roughness is {format(E, '.10f')}, flow is laminar, reynolds number is {re}")
			return laminar_flow_ffactor(re)

		elif re > 10000:
			return newton_method(E, re)


def laminar_flow_ffactor(re):
	# laminar flow
	# under this condition use the hagen-poisseuille equation
	frictionFactor = round(64 / re, 10)
	return frictionFactor, 0, 0


def ffactor_smooth_pipes(re):
	# calculate friction factor for smooth pipes
	targetFd = 0.000001		# for storing target friction factor temporary result
	counter = 0					# for tracking number of iterations
	inc = 0.000001				# increment
	arbitRes = round((targetFd * (2 * math.log10(re * math.sqrt(targetFd)) - 0.8)) - 1, 6)
	
	while arbitRes != 0:
		if arbitRes > 0:
			break
		targetFd += inc
		counter += 1
		arbitRes = round((math.sqrt(targetFd) * (2 * math.log10(re * math.sqrt(targetFd)) - 0.8)) - 1, 4)
	return round(targetFd, 10), arbitRes, counter


def _root_calc(E, re, f):
	# function for calculating the root of the equation
	# f = equals the estimated friction factor that will make the equation equal to zero
	A = E / 3.7
	B = 2.51 / re
	x = f
	eqn = (x + (2 * math.log10(A + (B * x))))
	return eqn


def _initial_guess_calc(E, re):
	A = E / 3.7
	C = 6.9 / re

	#return C + (A**1.11)
	return -1.8 * math.log10(C + (A**1.11))
	#return -1.8 * math.log10(C + (A**1.11))	# return initial guess


def _slope_calc(E, re, i):
	'''
	E = e / d, roughness divided by diameter
	re = reynolds number
	i = initial guess, estimated friction factor
	m = slope
	'''
	A = E / 3.7
	B = 2.51 / re
	x = i
	m = 1 + 2 * (((B/math.log(10, math.e)) / (A + (B * x))))
	return m


def newton_method(E, re):

	x = _initial_guess_calc(E, re)		# initial value to start calculation
	y = _root_calc(E, re, x)			# use same eqn to find value of x

	calcF = 1 / x**2
	counter = 0							# used to trace number of iterations
	while y != float(0):							# keep calculating until solution is found
	#for x in range(1000000):
		time.sleep(0.1)

		# dont stop iterating until root is found
		counter += 1
		y = _root_calc(E, re, x)
		m = _slope_calc(E, re, x)
		x = x - (y / m)				# find next value
		calcF = 1 / x**2

		# for testing
		print (f"counter[{counter}]...y: {y}, m: {m}, x: {x}, friction factor: {calcF}")

		# return answer after testing
		#print (f"calculating....{counter}, {calcF}, {y}")
	return  round(calcF, 10), y, counter


if __name__ == '__main__':
	e = 0.025
	d = 1
	re = 2310

	E = round(e/d, 8)

	#result = fcalc(e, d, re)
	#print (f"results : {result}")

	for idx in range(600, 1000000000, 100):
		print (idx, fcalc(e, d, idx))
