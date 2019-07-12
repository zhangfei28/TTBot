import execjs
import time
import math
import hashlib
from functools import partial
from settings import signature_js_func,signature_js_path

def get_js(js_file_path,mode='r'):
	"""
	:param data:
		@js_file_path: js脚本路径
		@mode   	 : IO操作js脚本文件的模式，默认为只读
	:return:
		@result 	 : js脚本文本
	"""
	f = open(js_file_path,mode)
	line = f.readline()
	result = ''
	while line:
		result +=  line
		line = f.readline()
	return result

def py_to_js(js_file_path,js_func,*params):
	"""
	:usage:
		python传值给js脚本执行后获取其结果
	:param data:
		@js_file_path	: js脚本路径
		@js_func	 	: 要执行的js脚本的函数
		@*params	 	: python传给js函数的参数，可传多个
	:return:
		@result 	 	: js脚本执行后的结果
	"""
	js_script = get_js(js_file_path)
	JsContext = execjs.compile(js_script)
	result = JsContext.call(js_func,*params)
	return result

def get_ascp():
	"""
	:usage:
		获取今日头条伪造请求链接的参数AS、CP
	:return:
		@result 	 : 元组(AS、CP)
	"""
	t = int(math.floor(time.time()))
	e = hex(t).upper()[2:]
	m = hashlib.md5()
	m.update(str(t).encode(encoding='utf-8'))
	i = m.hexdigest().upper()
	if len(e) != 8:
		AS = '479BB4B7254C150'
		CP = '7E0AC8874BB0985'
		return AS,CP
	n = i[0:5]
	a = i[-5:]
	s = ''
	r = ''
	for o in range(5):
		s += n[o] + e[o]
		r += e[o + 3] + a[o]
	AS = 'A1' + s + e[-3:]
	CP = e[0:3] + r + 'E1'
	return AS,CP

def payload_for_get( id, mode, max_behot_time):
	"""
    :usage:
        根据参数，爬取模式:文章、视频、微头条等来生成今日头条爬取
        用户首页内容的伪造请求参数
    :param data:
        @id             : 用户id
        @mode	 		: 爬取模式，0:视频，1:文章，2:微头条
        @max_bahot_time	: 区分爬取下拉获取条目的时间戳标识，起始为0
    :return:
        @result			: 生成的伪造请求参数
    """
	_signature = py_to_js(signature_js_path, signature_js_func, id, max_behot_time)
	# ascp = py_to_js(ascp_js_path,ascp_js_func)
	_as,_cp = get_ascp()
	return {
		'page_type': mode,
		'user_id': id,
		'max_behot_time': max_behot_time,
		'count':'20',
		'as': _as,
		'cp': _cp,
		'_signature': _signature
	}

signature_func = partial(py_to_js,signature_js_path,signature_js_func)
