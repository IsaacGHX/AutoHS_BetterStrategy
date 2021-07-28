# AutoHS
目前还在开发过程中，可能有很多Bug……

欢迎任何批评建议~

原来的脚本是通过计算机视觉手段（分析图片哈希相似度等）来分析局势的，但现在这个方案已经被放弃了（非常不靠谱）。可以在`cv`分支中看到cv相关的代码。

### 如何运行

1. 安装所需依赖:
```
pip install -r requirements.txt
```

2. 在 `constants/constants` 里有一些参数可以设置，其中名为
 `HEARTHSTONE_POWER_LOG_PATH` 的变量必须修改成你的电脑上的炉石传说日志
   `Power.log` 的路径，`Power.log` 在炉石安装路径下的 `Logs/`文件夹中。
   
> `Power.log` 中记录了对战过程中每一个**对象**(**Entity**)的每一项**属性**(**tag**)的变化。
> 这个**对象**包括玩家、英雄、英雄技能、卡牌(无论在牌库里、手牌中、战场上还是坟地里)等。
> 
> `Power.log` 会在进入炉石后第一次对战开始时创建，在退出炉石后自动删除。
> 
> 关于炉石log的更多信息可以查看这个
> [Reddit帖子](https://www.reddit.com/r/hearthstone/comments/268fkk/simple_hearthstone_logging_see_your_complete_play/) 。

3. 可以先跑一跑 `demo/` 下的一些文件

4. 若要启动脚本，运行 `main.py` 即可。
   注意脚本需要屏幕分辨率为`1920 * 1080`、炉石全屏，需要把炉石放在最前台。
   你可以把战网客户端最小化到任务栏，或是放在炉石应用下面，但请不要关闭战网客户端。有时炉石会意外关闭，这时程序会试图重新打开炉石。
   

### 我目前用的挂机卡组 
标准模式-解解拖拖牧
- 2x (1) 倦怠光波
- 2x (1) 护甲商贩
- 2x (1) 神圣惩击
- 2x (2) 噬骨殴斗者
- 2x (2) 暗言术：灭
- 2x (3) 亡首教徒
- 2x (3) 噬灵疫病
- 2x (3) 狂傲的兽人
- 1x (4) 暗言术：毁
- 2x (4) 狂乱
- 2x (4) 神圣新星
- 1x (5) 泰兰·弗丁
- 2x (5) 锈骑劫匪
- 1x (5) 除奇致胜
- 1x (6) 凯恩·血蹄
- 1x (7) 吞噬者穆坦努斯
- 1x (7) 灵魂之镜
- 2x (9) 戈霍恩之血

神秘代码:
```
AAECAa0GBsi+A/PuA6bvA6iKBPCfBKOgBAzXvgPcvgPmvgPLzQP63wP44wOS5AOY6gOb6wOEnwSFnwTBnwQA
```

[comment]: <> (### 如果想要用自己的卡组)

[comment]: <> (我觉得需要经过一下几步:)

[comment]: <> (- 你需要能认出每一张手牌， AutoHS使用图片哈希来识别图片， )

[comment]: <> (   你需要录入新卡的哈希， 可以通过 `demo/identify_cards.py` )

[comment]: <> (   去读取手牌卡画哈希)

[comment]: <> (- 把哈希和对应名称录入到 `constants/hash_vals.py` 中)

[comment]: <> (- 写出卡牌逻辑， 可以参照 `card.py`)

[comment]: <> (- 把卡牌和中文名对应， 需要更新 `name2card.py`)

[comment]: <> (好像有点麻烦...)



### 文件说明
- `demo/catch_screen_demo.py` : 运行此文件会获取炉石传说进程的整个截屏
(无论是在前台还是后台)，并画上一些坐标基准线，方便判断想实现的操作的坐标值
- `demo/game_state_snapshot_demo.py` : 在控制台显示目前的炉石战局情况，包括显示手牌情况，英雄情况，随从情况等；
  还会在`demp/`目录下创建一个名为`game_state_sanpshot.txt`的文件，记录log分析情况。
  需要在 `Power.log` 存在，即进入对战模式后调用。
- `demo/get_window_name.py` : 显示当前所有窗口的名称和编号，可以用来看炉石传说叫什么名字……
- `demo/mouse_control_demo.py` : 一个样例程序展现了如何控制鼠标


[comment]: <> (### 关于截取屏幕，以及opnecv2)

[comment]: <> (使用的是win的接口。在矩阵里第一维是行号，而在opencv里，windows接口里和mouse接口里第一维是列号。)

[comment]: <> (矩阵里的色彩排序为&#40;B，G，R&#41;)

[comment]: <> (### 关于控制鼠标)

[comment]: <> (原本想通过发送信号的方式在让炉石在后台也能接收到鼠标点击)

[comment]: <> (但是发现炉石应该是所谓的接受直接输入的进程，信号模拟它不会接收……)

[comment]: <> (所以只能使用很low的鼠标点击了)

[comment]: <> (也许能直接模拟网络发包？)


[comment]: <> (### 关于网络连接的观察)

[comment]: <> (一打开炉石就会建立两个TCP连接，这两个所有的数据都是加密的。像分解卡牌， 只有退出了某个卡牌的分解界面（就是可以撤销的界面）才会发包确认分解结果。)

[comment]: <> (实验下来感觉只有其中一条连接在真的交换数据。)

[comment]: <> (点击匹配会新建一个连接，这个连接是加密的。在匹配完成后连接就销毁。)

[comment]: <> (进入对战会又新建一个连接，这个是纯TCP没有加密，不过我仍然无法解析数据交换的格式……（总之不是json..……）。)

[comment]: <> (任何一个操作都会触发数据传输（比如空中乱晃鼠标……），而如果什么都不做炉石也会每个5秒跟服务器互相ping一下，应该是在确认是否掉线)
