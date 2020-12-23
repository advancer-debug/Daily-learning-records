### 标准数据类型
Python3 的六个标准数据类型中：

   - 不可变数据（3 个）：Number（数字）、String（字符串）、Tuple（元组）；
   - 可变数据（3 个）：List（列表）、Dictionary（字典）、Set（集合）

### python字符串

python用反斜杠(\)转义字符

|转义字符|	描述|
|----|----|
|\b| 	退格(Backspace)|
|\n|  换行|
|\v| 	纵向制表符|
|\t| 	横向制表符|
|\r|	回车|
|\f| 	换页|

python字符串格式化符号:

|符   号| 	描述|
|----|----|
|%c|	 格式化字符及其ASCII码|
|%s|	 格式化字符串|
|%d|	 格式化整数|
|%f|	 格式化浮点数字，可指定小数点后的精度|
|%g|	 %f和%e的简写|
一种格式化字符串的函数 str.format()，它增强了字符串格式化的功能,基本语法是通过 {} 和 : 来代替以前的 % 。

format 函数可以接受不限个参数，位置可以不按顺序。

^, <, > 分别是居中、左对齐、右对齐，后面带宽度， : 号后面带填充的字符，只能是一个字符，不指定则默认是用空格填充。

+ 表示在正数前显示 +，负数前显示 -；  （空格）表示在正数前加空格

b、d、o、x 分别是二进制、十进制、八进制、十六进制。

此外我们可以使用大括号 {} 来转义大括号

```
split(str="", num=string.count(str))
以 str 为分隔符截取字符串，如果 num 有指定值，则仅截取 num+1 个子字符串
```
```
splitlines([keepends])
按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为 False，不包含换行符，如果为 True，则保留换行符。
```

### 列表 [] list
双层嵌套`list[][]` 取值   包含函数len、max、min、list（元祖转列表） sort clear copy

list.append  count  insert pop（最后一个）  remove（一出第一个匹配项）

`list.extend(seq)`在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）

`list.index(obj)`从列表中找出某个值第一个匹配项的索引位置

### 元组 （） tup=（）
元组中只包含一个元素时，需要在元素后面添加逗号，否则括号会被当作运算符使用。

元组与字符串类似，下标索引从 0 开始，可以进行截取，组合等

元组可以使用下标索引来访问元组中的值tup[]

元组中的元素值是不允许删除的，但我们可以使用del语句来删除整个元组

与字符串一样，元组之间可以使用 + 号和 * 号进行运算。这就意味着他们可以组合和复制，运算后会生成一个新的元组。
Python 表达式	结果 	

包含的函数len max min tuple（将可迭代系列转换为元组）

### 字典 json Dictionary
字典是另一种可变容器模型，且可存储任意类型对象。

字典的每个键值 key=>value 对用冒号 : 分割，每个对之间用逗号(,)分割，整个字典包括在花括号 {} 中
`d = {key1 : value1, key2 : value2, key3 : value3 }`

键必须是唯一的，但值则不必。

值可以取任何数据类型，但键必须是不可变的，如字符串，数字。

可修改键、值，可`del`清空字典
键必须不可变，所以可以用数字，字符串或元组充当，而用列表就不行

包含函数len str type
`radiansdict.clear()`删除字典内所有元素
`radiansdict.copy()`返回一个字典的浅复制
`radiansdict.items()`以列表返回可遍历的(键, 值) 元组数组
`radiansdict.keys()`返回一个迭代器，可以使用 list() 来转换为列表
`radiansdict.values()`返回一个迭代器，可以使用 list() 来转换为列表

### 集合set

add clear copy pop remove

### if 语句  for while
```

if condition_1:
    statement_block_1
elif condition_2:
    statement_block_2
else:
    statement_block_3
```
```
if 表达式1:
    语句
    if 表达式2:
        语句
    elif 表达式3:
        语句
    else:
        语句
elif 表达式4:
    语句
else:
    语句
```
for while
```
while 判断条件(condition)：
    执行语句(statements)……
```
```
while <expr>:
    <statement(s)>
else:
    <additional_statement(s)>
```
```
for <variable> in <sequence>:
    <statements>
else:
    <statements>
```
遍历数字序列，可以使用内置range()函数。它会生成数列

break 语句可以跳出 for 和 while 的循环体。如果你从 for 或 while 循环中终止，任何对应的循环 else 块将不执行。

continue 语句被用来告诉 Python 跳过当前循环块中的剩余语句，然后继续进行下一轮循环。 

