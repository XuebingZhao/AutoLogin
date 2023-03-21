# AutoLogin
复旦大学校园网每天凌晨03:00自动断开网络连接，使用此python程序可实现每天03：01自动登录，保持在线

其他的校园网应该在更改登录部分的数据后也能使用


# 使用方法

## 使用Python运行
```py
python AutoLogin.py
```

## 打包成exe

### nuitka
```shell
py -3 -m nuitka --standalone --mingw64 --disable-console --file-version=1.0 --product-version=1.0 --company-name="XuebingZhao" --product-name="Autologin" --enable-plugin=tk-inter --include-data-file=./AutoLogin.ico=./ --remove-output --output-dir=%USERPROFILE%/Desktop/nuikta-out --windows-icon-from-ico=AutoLogin.ico AutoLogin.py
```

### pyintsaller
```shell
py -3 -m pyinstaller -F -w -i AutoLogin.ico AutoLogin.py
```