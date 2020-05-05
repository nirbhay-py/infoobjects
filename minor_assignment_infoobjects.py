import itertools
def prob_1(arr):
	arr_1 = []
	for row in arr:
		for obj in row:
			arr_1.append(obj)

	print(arr_1)



def prob_2():
	def char_1(func):
		def inner(*args, **kwargs):
			print("$" * 10)
			func(*args, **kwargs)
			print("$" * 10)
		return inner

	def char_2(func):
		def inner(*args, **kwargs):
			print("@" * 10)
			func(*args, **kwargs)
			print("@" * 10)
		return inner

	@char_1
	@char_2
	def printer(msg):
		print(msg)

	foo = printer('I have been decorated')



def prob_3(inp_string):
	final = []
	dict = {2:['a', 'b', 'c'], 3:['d', 'e', 'f'], 4:['g', 'h', 'i'], 5:['j', 'k', 'l'], 6:['m', 'n', 'o'], 7:['p', 'q', 'r', 's'], 8:['t', 'u', 'v'], 9:['w', 'x', 'y', 'z']}
	for char in dict[int(inp_string[0])]:
		final.append(char)
	for i in range(1, len(inp_string)):
		median = []
		for j in range(len(final)):
			for k in range(len(dict[int(inp_string[i])])):
				median.append(final[j]+dict[int(inp_string[i])][k])
		final = median[:]
	print(final)


prob_1([[1,3,4],[1,3,2],[1,5,21]])
prob_2()
prob_3("23")
