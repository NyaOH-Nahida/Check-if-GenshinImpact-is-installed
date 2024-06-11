import sys, ctypes, tempfile, requests, winreg, os, time

Genshin_URL = "https://ys-api.mihoyo.com/event/download_porter/link/ys_cn/official/pc_default"

#读取注册表
def Read_Registry(path, value_name):
    """
    读取指定注册表路径和键值名称的值。
    """
    try:
        # 尝试打开64位视图的注册表键
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path,0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        
        value, reg_type = winreg.QueryValueEx(reg_key, value_name)
        winreg.CloseKey(reg_key)
        return value

    except FileNotFoundError:
        try:
            # 如果64位视图失败，尝试打开32位视图的注册表键
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,path,0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
            
            value, reg_type = winreg.QueryValueEx(reg_key, value_name)
            winreg.CloseKey(reg_key)
            return value
        
        except FileNotFoundError:
            return None
        except Exception:
            return None

    except Exception:
        return None


#程序主函数
def main_function():
    install_path = Read_Registry(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\HYP_1_1_cn","InstallPath")
    #获取米哈游启动器安装路径
    if install_path:
        print(f"检测到您的电脑上安装了米哈游启动器，安装路径:{install_path}\n尝试启动原神……(该窗口即将在5秒后自动关闭)")
        time.sleep(5)
        try:
            os.startfile(f"{install_path}\games\Genshin Impact Game\YuanShen.exe")
        except Exception as e:
            print(f"启动失败！{e}")
        else:
            exit()
    else:
        print("在您的电脑上未找到米哈游启动器，即将在3秒后为你安装最新版米哈游启动器……")
        time.sleep(3)
        try:
            temp_dir = tempfile.gettempdir()
            save_path = f"{temp_dir}\yuanshen_setup.exe"
            #获取temp目录绝对路径
            download_file = requests.get(Genshin_URL, save_path)
            #发送请求下载文件
            print("正在下载安装包……")
            open(save_path,"wb").write(download_file.content)
            print(f"文件已下载到：{save_path}")
            #写入到文件
            print("正在打开……")
            os.system(f'start "" "{save_path}"')
            sleep(5)
            #打开下载好的安装包
        except Exception as e:
            print(f"下载文件时出错！{e}")

if __name__ == '__main__':
    # 判断当前进程是否以管理员权限运行
    if ctypes.windll.shell32.IsUserAnAdmin() :
        print('权限检查通过！')
        main_function()
    else:
        print('权限检查失败！尝试以管理员权限启动新进程...')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)