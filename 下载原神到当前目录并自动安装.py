import tempfile, requests, os

Genshin_URL = "https://ys-api.mihoyo.com/event/download_porter/link/ys_cn/official/pc_default"

try:
    temp_dir = tempfile.gettempdir()
    save_path = "yuanshen_setup.exe"
    #获取temp目录绝对路径
    download_file = requests.get(Genshin_URL, save_path)
    #f发送请求下载文件
    open(save_path,"wb").write(download_file.content)
    #写入到文件
    print("文件已下载到当前目录\n正在打开……")
    os.system(f'start "" "{save_path}"')
    #打开下载好的安装包
except Exception as e:
    print(f"下载文件时出错！{e}")