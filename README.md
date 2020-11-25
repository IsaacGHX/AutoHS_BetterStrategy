# AutoHS
欢迎任何批评建议~

### 如何运行
运行 main.py 即可
注意本脚本需要屏幕分辨率为 1920 * 1080, 炉石全屏
在运行时按下 Ctrl+Q 可以退出脚本
需要把炉石放在最前台

### 文件说明
- catch_screen_demo.py : 运行此文件会获取炉石传说进程的整个截屏
(无论是在前台还是后台),并画上一些坐标基准线,方便判断想实现的操作的坐标值 
- mouse_control_demo.py : 一个样例程序展现了如何控制鼠标
- get_window_name.py : 显示当前所有窗口的名称和编号,可以用来看炉石传说叫什么名字……

### 待办列表
- [ ] 补全注释
- [ ] 补全Readme
- [X] 随机化点击
- [X] 多样化表情
- [X] 英雄打脸 
- [ ] 卡组研发 (防战?) 
- [X] 换起始手牌
- [X] 一键退出
- [ ] 重写FSM(为什么会用递归实现...)

### 关于截取屏幕,以及opnecv2
使用的是win的接口。在矩阵里第一维是行号，而在opencv里,windows接口里,
mouse接口里第一维是列号

矩阵里的色彩排序为(B,G,R)

### 关于控制鼠标
原本像通过发送信号的方式在让炉石在后台也能接收到鼠标点击

但是发现炉石应该是所谓的接受直接输入的进程，信号模拟它不会接收……

所以只能使用很low的鼠标点击了

也许能直接模拟网络发包？


### 关于网络连接的观察
一打开炉石就会建立两个TCP连接,
这两个所有的数据都是加密的,像分解卡牌， 
只有退出了某个卡牌的分解界面（就是可以撤销的界面）才会发包确认分解结果
实验下来感觉只有其中一条连接在真的交换数据。

点击匹配会新建一个连接,这个连接是加密的。在匹配完成后连接就销毁

进入对战会又新建一个连接,这个是纯TCP没有加密，
不过我仍然无法解析数据交换的格式...总之不是json...
任何一个操作都会触发数据传输,比如空中乱晃鼠标...
如果什么都不做炉石也会每个5秒跟服务器互相ping一下,应该是在确认是否掉线


