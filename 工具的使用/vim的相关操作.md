[TOC]

### Vim相关操作示例

<font face="黑体">&emsp;&emsp;Vim是从 vi 发展出来的一个文本编辑器。代码补完、编译及错误跳转等方便编程的功能特别丰富，在程序员中被广泛使用。
简单的来说， vi 是老式的字处理器，不过功能已经很齐全了，但是还是有可以进步的地方。 vim 则可以说是程序开发者的一项很好用的工具。
连 vim 的官方网站 (<http://www.vim.org>) 自己也说 vim 是一个程序开发工具而不是文字处理软件。

</font>

- **vim键盘图：**

 ![Vim键盘使用图](https://img2018.cnblogs.com/blog/685007/201902/685007-20190219103545499-1516663381.png)

- **vim文字图：**

 ![Vim命令文字总结图](https://img2018.cnblogs.com/blog/685007/201902/685007-20190219103431877-1441653557.png)
 
### vi/vim 的使用

<font face="黑体" size=4>&emsp;&emsp;基本上 vi/vim 共分为三种模式，分别是命令模式（Command mode），输入模式（Insert mode）和底线命令模式（Last line mode）。 这三种模式的作用分别是：

**命令模式：**

用户刚刚启动 vi/vim，便进入了命令模式。
此状态下敲击键盘动作会被Vim识别为命令，而非输入字符。比如我们此时按下i，并不会输入一个字符，i被当作了一个命令。

以下是常用的几个命令：

- i 切换到输入模式，以输入字符。
- x 删除当前光标所在处的字符。
- : 切换到底线命令模式，以在最底一行输入命令。

若想要编辑文本：启动Vim，进入了命令模式，按下i，切换到输入模式。
命令模式只有一些最基本的命令，因此仍要依靠底线命令模式输入更多命令。

**输入模式**

在命令模式下按下i就进入了输入模式。

在输入模式中，可以使用以下按键：

- 字符按键以及Shift组合，输入字符 
- ENTER，回车键，换行 
- BACK SPACE，退格键，删除光标前一个字符 
- DEL，删除键，删除光标后一个字符 
- 方向键，在文本中移动光标 
- HOME/END，移动光标到行首/行尾 
- Page Up/Page Down，上/下翻页 
- Insert，切换光标为输入/替换模式，光标将变成竖线/下划线 
- ESC，退出输入模式，切换到命令模式

**底线命令模式**

在命令模式下按下:（英文冒号）就进入了底线命令模式。
底线命令模式可以输入单个或多个字符的命令，可用的命令非常多。
在底线命令模式中，基本的命令有（已经省略了冒号）：
- q 退出程序 
- w 保存文件 

按ESC键可随时退出底线命令模式。

这三个模式想成底下的图标来表示：

![](https://www.runoob.com/wp-content/uploads/2014/07/vim-vi-workmodel.png)
</font>

#### 启动Vim

```
vim -c cmd file: 在打开文件前，先执行指定的命令；
vim -r file: 恢复上次异常退出的文件；
vim -R file: 以只读的方式打开文件，但可以强制保存；
vim -M file: 以只读的方式打开文件，不可以强制保存；
vim -y num file: 将编辑窗口的大小设为num行；
vim + file: 从文件的末尾开始；
vim +num file: 从第num行开始；
vim +/string file: 打开file，并将光标停留在第一个找到的string上。
vim –remote file: 用已有的vim进程打开指定的文件。 如果你不想启用多个vim会话，这个很有用。但要注意， 如果你用vim，会寻找名叫VIM的服务器；如果你已经有一个gvim在运行了， 你可以用gvim –remote file在已有的gvim中打开文件。
```
#### 翻屏

```
ctrl+f: 下翻一屏。
ctrl+b: 上翻一屏。
ctrl+d: 下翻半屏。
ctrl+u: 上翻半屏。
ctrl+e: 向下滚动一行。
ctrl+y: 向上滚动一行。
n%: 到文件n%的位置。
zz: 将当前行移动到屏幕中央。
zt: 将当前行移动到屏幕顶端。
zb: 将当前行移动到屏幕底端。
```
#### 基本插入
```
i: 在光标前插入；一个小技巧：按8，再按i，进入插入模式，输入=， 按esc进入命令模式，就会出现8个=。 这在插入分割线时非常有用，如30i+<esc>就插入了36个+组成的分割线。
I: 在当前行第一个非空字符前插入；
gI: 在当前行第一列插入；
a: 在光标后插入；
A: 在当前行最后插入；
o: 在下面新建一行插入；
O: 在上面新建一行插入；
:r filename在当前位置插入另一个文件的内容。
:[n]r filename在第n行插入另一个文件的内容。
:r !date 在光标处插入当前日期与时间。同理，:r !command可以将其它shell命令的输出插入当前文档。
```
#### 移动光标
```
# hjkl
# 2w 向前移动两个单词
# 3e 向前移动到第 3 个单词的末尾
# 0 移动到行首
# $ 当前行的末尾
# gg 文件第一行
# G 文件最后一行
# 行号+G 指定行
# <ctrl>+o 跳转回之前的位置
# <ctrl>+i 返回跳转之前的位置

H ：光标移至屏幕顶行
M ：光标移至屏幕中间行
L ：光标移至屏幕最后行

0：（注意是数字零）光标移至当前行首
$：光标移至当前行尾


vi 编辑器中跳到文件的第一行：
   a  输入 :0 或者 :1   回车
   b  键盘按下 小写 gg

vi 编辑器跳到文件最后一行：
   a 输入 :$   回车
   b 键盘按下大写 G
   c 键盘按 shift + g  (其实和第二种方法一样)

```
#### 退出
```
# <esc> 进入正常模式
# :q! 不保存退出
# :wq 保存后退出
```
#### 删除
```
# x 删除当前字符
# dw 删除至当前单词末尾
# de 删除至当前单词末尾，包括当前字符
# d$ 删除至当前行尾
# dd 删除整行
# 2dd 删除两行
```
#### 修改
```
# i 插入文本
# A 当前行末尾添加
# r 替换当前字符
# o 打开新的一行并进入插入模式
```
#### 撤销复制粘贴剪切
```
# u 撤销
# <ctrl>+r 取消撤销
# v 进入可视模式
# y 复制
# p 粘贴
# yy 复制当前行
# dd 剪切当前行
```
#### 文件 查找
```
# :e! 强制刷新该文件
# <ctrl>+g 显示当前行以及文件信息

# / 正向查找（n：继续查找，N：相反方向继续查找）
# ？ 逆向查找
# % 查找配对的 {，[，(
# :set ic 忽略大小写
# :set noic 取消忽略大小写
# :set hls 匹配项高亮显示
# :set is 显示部分匹配

/something: 在后面的文本中查找something。
?something: 在前面的文本中查找something。
/pattern/+number: 将光标停在包含pattern的行后面第number行上。
/pattern/-number: 将光标停在包含pattern的行前面第number行上。
n: 向后查找下一个。
N: 向前查找下一个。

```
#### 替换 折叠 执行外部命令
```
# :s/old/new 替换该行第一个匹配串
# :s/old/new/g 替换全行的匹配串
# :%s/old/new/g 替换整个文件的匹配串

# zc 折叠
# zC 折叠所有嵌套
# zo 展开折叠
# zO 展开所有折叠嵌套

# :!shell 执行外部命令
```
#### 字体 分屏
```
# <ctrl> - 缩小
# <ctrl> shift + 放大
# <ctrl> 0 还原

$ Ctrl+W v  // 左右
$ Ctrl+W s  // 上下
# 移动光标
$ Ctrl+W h/j/k/l  // 左/上/下/右
# 移动分屏
$ Ctrl+W H/J/K/L  // 左/上/下/右
# 修改屏幕尺寸
$ Ctrl+W =/+/-
```
#### 基本配置 取消备份 文件编码
```
`.vimrc` 是 `Vim` 的配置文件，需要我们自己创建

cd
touch .vimrc

set nobackup
set noswapfile

set encoding=utf-8
```
#### 查找  显示行号 显示光标当前位置 设置缩进

```
set ic
set hls
set is

set number
set ruler

set cindent

set tabstop=2
set shiftwidth=2

```
 
#### 突出显示当前行  左下角显示当前 vim 模式 代码折叠 主题
```
set cursorline
set showmode
set nofoldenable

syntax enable
set background=dark
colorscheme solarized

```
 参考链接：
 
 <https://zhuanlan.zhihu.com/p/266573900>
 
 <https://www.cnblogs.com/chenyablog/p/10399601.html>