### 迭代器 生成器
迭代器是一个可以记住遍历的位置的对象。迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。
迭代器有两个基本的方法：`iter()` 和 `next()`。
字符串，列表或元组对象都可用于创建迭代器：

使用了 yield 的函数被称为生成器（generator）。在调用生成器运行的过程中，每次遇到 yield 时函数会暂停并保存当前所有的运行信息，返回 yield 的值, 并在下一次执行 next() 方法时从当前位置继续运行。

加了星号 * 的参数会以元组(tuple)的形式导入，存放所有未命名的变量参数

加了两个星号 ** 的参数会以字典的形式导入。


### 数据结构的使用
**将列表当堆栈使用stack**
列表方法使得列表可以很方便的作为一个堆栈来使用，堆栈作为特定的数据结构，最先进入的元素最后一个被释放（后进先出）。用 `append()`方法可以把一个元素添加到堆栈顶。用不指定索引的 `pop()` 方法可以把一个元素从堆栈顶释放出来。例如： 
**将列表当作队列使用**
也可以把列表当做队列用，只是在队列里第一加入的元素，第一个取出来；但是拿列表用作这样的目的效率不高。在列表的最后添加或者弹出元素速度快，然而在列表里插入或者从头部弹出速度却不快（因为所有其他的元素都得一个一个地移动）。 

同时遍历两个或更多的序列，可以使用 `zip()` 组合  组合成字典
```
questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
a=dict(zip(questions,answers))
```

open 打开文件（file，mode）

- mode选择 r rb r+ rb+ w wb w+ wb+  a（追加） 
- ab以二进制格式打开一个文件用于追加。
- a+打开一个文件用于读写
- ab+以二进制格式打开一个文件用于追加。

`f.read` 

`f.readline()`会从文件中读取单独的一行。换行符为 '\n'。如果返回一个空字符串, 说明已经已经读取到最后一行。

`f.readlines()`返回该文件中包含的所有行.如果设置可选参数 sizehint, 则读取指定长度的字节, 并且将这些字节按行分割。 

如果要改变文件当前的位置, 可以使用 f.seek(offset, from_what) 函数。

from_what 的值, 如果是 0 表示开头, 如果是 1 表示当前位置, 2 表示文件的结尾，

**pickle 模块**

python的pickle模块实现了基本的数据序列和反序列化。

通过pickle模块的序列化操作我们能够将程序中运行的对象信息保存到文件中去，永久存储。

通过pickle模块的反序列化操作，我们能够从文件中创建上一次程序保存的对象。 

pickle.dump()     load()

### 错误与异常
Python 有两种错误很容易辨认：语法错误和异常。

Python assert（断言）用于判断一个表达式，在表达式条件为 false 的时候触发异常。

**异常处理`try/except`**

异常捕捉可以使用 try/except 语句。

![](https://www.runoob.com/wp-content/uploads/2019/07/try_except.png)

一个 try 语句可能包含多个except子句，分别来处理不同的特定的异常。最多只有一个分支会被执行。

处理程序将只针对对应的 try 子句中的异常进行处理，而不是其他的 try 的处理程序中的异常。

一个except子句可以同时处理多个异常，这些异常将被放在一个括号里成为一个元组，

`try/except` 语句还有一个可选的 else 子句，如果使用这个子句，那么必须放在所有的 except 子句之后。

else 子句将在 try 子句没有发生任何异常的时候执行。

![](https://www.runoob.com/wp-content/uploads/2019/07/try_except_else.png)

`try-finally `语句无论是否发生异常都将执行最后的代码。

![](https://www.runoob.com/wp-content/uploads/2019/07/try_except_else_finally.png)

Python 使用 raise 语句抛出一个指定的异常。
raise语法格式如下：`raise [Exception [, args [, traceback]]]`



运行.py文件无法加载包--可能文件名包名相同

1.package里的__init__.py文件，可以为空文件

2.可以设置PYTHONPATH环境变量，来增加python的搜索路径；

3.运行文件名称不要与类库中的package同名。


### 实例可以利用Python的pickle或shelve模块，通过单个步骤储存到磁盘上

```
import pickle
object = someclass
file = open(filename, 'wb')
picke.dump(object, file)

file = open(filename, 'rb')
object = pickle.load(file)
```
pickle机制把内存中的对象转换成序列化的字节流，可以保存在文件中，也可通过网络发送出去

解除pickle状态则是从字节流转换回同一个内存中的对象，Shelve也类似。但是它会自动把对象pickle生成按键读取的数据库，而此数据库会导出类似于字典的接口
```
import shelve
object = someclass()
dbase = shelve.open('filename')
dbase['key'] = object


```





