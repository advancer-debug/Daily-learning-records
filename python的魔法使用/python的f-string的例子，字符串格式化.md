[TOC]



### f-string的例子，字符串格式化

##### 1.f-string 是什么？

*str.format 方法：*

```python
>>> msg = 'hello world'
>>> 'msg: {}'.format(msg)
'msg: hello world'
```

进一步简化格式化方法，Eric Smith 在2015年提交了 PEP 498 -- Literal String Interpolation 提案。

PEP 498 提出了一种新的字符串插值方法，该方法可以更简单便捷的使用 str.format 方法。你只需要在字符串开头加上一个字母 f，形成 f 的格式

```python
>>> msg = 'hello world'
>>> f'msg: {msg}'
'msg: hello world'
```

##### 2.用 python 做基本的文本格式化

使用f-string格式化字符串十分简单。唯一的要求就是给它一个有效的表达式。f-string 也可以用大写F开头或者与 r 原始字符串结合使用。但是你不能将其与 b”” 或者 ”u” 混用。

```python
>>> book = "The dog guide"
>>> num_pages = 124
>>> f"The book {book} has{num_pages} pages"
'The book The dog guide has 124 pages'

>>> F"The book {book} has{num_pages} pages"
'The book The dog guide has 124 pages'
>>> print(Fr"The book {book} has{num_pages} pages\n")

The book The dog guide has 124 pages\n 
>>> print(FR"The book {book} has{num_pages} pages\n")
The book The dog guide has 124 pages\n
>>> print(f"The book {book} has{num_pages} pages\n")
The book The dog guide has 124 pages
```

##### 3.**f-string 的限制**

f-string在表达式出现的上下文中进行求值计算。根据PEP498，这意味着该表达式可以获取所有局部和全局变量。而且该表达式是在运行时计算的表达式。如果在 { <expr> } 之中使用的表达式无法被计算，就会跳出如下异常。

```python
>>> f"{name}"
---------------------------------------------------------------------------
NameError                                 Traceback(most recent call last)
<ipython-input-1-f0acc441190f> in<module>
----> 1 f"{name}"
NameError: name 'name' is not defined
```

##### 4.**如何格式化一个表达式**

如果不想定义变量，那你可以在大括号中使用常量。Python会计算该表达式并显示最终计算结果。

```python
>>> f"4 * 4 is {4 * 4}"
'4 * 4 is 16'
```

或者

```python
>>> n = 4

>>> f"4 * 4 is {n * n}"
'4 * 4 is 16'
```

##### 5.**如何使用 f-string 来调试代码**

```python
>>> def magic_number():
     ...:     return 42
     ...: 

>>> f"{magic_number() = }"
'magic_number() = 42'
```

##### **6、如何格式化数字的不同进制**

