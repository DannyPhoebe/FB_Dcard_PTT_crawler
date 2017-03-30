def init(input_forum,input_until):
	global header,default_len,forum,until
	header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
	default_len = 30
	forum = input_forum
	until = input_until