from django.shortcuts import render
from .excel_operate import *
from django.core.files.storage import default_storage

# Create your views here.
from django.shortcuts import HttpResponse

upload_files = []
upload_file_names =[]
store_keys = []
select_keys = []

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
    # request.session['upload_files']=[]
    # session_files=[]
    # if request.session.has_key('upload_files'):
    #     session_files = request.session['upload_files']
    # session_keys=[]
    # if request.session.has_key('store_keys'):
    #     session_keys = request.session['store_keys']
    done = False
    
    global store_keys
    global upload_files
    global upload_file_names
    global select_keys
    
    if request.method == "POST":
        post_message = request.POST
        if post_message.get('insert',None):
            print(request.FILES['upload_file'])
            for name, upload in request.FILES.items():
                # print(upload)
                # 这里以二进制打开，方便写文件
                file_name = upload.name
                write_url = os.path.join('static', file_name)
                with default_storage.open(write_url, 'wb') as f:
                    for chunk in upload.chunks():
                        f.write(chunk)
                    upload_file_names.append(file_name)
                    upload_files.append(write_url)
                    for sheet in get_visible_names(write_url):
                        store_keys = store_keys+get_keys(write_url,sheet)
                        store_keys = list(set(store_keys))
                    # if session_keys:
                    #     session_keys.extend(get_keys(write_url, sheet))
                    # request.session['store_keys']=store_keys
        elif post_message.get('generate',None):
            select_index = post_message.getlist('check_box_list',None)
            tmp_select = [store_keys[int(index)] for index in select_index]
            select_keys.extend(tmp_select)
        elif post_message.get('done',None):
            if select_keys:
                write_file_by_keys(upload_files,select_keys)
                done = True
        elif post_message.get('clear',None):
            for file in os.listdir('static'):
                if '.xlsx' in file:
                    os.remove(os.path.join('static',file))
            upload_files.clear()
            upload_file_names.clear()
            store_keys.clear()
            select_keys.clear()
            
    
    # if request.method == 'POST' and request.POST.has_key('done'):
    # 第一步解析用户上传的excel的keys
    # 使用context传递信息
    context = dict({'use_keys': select_keys,'valid_keys': store_keys,'done':done,'files':upload_file_names})
    return render(request, 'index.html', context)
