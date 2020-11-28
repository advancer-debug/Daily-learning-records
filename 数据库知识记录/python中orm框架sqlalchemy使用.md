
[TOC]

### python中orm框架sqlalchemy使用
游标指针 cursor() execute()执行sql命令语句

#### 1.简介
&emsp;&emsp;sqlalchemy是python中开源的orm框架，用于简化在python中对数据库的操作。这里对sqlalchemy中的常用操作进行介绍。
#### 2.准备
官网地址<https://docs.sqlalchemy.org/en/14/> 
```
pip3 install sqlalchemy
```
#### 3.使用
##### 3.1创建映射对象
&emsp;&emsp;定义对象类，属性字段与对应表字段关联，同时可指定默认值等属性，示例如下： 
```
# 基类
Base = declarative_base()
class Stu(Base):
    # 设置表名
    __tablename__ = 'stu'

    # 属性名与表中字段名映射
    id = Column('id', Integer, primary_key=True)
    no = Column('no', String)
    # server_default为默认值,text为文本表示
    stuName = Column('stu_name', String, server_default='')
    createTime = Column('create_time', DateTime, server_default=text('NOW()'))

    # 返回对象的字符串表示
    def __repr__(self) -> str:
        return str(self.__dict__)
```
##### 3.2创建数据库连接
&emsp;&emsp;指定要连接的数据库，创建会话，同时可根据需要设置相关参数，示例如下：
```
# 连接地址,格式为 mysql+pymysql://[账号]:[密码]@[主机]:[端口]/[数据库]?charset=utf8"
url = 'mysql+pymysql://root:root@127.0.0.1:3306/school?charset=utf8'
# echo为True时，打印sql,可用于调试
engine = create_engine(url, echo=False, encoding='utf-8', pool_size=5)
sessionClass = sessionmaker(bind=engine)
# 创建会话
session = sessionClass()

# 使用完后关闭会话
# session.close()
```
##### 3.3查询
######3.3.1常用查询
&emsp;&emsp;这里列中常用查询，包含排序、分组、条件查询、个数查询、单个查询、列表查询等，具体请看示例代码：
```
# 查所有,并排序
stuList = session.query(Stu).order_by(Stu.id).all()

# 查询指定属性并遍历,方式一
for id, no in session.query(Stu.id, Stu.no):
    print("id:{} no:{}".format(id, no))

# 查询指定属性并遍历,方式二
for t in session.query(Stu.id, Stu.no).all():
    print("id:{} no:{}".format(t.id, t.no))

# 查所有,并排序
stuList = session.query(Stu).order_by(Stu.id).all()
# 分页查询
stuList = session.query(Stu).limit(2).offset(0).all()

# 查询个数
stuList = session.query(Stu).count()
# 查询个数，scalar（）表示返回第一个结果的第一个元素
cnt = session.query(func.count('*')).select_from(Stu).scalar()
# 查询个数,带条件统计
cnt = session.query(func.count('*')).select_from(Stu).filter(Stu.id>2).scalar()
# 根据id统计
cnt = session.query(func.count(Stu.id)).scalar()

# 指定条件查询
stuList = session.query(Stu).filter(Stu.id > 2, Stu.createTime < datetime.datetime.now()).all()
# 获取第一个,没有则抛异常
# stu = session.query(Stu).filter(Stu.id==2).one()
# 获取第一个,没有则返回None
stu = session.query(Stu).filter(Stu.id == 1).first()
# 获取第一个,没有则返回None
stu = session.query(Stu).filter(Stu.id == 2).one_or_none()
# group by查询
stuList = session.query(func.count('*'), Stu.stuName).filter(or_(Stu.id > 2, Stu.stuName == 'apple1')).group_by(
    Stu.stuName).all()
```
###### 3.3.2条件查询
&emsp;&emsp;这里列出常用的条件查询，示例如下： 
```
# 相等查询
stuList = session.query(Stu).filter(Stu.id == 2).all()
# 不等查询
stuList = session.query(Stu).filter(Stu.id != 2).all()
# 大于查询
stuList = session.query(Stu).filter(Stu.id > 2).all()
# in查询
stuList = session.query(Stu).filter(Stu.id.in_([82, 83])).all()
# not in 查询
stuList = session.query(Stu).filter(~Stu.id.in_([82, 83])).all()
# 嵌套查询
stuList = session.query(Stu).filter(Stu.id.in_(session.query(Stu.id).filter(Stu.id <= 83))).all()
# like查询(不同后端时,有时大小写不敏感)
stuList = session.query(Stu).filter(Stu.stuName.like('Apple%')).all()
# like查询(明确大小写不敏感)
stuList = session.query(Stu).filter(Stu.stuName.ilike('Apple%')).all()
# null查询
stuList = session.query(Stu).filter(Stu.stuName.is_(None)).all()
# not null查询
stuList = session.query(Stu).filter(Stu.stuName.isnot(None)).all()
# and查询
stuList = session.query(Stu).filter(Stu.id > 2, Stu.stuName == 'apple1').all()
# or查询
stuList = session.query(Stu).filter(or_(Stu.id > 2, Stu.stuName == 'apple1')).all()
# 多级过滤
stuList = session.query(Stu).filter(Stu.id > 2).filter(Stu.stuName == 'apple1').all()
```
###### 3.3.3直接sql语句查询
&emsp;&emsp;除了sqlalchemy带的查询方法，还可直接使用sql语句查询，使用如下： 
```
# 直接使用sql语句查询(只有条件sql语句)
stuList = session.query(Stu).filter(text("id>2 and stu_name='apple1'")).order_by(text("id")).all()
# 直接使用sql语句查询(完整的sql语句)
stuList = session.query(Stu).from_statement(
    text("select * from stu where id>:id and stu_name=:name order by id").params(id=2, name='apple1')).all()
```
##### 3.4插入
###### 3.4.1单条插入 
```
# 单条插入
stu = Stu(no='86', stuName='apple86', createTime=datetime.datetime.now())
session.add(stu)
session.commit()
```
###### 3.4.2批量插入
```
# 批量插入
stuList = [Stu(id=83, no='83', stuName='apple83', createTime=datetime.datetime.now()), Stu(id=84, no='84', stuName='apple84')]
session.add_all(stuList)
session.commit()
```
###### 3.4.3使用sql语句插入
```
# 直接使用sql语句,用Stu对象转dict插入
stu = Stu(id=91, no='2', stuName='tree4', createTime=datetime.datetime.now())
session.execute("insert into stu(no, stu_name) value(:no, :stuName)", stu.__dict__)

# 直接使用sql语句,用stu映射
stu_obj = {'id': 3, 'no': '3', 'stuName': 'tree3', 'createTime': datetime.datetime.now()}
session.execute("insert into stu(no, stu_name) value(:no, :stuName)", stu_obj)
```
###### 3.4.4忽略已存在的插入
&emsp;&emsp;若数据已经存在，则不插入，否则直接插入。 
```
# 直接使用sql语句,用stu映射,若对象已存在,则忽略
stu = Stu(id=91, no='2', stuName='tree4', createTime=datetime.datetime.now())
session.execute("insert ignore into stu(no, stu_name) value(:no, :stuName)", stu.__dict__)
```
###### 3.4.5更新插入
&emsp;&emsp;若数据已经存在，则做更新操作，否则直接插入。 
```
# 直接使用sql语句,若对象已存在,则更新
stu = Stu(id=91, no='2', stuName='tree4', createTime=datetime.datetime.now())
session.execute("insert into stu(no, stu_name) value(:no, :stuName) on duplicate key update stu_name=values(stu_name)", stu.__dict__)
```
##### 3.5更新
&emsp;&emsp;更新时，流程是先查出对象,再对对象修改,最后直接commit。使用示例如下：
```
# 更新,流程:先查出对象,再对对象修改,最后直接commit
stu = session.query(Stu).filter(Stu.id==82).first()
stu.stuName ='rice1'
session.commit()

# 更新(根据条件可批量更新),流程:查对象同时进行修改,最后直接commit
session.query(Stu).filter(Stu.id >= 85).update({Stu.stuName: 'tree1'})
session.commit()
```
##### 3.6删除
&emsp;&emsp;删除同更新类似,流程是先查出对象,再删除对象delete,最后直接commit。使用示例如下：（物理删除）
```
# 删除,流程:先查出对象,再删除对象delete,最后直接commit
stu = session.query(Stu).filter(Stu.id==83).first()
session.delete(stu)
session.commit()

# 删除(根据条件可批量删除),流程:查出对象同时删除对象delete,最后直接commit
session.query(Stu).filter(Stu.id >= 85).delete()
session.commit()
```