![图片](https://mmbiz.qpic.cn/mmbiz_png/fhujzoQe7Tq06w3gVXehYIgQKO3U9jq8I3vlFrVfNyydhWibLZdibWMORNOjxic92yx8EH70r7VeEib7WlfpLE3wMw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

f-string 还能在不同进制下显示数字。例如，你不需要通过b来对一个int进行格式转化就可以显示其二进制结果。

```python
>>> f'{7:b}'
'111'
```

```python
>>> bases = {
       "b": "bin", 
       "o": "oct", 
       "x": "hex", 
       "X": "HEX", 
       "d": "decimal"
}
>>> for n in range(1, 21):
     ...:     for base, desc in bases.items():
     ...:         print(f"{n:5{base}}", end=' ')
     ...:     print()

    1     1     1     1     1 
   10     2     2     2     2 
   11     3     3     3     3 
  100     4     4     4     4 
  101     5     5     5     5 
  110     6     6     6     6 
  111     7     7     7     7 
 1000    10     8     8     8 
 1001    11     9     9     9 
 1010    12     a     A    10 
 1011    13     b     B    11 
 1100    14     c     C    12 
 1101    15     d     D    13 
 1110    16     e     E    14 
 1111    17     f     F    15 
10000    20    10    10    16 
10001    21    11    11    17 
10010    22    12    12    18 
10011    23    13    13    19 
10100    24    14    14    20

```

##### **7、如何用 f-string 打印对象**

你可以用f-string打印自定义对象。默认设置是，如果你向f-string表达式传递了一个对象，它将会显示该对象 __str__ 方法的返回值。不过，你也可以用显式转换操作标志来打印__repr__的值。



- !r - 使用 repr() 将值转化为文本.
- !s - 使用 str() 将值转化为文本.

```python
>>> class Color:
    def __init__(self, r: float = 255, g: float = 255, b: float = 255):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self) -> str:
        return "A RGB color"

    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b})"

>>> c = Color(r=123, g=32, b=255)

# 如不加任何操作符, 会打印 __str__ 的值
>>> f"{c}"
'A RGB color'

# 用`obj!r` 的话会打印 __repr__ 的值
>>> f"{c!r}"
'Color(r=123, g=32, b=255)'

# 使用!s跟默认值一样
>>> f"{c!s}"
'A RGB color'
```

Python也允许通过定义不同类型使用__format__方法控制格式化结果，下面的例子会展示所有可能情况。

```python
>>> class Color:
    def __init__(self, r: float = 255, g: float = 255, b: float = 255):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self) -> str:
        return "A RGB color"

    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b})"

>>> c = Color(r=123, g=32, b=255)

# When no option is passed, the __str__ result is printed
>>> f"{c}"
'A RGB color'

# When `obj!r` is used, the __repr__ output is printed
>>> f"{c!r}"
'Color(r=123, g=32, b=255)'

# Same as the default
>>> f"{c!s}"
'A RGB color'
Python also allows us to control the formatting on a per-type basis through the __format__ method. The following example shows how you can do all of that.

>>> class Color:
    def __init__(self, r: float = 255, g: float = 255, b: float = 255):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self) -> str:
        return "A RGB color"

    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b})"

    def __format__(self, format_spec: str) -> str:
        if not format_spec or format_spec == "s":
            return str(self)

        if format_spec == "r":
            return repr(self)

        if format_spec == "v":
            return f"Color(r={self.r}, g={self.g}, b={self.b}) - A nice RGB thing."

        if format_spec == "vv":
            return (
                f"Color(r={self.r}, g={self.g}, b={self.b}) "
                f"- A more verbose nice RGB thing."
            )

        if format_spec == "vvv":
            return (
                f"Color(r={self.r}, g={self.g}, b={self.b}) "
                f"- A SUPER verbose nice RGB thing."
            )

        raise ValueError(
            f"Unknown format code '{format_spec}' " "for object of type 'Color'"
        )

>>> c = Color(r=123, g=32, b=255)

>>> f'{c:v}'
'Color(r=123, g=32, b=255) - A nice RGB thing.'

>>> f'{c:vv}'
'Color(r=123, g=32, b=255) - A more verbose nice RGB thing.'

>>> f'{c:vvv}'
'Color(r=123, g=32, b=255) - A SUPER verbose nice RGB thing.'

>>> f'{c}'
'A RGB color'

>>> f'{c:s}'
'A RGB color'

>>> f'{c:r}'
'Color(r=123, g=32, b=255)'

>>> f'{c:j}'
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-20-1c0ee8dd74be> in <module>
----> 1 f'{c:j}'

<ipython-input-15-985c4992e957> in __format__(self, format_spec)
     29                 f"- A SUPER verbose nice RGB thing."
     30             )
---> 31         raise ValueError(
     32             f"Unknown format code '{format_spec}' " "for object of type 'Color'"
     33         )

ValueError: Unknown format code 'j' for object of type 'Color'
```



最后，还有个用来转义ASCII字符的a操作符。更多信息可参考:

 docs.python.org/3/library/functions.html#as..

##### **8、如何用f-string设定浮点数精度**

F-string可以像str.format那样格式化浮点数。想要实现这一点，你需要加一个 :（冒号）再加一个 .（英文句号）然后跟着小数点位数最后以f结尾。

举例来说，你可以通过如下代码打印一个浮点数精确到百分位的近似值。

```python
>>> num =4.123956
>>> f"num rounded to 2 decimalpalces = {num:.2f}"
'num rounded to 2 decimal palces = 4.12’
```

不加任何选项的话，则会打印浮点数本身的精确值。

```python
>>> print(f'{num}')
4.123956
```

##### **9、如何将一个数字格式化为百分数**

Python f-string方法有个非常便捷的实现格式化百分数的操作方法。方法与浮点数格式化类似，但是要用%代替结尾的f。它会将原始数值乘以100并显示成有百分符号的固定格式。精度一样也是可以设定的。

```python
>>> total = 87

>>> true_pos = 34

>>> perc = true_pos / total

>>> perc
0.39080459770114945

>>> f"Percentage of true positive: {perc:%}"
'Percentage of true positive: 39.080460%'

>>> f"Percentage of true positive: {perc:.2%}"
'Percentage of true positive: 39.08%'
```

##### **10、如何调整或者增加 f-string 的填充**

你可以便捷的通过 < 或者 > 符号来调整字符串填充。

![图片](https://mmbiz.qpic.cn/mmbiz_png/fhujzoQe7Tq06w3gVXehYIgQKO3U9jq87j9BMk5tfwjAUDOkDblswbpbuibnYSmWSdw9yjOOQ6qibPzxaxsfibtuQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```python
>>> greetings = "hello"

>>> f"She says {greetings:>10}"
'She says      hello'

# Pad 10 char to the right
>>> f"{greetings:>10}"
'     hello'

>>> f"{greetings:<10}"
'hello     '

# You can omit the < for left padding
>>> f"{greetings:10}"
'hello     '
```

![图片](https://mmbiz.qpic.cn/mmbiz_png/fhujzoQe7Tq06w3gVXehYIgQKO3U9jq8QBIwuSEZ0QQPPFamlNIcN22nvuL5FFodiaXFUKQGYw1nq4x3VXXyX9w/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```python
>>> a = "1"

>>> b = "21"

>>> c = "321"

>>> d = "4321"

>>> print("\n".join((f"{a:>10}", f"{b:>10}", f"{c:>10}", f"{d:>10}")))
         1
        21
       321
      4321
```

##### **11、如何转义符号**

如果你想想打印由大括号括起来的变量名称，而不是该变量的值，那你需要双层大括号 {{<expr>}}。

```python
>>> hello = "world"

>>>f"{{hello}} = {hello}"
'{hello} = world'
```

而如果你想转义双引号，就需要在引号前用反斜线 \ 做标记。

```python
>>>f"{hello} = \"hello\""
'world = "hello"'
```

##### **12、如何使字符串居中**

![图片](https://mmbiz.qpic.cn/mmbiz_png/fhujzoQe7Tq06w3gVXehYIgQKO3U9jq8GiaDqsX62ibQLothrxguS3n0txhuuh2ODmF8wh9954p3xUE3193DxAnw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

想要实现字符串居中，可以通过 var:^N 的方式。其中var是你想要打印的变量，N是字符串长度。如果N小于var的长度，会打印全部字符串。

```python
>>> hello = "world"
>>>f"{hello:^11}"

'  world   '
>>>f"{hello:*^11}"
'***world***'

# Extra padding is added to the right
>>>f"{hello:*^10}"
'**world***'

# N shorter than len(hello)
>>>f"{hello:^2}"
'world'
```

##### **13、如何格式化千分位**

![图片](https://mmbiz.qpic.cn/mmbiz_png/fhujzoQe7Tq06w3gVXehYIgQKO3U9jq8nT76NzzZjqpB1aMwSJvxgIH91gR7oTn83PgYzjw6ZNC9oQsBg0ELpQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

F-string也允许我们自定义数字显示的格式。有个非常普遍的需求就是把数字以每3位为一个间隔使用下划线进行分隔

```python
>>> big_num = 1234567890

>>> f"{big_num:_}"
'1_234_567_890'
```

##### **13.1  如何使用逗号千分位分隔符数字**

实际上，你可以随便用任何符号做千分位分隔符。所以用逗号做分隔符也完全没问题

```python
>>> big_num = 1234567890

>>> f"{big_num:,}"
'1,234,567,890'
```

甚至可以一次性同时搞定既有千分位分隔符又有精度设定的浮点数。

```python
>>> num =2343552.6516251625
>>> f"{num:,.3f}"
‘2,343,552.652'
```

##### **13.2 如何用空格做千分位分隔符**

 

```python
>>> big_num = 1234567890
>>> f"{big_num:,}".replace(',',' ')'
1 234 567 890'
```

##### **14、如何用科学计数法（指数计数法）显示一个数字**

可以用 e 或者 E 字符来格式化。

```python

>>> num =2343552.6516251625
>>>f"{num:e}"

'2.343553e+06'
>>> f"{num:E}"

'2.343553E+06'
>>> f"{num:.2e}"

'2.34e+06'
>>> f"{num:.4E}"
'2.3436E+06'
```

##### **15、在 f-string 中使用 if-else**

F-string也能计算稍微复杂的运算式，比如if/else

```python
>>> a = "this is a"
>>> b = "this is b"

>>> f"{a if 10 > 5 else b}"
'this is a'

>>> f"{a if 10 < 5 else b}"
'this is b'
```

##### **16、如何在 f-string 中使用字典**

你可以在f-string中使用字典。唯一的要求是引起整个字符串的引号要跟内部的引号不一样。

```python
>>>color = {"R": 123, "G": 145, "B": 255}
>>> f"{color['R']}"
'123'
>>> f'{color["R"]}'

‘’123'此处有误啊应该是‘123’吧
>>> f"RGB = ({color['R']},{color['G']}, {color['B']})"

'RGB = (123, 145, 255)’
```

##### **17、如何用 f-string 拼接字符串**

合并f-string与普通字符串拼接一样，可以隐式的直接拼接，或者显式地用加号 +，或者使用 str.join 方法。

```python
# 隐式字符串拼接
>>> f"{123}" " = "f"{100}" " + " f"{20}" " + "f"{3}"
'123 = 100 + 20 + 3'

# 使用加号 + 的显式字符串拼接
>>> f"{12}" + " != "+ f"{13}"
'12 != 13'

# 使用str.join的字符串拼接
>>> "".join((f"{13}", f"{45}"))
'13 45'

>>>"#".join((f"{13}", f"{45}"))
'13#45'
```

##### **18、如何格式化 datetime 对象**

F-string也支持datetime对象的格式化。其过程与str.format格式化日期的方法很近似。请查阅官方文档中的表格获取更多所支持格式的相关信息。

![图片](https://mmbiz.qpic.cn/mmbiz_png/fhujzoQe7Tq06w3gVXehYIgQKO3U9jq8bcLY9czFckRrOUa5GoZcwmTFC8fW4vypX2glbyKMhg7K7doGtaoiccw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

```python
>>> import datetime
>>> now = datetime.datetime.now()
>>> ten_days_ago = now -datetime.timedelta(days=10)
>>> f'{ten_days_ago:%Y-%m-%d %H:%M:%S}'

'2020-10-13 20:24:17'
>>> f'{now:%Y-%m-%d %H:%M:%S}'
'2020-10-23 20:24:17'
```

##### **19、如何修复f-string的非法格式错误**

如果用的不对，f-string会报格式错误。最常见的错误就是双引号里面套双引号。单引号也会引发相同错误。

```python
>>>color = {"R": 123, "G": 145, "B": 255}

>>> f"{color["R"]}"
  File"<ipython-input-43-1a7f5d512400>", line 1
   f"{color["R"]}"
   ^
SyntaxError: f-string: unmatched '['

>>> f'{color['R']}'
  File"<ipython-input-44-3499a4e3120c>", line 1
   f'{color['R']}'
   ^
SyntaxError: f-string: unmatched '['
```

还有个常见错误是在旧版本python中用f-string。python3.6才引入了f-string。如果你在之前版本中使用这个方法，解释器会报格式错误 SyntaxError: invalid syntax。

```python
>>> f"this is an old version"
 File"<stdin>", line 1
   f"this is an old version"

SyntaxError: invalid syntax
```

看到这个错误的话，先确定当前使用的python版本。我检查的方法是在python2.7下通过调用sys.version来获取版本号。

```python
>>> import sys;print(sys.version)
2.7.18 (default, Apr 202020, 19:27:10)
[GCC 8.3.0]
```

##### **20、如何在字符串前补零**

可以用{expr:0len} 这个方法来进行字符串补零。len是最终返回字符串的长度。还可以增加一个正负号标记。在这种情况下，用+则无论数值为正负数都将显示相应正负号。用-则只有当数值为负数时才显示负号，默认设定也是如此。更多信息可参考该链接

https://docs.python.org/3/library/string.html#format-specification-mini-language

```python
>>> num = 42

>>> f"{num:05}"
'00042'

>>> f'{num:+010}'
'+000000042'

>>> f'{num:-010}'
'0000000042'

>>> f"{num:010}"
'0000000042'

>>> num = -42

>>> f'{num:+010}'
'-000000042'

>>> f'{num:010}'
'-000000042'

>>> f'{num:-010}'
'-000000042'
```

##### **21、如何处理多行f-string（换行符的处理）**

你可以用换行符\n来打印多行文本。

```python
>>> multi_line = (f'R: {color["R"]}\nG: {color["G"]}\nB: {color["B"
    ...: ]}\n')

>>> multi_line
'R: 123\nG: 145\nB: 255\n'

>>> print(multi_line)
R: 123
G: 145
B: 255
```

还可以用三引号实现多行字符串。这样不单能增加换行符，还能有Tab。

```python
>>> other = f"""R:{color["R"]}
    ...: G:{color["G"]}
    ...: B:{color["B"]}
    ...:"""
>>> print(other)

R: 123
G: 145
B: 255
```

用 Tab 的代码样例

```python
>>> other = f'''
    ...:this is an example
    ...:
    ...:^Iof color {color["R"]}
   ...:    
    ...: '''

>>> other

'\nthis is an example\n\n\tof color 123\n    \n'

>>> print(other)
this is an example
    of color123

>>>
```



[参考](https://mp.weixin.qq.com/s/YKbWor-BHlnahNHOt3rYDQ)