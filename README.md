# Person Counter
Count person number

How to Build?

1. 打开setup.py.
2. 更改"ext_modules=cythonize(['方法文件目录（比如:api/video）'])"，反正我每次更改都会写更新日志的，日志里的每一个文件都要用一次，
晚点我会把这个脚本优化，到时候看日志。
3. 然后右键有一个Run"setup",点击他
4. 然后点击下面的Terminal，输入命令pyinstaller mian.spec（有时候我会傻逼没传，没传这个文件记得提醒我，不要自己去打包spec一定会出问题的）

怎么使用。

1. 把build下的lib开头的文件内的所有文件复制到一个新的文件夹
2. 把dist下的main.exe文件一起复制过去
3. 把weights文件夹也放过去
4. 双击打开即可

以下是更新日志：

2.26: update api/video.py, ulits/Video_processomg.py, change /output api, now need add ipaddress after /output, for example /ouput/192.168.3.66