#### 使用
![](https://img2018.cnblogs.com/blog/1699309/201907/1699309-20190725153802749-534006379.png)

- 1.创建自定义类--数据库表 
   - 数据库结构 id=Column()

  ```
  from sqlalchemy import create_engine, Column, INT, VARCHAR
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy.orm import sessionmaker   
  # 创建基类，返回一个定制的metaclass 类
  Base = declarative_base()
  
  # 自定义类
  class Student(Base):
    # 表名
      __tablename__ = 'student'
    # 字段映射
      id = Column('id', INT, primary_key=True)
      name = Column('name', VARCHAR)
      code = Column('code', VARCHAR)
      sex = Column('sex', VARCHAR)
 
    def to_dict(self):
        """
        将查询的结果转化为字典类型
        Student 对象的内容如下 {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x10174c898>, 'sex': 'nan', 'name': 'ygh', 'code': 'AU', 'school': 'hua'}
        获取其值剔除 "_sa_instance_state 即可。但不能在self.__dict__上直接删除”_sa_instance_state” 这个值是公用的。
        :return:
        """
        return {k: v for k, v in self.__dict__.items() if k != "_sa_instance_state”}
  ```
或者 
  ```
  def __repr__(self):
     """命令运行时，打印对象显示的值调用"""
     return "<Student(id='%s', name='%s', code='%s',sex='%s')>" %(self.id, self.name, self.code, self.sex)
  ```
  ```
  CREATE TABLE `student` (
    `id` int(2) NOT NULL AUTO_INCREMENT,
    `name` char(20) NOT NULL,
    `code` char(64) NOT NULL,
    `sex` char(4) NOT NULL,
    PRIMARY KEY (`id`) USING BTREE
  ) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
  ```
  - 创建会话连接
 ```
 # 创建引擎 , echo=True ,表示需要开启 sql 打印，调试的以后特别好用
 engine =create_engine("mysql+mysqldb://root:123qwe@192.168.1.254:3306/yinguohai", pool_size=2, max_overflow=0, echo=True
 # 创建会话对象，用于操作数据库
 Session = sessionmaker(bind=engine)
 session = Session()
 ```

- 2.数据库表操作 all() filter first() like in_ and_ or_ asc() desc() count
  distinct()
   ```
   #查询所有
   result = session.squery(Student).all()
   #部分查询
   result = session.query(Student.id, Student.name).all()
   #多条件查询，or_,and_
   result = session.query(Student).filter(or_(Student.name == "Bob", Student.sex != "aa")).first()
   #模糊查询
   result = session.query(Student).filter(Student.sex.like('%bo%')).first()
   范围查询
   result = session.query(Student).filter(Student.name.in_(["Bob", "Smith"])).all()
   #排序
   #result = session.query(Student).order_by(Student.id.desc()).all()
   result = session.query(Student).order_by(Student.id.asc()).all()
   #限制，limit ， slice offset
   result = session.query(Student).limit(2).all()
   result = session.query(Student).order_by(Student.id.asc()).slice(2, 3).all()
   #统计
   result = session.query(Student).count()
   #去重,distinct()
   result = session.query(Student.name).distinct(Student.name).all()
   #联合查询,默认 inner join查询
   result = session.query(Student.id, Student.code, Student.name, Country.population).join(Country, Student.code == Country.code).all()
   #单独查询一行，如果存在则返回对象，不存在返回None
   user_obj = session.query(User).filter(User.id == '222').scalar()
   ```
   sql语句 
   ```
   
   ```
   区别于查询，需要提交事务才能生效 
   ```
   #添加,add() , add_all()
   result = session.add(Student(name="Bob", code="AU", sex="boy"))
   session.commit()
   
   result = session.add_all([
    Student(name="Smith", code="BM", sex="girl"),
    Student(name="Hub", code="BU", sex="boy"),
    Student(name="Hip", code="HK", sex="boy"),
    ])
   session.commit()
   
   #更新,update()
   result = session.query(Student).filter(Student.id == 1).update({Student.sex: "dddd”})
   # 如果想回滚，则使用 session.rollback() 回滚即可
   session.commit()
   
   #不存在则插入，存在则更新,on_duplicate_key_update()
   insert_smt = insert(Student).values(id=1, name="bb", code="AA", sex="boy").on_duplicate_key_update(sex="aaaaa",code="uuuuu")
   result = session.execute(insert_smt)
   session.commit()
   ```
   注意事项：

    需要引入 一个特别函数 , insert( ) , 它是mysql包下的。from sqlalchemy.dialects.mysql import insert
    
    使用 on_duplicate_key_update( ) 这个函数进行异常处理，别用错了
    
    使用execute ， 执行insert( ) 函数创建的 Sql 语句即可
    
    最后一定要记得 commit( ) 一下。

- 对用的sql语句
 
  - 查询
   
  ```	
  SELECT
      student.id AS student_id,
      student.NAME AS student_name,
      student.CODE AS student_code,
      student.sex AS student_sex
  FROM student
  
  #多条件查询
  FROM student
  WHERE student.NAME = % s OR student.sex != % s ( 'Bob', 'aa', 1 )
  
  #模糊查询
  FROM student
  WHERE student.sex LIKE % s LIMIT %s  ('%bo%', 1)
  
  #范围查询
  FROM student
  WHERE student.NAME IN (% s, % s ) ( 'Bob', 'Smith' )
  
  #排序
  FROM student ORDER BY student.id ASC
  
  #限制
  FROM student LIMIT % s (2,)
  
  #统计
  SELECT count(*) AS count_1
  FROM
    ( SELECT student.id AS student_id, student.NAME AS student_name, student.CODE AS student_code, student.sex AS student_sex FROM student ) AS anon_1
  
  #去重
  SELECT DISTINCT
    student.NAME AS student_name
  FROM student
  
  #联合查询
  FROM student
    INNER JOIN a_country ON student.CODE = a_country.CODE
    
  #添加
  BEGIN 
  INSERT INTO student (name, code, sex) VALUES (%s, %s, %s) ('Smith', 'BM', 'girl')
  COMMIT
  
  #更新
  BEGIN 
  UPDATE student SET sex=%s WHERE student.id = %s ('dddd', 1)
  COMMIT
  
  #不存在则插入，存在则更新,on_duplicate_key_update()
  BEGIN
  INSERT INTO student ( id, NAME, CODE, sex )
  VALUES (% s, % s, % s, % s )
  ON DUPLICATE KEY UPDATE code = %s, sex = %s
  (1, 'bb', 'AA', 'boy', 'uuuuu', 'aaaaa')
  COMMIT
  
  #算表中所有列数据行记录总数
  user_count = session.query(func.count('*')).select_from(User).scalar()
  
  #单独查询一行，如果存在则返回对象，不存在抛出sqlalchemy.orm.exc.NoResultFound异常
  user_obj = session.query(User).filter(User.id == 1).one()
  ``` 
  `session.new`的案例，主要作用：打印出已增加的数据，但是未提交至数据库的数据
  
  `session.dirty`案例，主要作用：打印出已增加到session中，未提交至数据库，但是在这个过程中又被修改的数据，也叫脏读

- 数据库表删除迁移 
 
 # 删除所有表 `Base.metadata.drop_all(engine)`

 # 创建所有表 `Base.metadata.create_all(engine)`

   

参考链接

- <https://blog.csdn.net/chinabestchina/article/details/89816798?utm_medium=distribute.pc_relevant.none-task-blog-title-2&spm=1001.2101.3001.4242>
- <https://www.osgeo.cn/sqlalchemy/index.html>
- <https://www.jianshu.com/p/0ad18fdd7eed>
- <https://www.cnblogs.com/superscfan/p/12256949.html>
- <https://www.cnblogs.com/yinguohai/p/11243834.html>




















