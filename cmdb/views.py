from django.shortcuts import render
import cv2
from excel_operate import *
from django.core.files.storage import default_storage


# Create your views here.
from django.shortcuts import HttpResponse
def index(request):
	# return HttpResponse('Hello world')
	# return render(request,'index.html')
	# if request.method=="POST":
	# 	username = request.POST.get("username",None)
	# 	password = request.POST.get("password",None)
	# 	print(username,password)
	# image_file = request.POST.get("upload_file",None)
	# if image_file:
	# 	img = cv2.imread(image_file)
	# 	cv2.imshow(img)
	# 	cv2.waitkey(0)
	# 只有在请求方法是POST，并且请求页面中 < form > 有enctype = "multipart/form-data"
	# 属性时FILES才拥有数据。否则，FILES
	# 是一个空字典。
	upload_files = []
	if request.method=="POST":
		print(request.FILES['upload_file'])
		for name,upload in request.FILES.items():
			# print(upload)
			# 这里以二进制打开，方便写文件
			file_name = upload.name
			with default_storage.open(file_name, 'wb') as f:
				for chunk in upload.chunks():
					f.write(chunk)
				upload_files.append(file_name)
	# 第一步解析用户上传的excel的keys
	keys = []
	for file in upload_files:
		for sheet in get_visible_names(file):
			keys.extend(get_keys(file,sheet))
			keys = list(set(keys))
	print(keys)
	# 使用context传递信息
	context = dict({'keys':keys})
	return render(request,'index.html',context)

