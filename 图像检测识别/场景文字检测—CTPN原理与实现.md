### 场景文字检测—CTPN原理与实现

![场景文字检测—CTPN原理与实现](https://pic1.zhimg.com/v2-2ea98126ebc05e35be28efe598a021ed_1440w.jpg?source=172ae18b)

对于复杂场景的文字识别，首先要定位文字的位置，即文字检测。

CTPN是在ECCV  2016提出的一种文字检测算法。CTPN结合CNN与LSTM深度网络，能有效的检测出复杂场景的横向分布的文字，效果如图1，是目前比较好的文字检测算法。由于CTPN是从Faster RCNN改进而来，本文默认读者熟悉CNN原理和Faster RCNN网络结构。

原始CTPN只检测横向排列的文字。CTPN结构与Faster R-CNN基本类似，但是加入了LSTM层。假设输入 ![[公式]](https://www.zhihu.com/equation?tex=N) Images：

- 首先VGG提取特征，获得大小为 ![[公式]](https://www.zhihu.com/equation?tex=N+%5Ctimes+C%5Ctimes+H%5Ctimes+W) 的conv5 feature map。
- 之后在conv5上做 ![[公式]](https://www.zhihu.com/equation?tex=3%C3%973) 的滑动窗口，即每个点都结合周围 ![[公式]](https://www.zhihu.com/equation?tex=3%C3%973) 区域特征获得一个长度为 ![[公式]](https://www.zhihu.com/equation?tex=3%C3%973%C3%97C) 的特征向量。输出 ![[公式]](https://www.zhihu.com/equation?tex=N+%5Ctimes9C%5Ctimes+H%5Ctimes+W) 的feature map，该特征显然只有CNN学习到的空间特征。
- 再将这个feature map进行Reshape

![img](https://pic3.zhimg.com/80/v2-74fdcc9eeee49b7fb73acb4ba8aabef2_720w.png)

- 然后以 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7BBatch%7D%3DNH) 且最大时间长度 ![[公式]](https://www.zhihu.com/equation?tex=T_%5Ctext%7Bmax%7D%3D+W) 的数据流输入双向LSTM，学习每一行的序列特征。双向LSTM输出 ![[公式]](https://www.zhihu.com/equation?tex=%28NH%29+%5Ctimes+W%5Ctimes+256) ，再经Reshape恢复形状：

![img](https://pic3.zhimg.com/80/v2-27b8e73c01bf7962c53589f78b4aba6e_720w.png)

该特征既包含空间特征，也包含了LSTM学习到的序列特征。

- 然后经过“FC”卷积层，变为 ![[公式]](https://www.zhihu.com/equation?tex=N+%5Ctimes512%5Ctimes+H%5Ctimes+W) 的特征
- 最后经过类似Faster R-CNN的RPN网络，获得text proposals，如图2-b。

##### 为何使用双向LSTM?

![img](https://pic1.zhimg.com/80/v2-8d72777321cbf1336b79d839b6c7f9fc_720w.jpg)

CNN学习的是感受野内的空间信息，LSTM学习的是序列特征。对于文本序列检测，显然既需要CNN抽象空间特征，也需要序列特征（毕竟文字是连续的）。

CTPN中使用双向LSTM，相比一般单向LSTM有什么优势？双向LSTM实际上就是将2个方向相反的LSTM连起来，如图4。

![img](https://pic1.zhimg.com/80/v2-bc5266c4587af49516adb2cee4351838_720w.jpg)

##### 如何通过"FC"卷积层输出产生图2-b中的Text proposals?

CTPN通过CNN和BLSTM学到一组“空间 + 序列”特征后，在"FC"卷积层后接入RPN网络。这里的RPN与Faster R-CNN类似，分为两个分支：

1. 左边分支用于bounding box regression。由于fc feature map每个点配备了10个Anchor，同时只回归中心y坐标与高度2个值，所以rpn_bboxp_red有20个channels
2. 右边分支用于Softmax分类Anchor

**竖直Anchor定位文字位置**

由于CTPN针对的是横向排列的文字检测，所以其采用了一组（10个）等宽度的Anchors，用于定位文字位置。Anchor宽高为：

![img](https://pic2.zhimg.com/80/v2-0d777cb27dbb89bf925ca9d90211383d_720w.png)

需要注意，由于CTPN采用VGG16模型提取特征，那么conv5 feature map的宽高都是输入Image的宽高的 ![[公式]](https://www.zhihu.com/equation?tex=1%2F16) 。同时fc与conv5 width和height都相等。

如图6所示，CTPN为fc feature map每一个点都配备10个上述Anchors。

<img src="https://pic2.zhimg.com/80/v2-93e22f54fb0231b3f763f2f8129913ad_720w.jpg" alt="img" style="zoom: 67%;" />                                                                                         图6 CTPN Anchor

这样设置Anchors是为了：

1. 保证在 ![[公式]](https://www.zhihu.com/equation?tex=x) 方向上，Anchor覆盖原图每个点且不相互重叠。
2. 不同文本在 ![[公式]](https://www.zhihu.com/equation?tex=y) 方向上高度差距很大，所以设置Anchors高度为11-283，用于覆盖不同高度的文本目标。

获得Anchor后，与Faster R-CNN类似，CTPN会做如下处理：

1. Softmax判断Anchor中是否包含文本，即选出Softmax score大的正Anchor
2. Bounding box regression修正包含文本的Anchor的**中心y坐标**与**高度**。

注意，与Faster R-CNN不同的是，这里Bounding box regression不修正Anchor中心x坐标和宽度。具体回归方式如下：

![img](https://pic3.zhimg.com/80/v2-738d5b097b64f8012cef7b9d3c05f7b2_720w.jpg)

其中， ![[公式]](https://www.zhihu.com/equation?tex=v%3D%28v_c%2C+v_h%29) 是回归预测的坐标， ![[公式]](https://www.zhihu.com/equation?tex=v%3D%28v_c%5E%2A%2C+v_h%5E%2A%29) 是Ground Truth， ![[公式]](https://www.zhihu.com/equation?tex=c_y%5Ea) 和 ![[公式]](https://www.zhihu.com/equation?tex=h%5Ea) 是Anchor的中心y坐标和高度。Bounding box regression具体原理请参考之前文章。

Anchor经过上述Softmax和 ![[公式]](https://www.zhihu.com/equation?tex=y) 方向bounding box regeression处理后，会获得图7所示的一组竖直条状text proposal。后续只需要将这些text proposal用文本线构造算法连接在一起即可获得文本位置。

![img](https://pic1.zhimg.com/80/v2-447461eb54bcc3c93992ffd1c70bcfb8_720w.jpg)

在论文中，作者也给出了直接使用Faster R-CNN RPN生成普通proposal与CTPN LSTM+竖直Anchor生成text proposal的对比，如图8，明显可以看到CTPN这种方法更适合文字检测。

![img](https://pic1.zhimg.com/80/v2-82a34bf3b3591c4a21d90e8997ed1534_720w.jpg)

##### 文本线构造算法

已经获得了图7所示的一串或多串text proposal，接下来就要采用文本线构造办法，把这些text proposal连接成一个文本检测框。

![img](https://pic4.zhimg.com/80/v2-de8098e725d168a038f197ce0707faaf_720w.jpg)图9

为了说明问题，假设某张图有图9所示的2个text proposal，即蓝色和红色2组Anchor，CTPN采用如下算法构造文本线：

1. 按照水平 ![[公式]](https://www.zhihu.com/equation?tex=x) 坐标排序Anchor
2. 按照规则依次计算每个Anchor  ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bbox%7D_i) 的 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bpair%7D%28%5Ctext%7Bbox%7D_j%29) ，组成 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bpair%7D%28%5Ctext%7Bbox%7D_i%2C+%5Ctext%7Bbox%7D_j%29) 
3. 通过 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bpair%7D%28%5Ctext%7Bbox%7D_i%2C+%5Ctext%7Bbox%7D_j%29) 建立一个Connect graph，最终获得文本检测框

下面详细解释。假设每个Anchor index如绿色数字，同时每个Anchor Softmax score如黑色数字。

**文本线构造算法通过如下方式建立每个Anchor** ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bbox%7D_i) **的** ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bpair%7D%28%5Ctext%7Bbox%7D_i%2C+%5Ctext%7Bbox%7D_j%29) **：**

正向寻找：

1. 沿水平正方向，寻找和 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bbox%7D_i) 水平距离小于50像素的候选Anchor（每个Anchor宽16像素，也就是最多正向找50/16=3个）
2. 从候选Anchor中，挑出与 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bbox%7D_i) 竖直方向 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Boverlap%7D_v+%3E0.7) 的Anchor
3. 挑出符合条件2中Softmax score最大的 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bbox%7D_j) 

再反向寻找：

1. 沿水平负方向，寻找和 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bbox%7D_j) 水平距离小于50的候选Anchor
2. 从候选Anchor中，挑出与 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bbox%7D_j) 竖直方向 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Boverlap%7D_v+%3E0.7) 的Anchor
3. 挑出符合条件2中Softmax score最大的 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bbox%7D_k) 

最后对比 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bscore%7D_i) 和 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bscore%7D_k) :

1. 如果 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bscore%7D_i+%3E%3D+%5Ctext%7Bscore%7D_k) ，则这是一个最长连接，那么设置 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7BGraph%7D%28i%2C+j%29+%3D+%5Ctext%7BTrue%7D) 
2. 如果 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctext%7Bscore%7D_i+%3C+%5Ctext%7Bscore%7D_k) ，说明这不是一个最长的连接（即该连接肯定包含在另外一个更长的连接中）。

##### CTPN的损失函数

##  

分类损失函数 ![[公式]](https://www.zhihu.com/equation?tex=L_s%5E%7Bcl%7D%28s_i%2Cs_i%5E%29) 是softmax损失函数，其中 ![[公式]](https://www.zhihu.com/equation?tex=s_i%5E%3D%5C%7B0%2C1%5C%7D) 是ground truth，即如果锚点为正锚点（前景）， ![[公式]](https://www.zhihu.com/equation?tex=s_i%5E%3D1) ，否则 ![[公式]](https://www.zhihu.com/equation?tex=s_i%5E%3D0) 。在tf的源码中(lib/rpn_msr/anchor_target_layer_tf.py)，一个锚点是正锚点的条件如下:

1. 每个位置上的9个anchor中overlap最大的认为是前景；
2. overlap大于0.7的认为是前景3

如果overlap小于0.3，则被判定为背景。在源码中参数RPN_CLOBBER_POSITIVES为true则表示如果一个样本的overlap小于0.3，且同时满足正样本的条件1，则该样本被判定为负样本。

![[公式]](https://www.zhihu.com/equation?tex=s_i) 是预测锚点 ![[公式]](https://www.zhihu.com/equation?tex=i) 为前景的概率。



![img](https://pic4.zhimg.com/80/v2-06f4af15265c1a37269d0b9919daa79b_720w.png)



可以看出，该Loss分为3个部分：

1. Anchor Softmax loss：该Loss用于监督学习每个Anchor中是否包含文本。 ![[公式]](https://www.zhihu.com/equation?tex=s_i%5E%2A%3D%5C%7B0%2C1%5C%7D) 表示是否是Groud truth。
2. Anchor y coord regression loss：该Loss用于监督学习每个包含为本的Anchor的Bouding box regression y方向offset，类似于Smooth L1 loss。其中 ![[公式]](https://www.zhihu.com/equation?tex=v_j) 是 ![[公式]](https://www.zhihu.com/equation?tex=s_i) 中判定为有文本的Anchor，或者与Groud truth vertical IoU>0.5。
3. Anchor x coord regression loss：该Loss用于监督学习每个包含文本的Anchor的Bouding box regression x方向offset，与y方向同理。前两个Loss存在的必要性很明确，但这个Loss有何作用作者没有解释（从训练和测试的实际效果看，作用不大）







## 

1. 由于加入LSTM，所以CTPN对水平文字检测效果超级好。
2. 因为Anchor设定的原因，CTPN只能检测横向分布的文字，小幅改进加入水平Anchor即可检测竖直文字。但是由于框架限定，对不规则倾斜文字检测效果非常一般。
3. CTPN加入了双向LSTM学习文字的序列特征，有利于文字检测。但是引入LSTM后，在训练时很容易梯度爆炸，需要小心处理。



[场景文字检测—CTPN原理与实现](https://zhuanlan.zhihu.com/p/34757009)



































