
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




























