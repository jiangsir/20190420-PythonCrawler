import time, os
s = time.strftime("%Y%m%d%H%M%S", time.localtime())
desktoppath = os.path.join(os.path.expanduser("~"), 'Desktop')
filepath = os.path.join(desktoppath, s+".text")
with open(filepath, "w+") as f:
    f.write("Hello crontab!!!!")
