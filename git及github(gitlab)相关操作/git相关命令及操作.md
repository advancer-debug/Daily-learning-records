[TOC]
## Git常用命令及方法大全
  
- Workspace：工作区
- Index / Stage：暂存区
- Repository：仓库区（或本地仓库）
- Remote：远程仓库
![关系图示](https://imgconvert.csdnimg.cn/aHR0cDovL3d3dy5ydWFueWlmZW5nLmNvbS9ibG9naW1nL2Fzc2V0LzIwMTUvYmcyMDE1MTIwOTAxLnBuZw?x-oss-process=image/format,png)

- 工作区域关系图
![工作区域关系](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAyMC82LzI2LzE3MmYwMmZjNzU4ZWQ5NmQ?x-oss-process=image/format,png)
- 1 本地分支关联远程

  `git branch --set-upstream-to=origin/分支名 分支名`
  
  代码库修改密码后push不上去怎么办？
  
  重新输入密码`git config --system --unset credential.helper`
 
  密码存储同步`git config --global credential.helper store`
  
### 一、新建代码库
  
  - 1.在当前目录新建一个Git代码库
     
     `$ git init`
 
  - 2.新建一个目录，将其初始化为Git代码库
      
      `$ git init [project-name]`
 
  - 3.下载一个项目和它的整个代码历史
  
       `$ git clone [url]`

### 二、配置
  - Git的设置文件为.gitconfig，它可以在用户主目录下（全局配置），也可以在项目目录下（项目配置）。
  
  - 1.显示当前的Git配置
     `$ git config --list`
 
  - 2.编辑Git配置文件
     `$ git config -e [--global]`
 
  - 3.设置提交代码时的用户信息
     `$ git config [--global] user.name "[name]"`
     `$ git config [--global] user.email "[email address]"`
  
### 三、增加/删除文件
     # 添加指定文件到暂存区
     $ git add [file1] [file2] ...
     # 添加指定目录到暂存区，包括子目录
     $ git add [dir]
     # 添加当前目录的所有文件到暂存区
     $ git add .
     # 添加每个变化前，都会要求确认
       #对于同一个文件的多处变化，可以实现分次提交
     $ git add -p`
     # 删除工作区文件，并且将这次删除放入暂存区
     $ git rm [file1] [file2] ...
     # 停止追踪指定文件，但该文件会保留在工作区
     $ git rm --cached [file]
     # 改名文件，并且将这个改名放入暂存区
     $ git mv [file-original] [file-renamed]
     
     使用git命令删除GitHub上的文件或文件夹
    # 删除名字为.idea的文件夹
    git rm -r --cached .idea 
    # 提交到git
    git commit -m '删除.idea文件夹'
     
    # 推送到GitHub
    git push -u origin master
### 四、代码提交
     # 提交暂存区到仓库区
     $ git commit -m [message]
     # 提交暂存区的指定文件到仓库区
     $ git commit [file1] [file2] ... -m [message]
     # 提交工作区自上次commit之后的变化，直接到仓库区
     $ git commit -a
     # 提交时显示所有diff信息
     $ git commit -v
     # 使用一次新的commit，替代上一次提交
     # 如果代码没有任何新变化，则用来改写上一次commit的提交信息
     $ git commit --amend -m [message]
     # 重做上一次commit，并包括指定文件的新变化
     $ git commit --amend [file1] [file2] ...
### 五、分支     
     # 列出所有本地分支
     $ git branch
     # 列出所有远程分支
     $ git branch -r
     # 列出所有本地分支和远程分支
     $ git branch -a
     # 新建一个分支，但依然停留在当前分支
     $ git branch [branch-name]
     # 以远程分支为基础新建一个分支，并切换到该分支
     $ git checkout -b [branch] origin/[remote-branch]
     # 新建一个分支，指向指定commit
     $ git branch [branch] [commit]
     # 新建一个分支，与指定的远程分支建立追踪关系
     $ git branch --track [branch] [remote-branch]
     # 切换到指定分支，并更新工作区
     $ git checkout [branch-name]
     # 切换到上一个分支
     $ git checkout -
     # 建立追踪关系，在现有分支与指定的远程分支之间
     $ git branch --set-upstream [branch] [remote-branch]
     # 合并指定分支到当前分支
     $ git merge [branch]
     # 选择一个commit，合并进当前分支
     $ git cherry-pick [commit]
     # 删除分支
     $ git branch -d [branch-name]
     # 删除远程分支
     $ git push origin --delete [branch-name]
     $ git branch -dr [remote/branch]
### 六、标签
    # 列出所有tag
    $ git tag
    # 新建一个tag在当前commit
    $ git tag [tag]
    # 新建一个tag在指定commit
    $ git tag [tag] [commit]
    # 删除本地tag
    $ git tag -d [tag]
    # 删除远程tag
    $ git push origin :refs/tags/[tagName]
    # 查看tag信息
    $ git show [tag]
    # 提交指定tag
    $ git push [remote] [tag]
    # 提交所有tag
    $ git push [remote] --tags
    # 新建一个分支，指向某个tag
    $ git checkout -b [branch] [tag]
### 七、查看信息
    # 显示有变更的文件
    $ git status
    # 显示当前分支的版本历史
    $ git log
    # 显示commit历史，以及每次commit发生变更的文件
    $ git log --stat
    # 搜索提交历史，根据关键词
    $ git log -S [keyword]
    # 显示某个commit之后的所有变动，每个commit占据一行
    $ git log [tag] HEAD --pretty=format:%s
    # 显示某个commit之后的所有变动，其"提交说明"必须符合搜索条件
    $ git log [tag] HEAD --grep feature
    # 显示某个文件的版本历史，包括文件改名
    $ git log --follow [file]
    $ git whatchanged [file]
    # 显示指定文件相关的每一次diff
    $ git log -p [file]
    # 显示过去5次提交
    $ git log -5 --pretty --oneline
    # 显示所有提交过的用户，按提交次数排序
    $ git shortlog -sn
    # 显示指定文件是什么人在什么时间修改过
    $ git blame [file]
    # 显示暂存区和工作区的差异
    $ git diff
    # 显示暂存区和上一个commit的差异
    $ git diff --cached [file]
    # 显示工作区与当前分支最新commit之间的差异
    $ git diff HEAD
    # 显示两次提交之间的差异
    $ git diff [first-branch]...[second-branch]
    # 显示今天你写了多少行代码
    $ git diff --shortstat "@{0 day ago}"
    # 显示某次提交的元数据和内容变化
    $ git show [commit]
    # 显示某次提交发生变化的文件
    $ git show --name-only [commit]
    # 显示某次提交时，某个文件的内容
    $ git show [commit]:[filename]
    # 显示当前分支的最近几次提交
    $ git reflog
### 八、远程同步
    # 下载远程仓库的所有变动
    $ git fetch [remote]
    # 显示所有远程仓库
    $ git remote -v
    # 显示某个远程仓库的信息
    $ git remote show [remote]
    # 增加一个新的远程仓库，并命名
    $ git remote add [shortname] [url]
    # 取回远程仓库的变化，并与本地分支合并
    $ git pull [remote] [branch]
    # 上传本地指定分支到远程仓库
    $ git push [remote] [branch]
    # 强行推送当前分支到远程仓库，即使有冲突
    $ git push [remote] --force
    # 推送所有分支到远程仓库
    $ git push [remote] --all
### 九、撤销
    # 恢复暂存区的指定文件到工作区
    $ git checkout [file]
    # 恢复某个commit的指定文件到暂存区和工作区
    $ git checkout [commit] [file]
    # 恢复暂存区的所有文件到工作区
    $ git checkout .
    # 重置暂存区的指定文件，与上一次commit保持一致，但工作区不变
    $ git reset [file]
    # 重置暂存区与工作区，与上一次commit保持一致
    $ git reset --hard
    # 重置当前分支的指针为指定commit，同时重置暂存区，但工作区不变
    $ git reset [commit]
    # 重置当前分支的HEAD为指定commit，同时重置暂存区和工作区，与指定commit一致
    $ git reset --hard [commit]
    # 重置当前HEAD为指定commit，但保持暂存区和工作区不变
    $ git reset --keep [commit]
    # 新建一个commit，用来撤销指定commit
    # 后者的所有变化都将被前者抵消，并且应用到当前分支
    $ git revert [commit]
    # 暂时将未提交的变化移除，稍后再移入
    $ git stash
    $ git stash pop
### 十 另加
    # 生成一个可供发布的压缩包
    $ git archive
## Git分支管理策略
### 一、主分支Master
&ensp;&ensp;首先，代码库应该有一个、且仅有一个主分支。所有提供给用户使用的正式版本，都在这个主分支上发布。

![图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL3d3dy5ydWFueWlmZW5nLmNvbS9ibG9naW1nL2Fzc2V0LzIwMTIwNy9iZzIwMTIwNzA1MDMucG5n?x-oss-process=image/format,png)

&ensp;&ensp;Git主分支的名字，默认叫做Master。它是自动建立的，版本库初始化以后，默认就是在主分支在进行开发。
### 二、开发分支Develop
&ensp;&ensp;主分支只用来分布重大版本，日常开发应该在另一条分支上完成。我们把开发用的分支，叫做Develop。

![图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL3d3dy5ydWFueWlmZW5nLmNvbS9ibG9naW1nL2Fzc2V0LzIwMTIwNy9iZzIwMTIwNzA1MDQucG5n?x-oss-process=image/format,png)

&ensp;&ensp;这个分支可以用来生成代码的最新隔夜版本（nightly）。如果想正式对外发布，就在Master分支上，对Develop分支进行"合并"（merge）。

   Git创建Develop分支的命令:
   
   `$ git checkout -b develop master`
   
   将Develop分支发布到Master分支的命令：
    
   `# 切换到Master分支`
　 `$ git checkout master`
　 `# 对Develop分支进行合并`
　 `$ git merge --no-ff develop`

## 版本回退撤销文件修改

   - 当然可以直接手动再在工作区中将文件修改回去
   - 修改后，通过命令git status查看
   Git会告诉你，git checkout -- file可以丢弃工作区的修改：
   `$ git checkout -- readme.txt`
   
  <font face="黑体">Note:</font>
  - git checkout -- file命令中的--很重要，没有--，就变成了“切换到另一个分支”的命令，我们在后面的分支管理中会再次遇到git checkout命令。

  - 命令git checkout -- readme.txt意思就是，把readme.txt文件在工作区的修改全部撤销，这里有两种情况：
    - 1.一种是readme.txt自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库一模一样的状态；
    - 2.一种是readme.txt已经添加到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。总之，就是让这个文件回到最近一次git commit或git add时的状态。
   
## 如果在工作区中修改了文件还git add到暂存区（但是在commit之前）
   用git status查看一下，修改只是添加到了暂存区，还没有提交：
   
    $ git status
    $ On branch master
    $ Changes to be committed:
    $ (use "git reset HEAD <file>..." to unstage)
    $ modified:   readme.txt

   Git同样告诉我们，用命令git reset HEAD file可以把暂存区的修改撤销掉（unstage），重新放回工作区：
   
    $ git reset HEAD readme.txt
    $ Unstaged changes after reset:
      M       readme.txt
   git reset命令既可以回退版本，也可以把暂存区的修改回退到工作区。当我们用HEAD时，表示最新的版本。

   再用git status查看一下，现在暂存区是干净的，工作区有修改。
   
## 不但修改了文件还从暂存区提交commit到了版本库 - 版本回退
  版本回退可以回退到上一个版本。不过，这是有条件的，就是你还没有把自己的本地版本库推送到远程。Git是分布式版本控制系统。
  在工作中对某个文件（如readme.txt）进行多次修改交commit。
  可以通过版本控制系统命令告诉我们提交的历史记录，在Git中，我们用git log命令查看：
  
  <font face="黑体">Note:</font>
  - 1. git log命令显示从最近到最远的提交日志，我们可以看到3次提交，最近的一次是append GPL，上一次是add distributed，最早的一次是wrote a readme file。
  - 2. 如果嫌输出信息太多，看得眼花缭乱的，可以试试加上--pretty=oneline参数：
       
   `$ git log --pretty=oneline`
   `3628164fb26d48395383f8f31179f24e0882e1e0 append GPL`
   `ea34578d5496d7dd233c827ed32a8cd576c5ee85 add distributed`
   `cb926e7ea50ad11b8f9e909c05226233bf755030 wrote a readme file`
   
   可以使用git reset命令：
    
   `$ git reset --hard HEAD^`
   `HEAD is now at ea34578 add distributed`
   
### git工作原理图
![图片描述](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAyMC82LzIyLzE3MmRjODVkYmZmZDllZTk?x-oss-process=image/format,png)
 
### git基本命令使用的大概流程
![图片描述](https://imgconvert.csdnimg.cn/aHR0cHM6Ly91c2VyLWdvbGQtY2RuLnhpdHUuaW8vMjAyMC82LzI1LzE3MmVjMDhlZGU1MWQwNTY?x-oss-process=image/format,png)

#### 参考地址
<https://blog.csdn.net/WEB_CSDN_SHARE/article/details/79243308#t12>

<https://blog.csdn.net/weiwenhou/article/details/106985423?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.channel_param#t19>