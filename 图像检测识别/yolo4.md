### YOLOV4的操作技巧

### 1.数据来源

### 2.YOLOV4简介

![img](https://pic4.zhimg.com/80/v2-3174a6130f65150542aec5b7d00d2d57_720w.jpg)

##### 主要构成及改进

![img](https://pic3.zhimg.com/80/v2-10ef16bb302a869b3c98d1ac84f788ce_720w.jpg)

##### **5个基本组件：**

​	**CBM：**Yolov4网络结构中的最小组件，由Conv+Bn+Mish激活函数三者组成。

​	**CBL：**由Conv+Bn+Leaky_relu激活函数三者组成。

​	**Res unit：**借鉴Resnet网络中的残差结构，让网络可以构建的更深。

​	**CSPX：**借鉴CSPNet网络结构，由卷积层和X个Res unint模块Concate组成。

​	**SPP：**采用1×1，5×5，9×9，13×13的最大池化的方式，进行多尺度融合。

densenet借鉴resnet的跨层连接，但densenet在进行多层卷积进行叠加组成稠密块，稠密块内不同层进行跨层连接，不同稠密块也会进行跨层连接

##### **mish激活函数**

 **Mish**是一种平滑的，非单调的激活函数，可以定义为： 

**f(x) = x**・**tanh(ς(x))**

![img](https://pic3.zhimg.com/80/v2-d7e1e3ede6d4fbfa34f07d0d086be78a_720w.jpg)

##### **Dropblock**

其实和常见网络中的Dropout功能类似，也是缓解过拟合的一种正则化方式。

传统的Dropout很简单，一句话就可以说的清：**随机删除减少神经元的数量，使网络变得更简单。**

![img](https://pic1.zhimg.com/80/v2-fc1787220d4a48d285ade7d55ea90854_720w.jpg)

而Dropblock和Dropout相似，比如下图：

![img](https://pic2.zhimg.com/80/v2-8b9a2710b100dccd1ebc1fe500d5a7a1_720w.jpg)

中间Dropout的方式会随机的删减丢弃一些信息，但**Dropblock的研究者**认为，卷积层对于这种随机丢弃并不敏感，因为卷积层通常是三层连用：**卷积+激活+池化层**，池化层本身就是对相邻单元起作用。而且即使随机丢弃，卷积层仍然可以从相邻的激活单元学习到**相同的信息**。

借鉴**2017年的cutout数据增强**的方式，cutout是将输入图像的部分区域清零，而Dropblock则是将Cutout应用到每一个特征图。而且并不是用固定的归零比率，而是在训练时以一个小的比率开始，随着训练过程**线性的增加这个比率**。

**Dropblock**的研究者与**Cutout**进行对比验证时，发现有几个特点：

**优点一：**Dropblock的效果优于Cutout

**优点二：**Cutout只能作用于输入层，而Dropblock则是将Cutout应用到网络中的每一个特征图上

**优点三：**Dropblock可以定制各种组合，在训练的不同阶段可以修改删减的概率，从空间层面和时间层面，和Cutout相比都有更精细的改进。

###  Neck创新

Yolov4的Neck结构主要采用了**SPP模块**、**FPN+PAN**的方式。

##### （1）SPP模块

![img](https://pic1.zhimg.com/80/v2-60f3d4a7fb071766ac3c3bf70bb5a6f8_720w.jpg)

作者在SPP模块中，使用k={1*1,5*5,9*9,13*13}的最大池化的方式，再将不同尺度的特征图进行Concat操作。

**注意：**这里最大池化采用**padding操作**，移动的步长为1，比如13×13的输入特征图，使用5×5大小的池化核池化，**padding=2**，因此池化后的特征图仍然是13×13大小。

##### （2）FPN+PAN

Yolov4中Neck这部分除了使用FPN外，还在此基础上使用了PAN结构：

![img](https://pic3.zhimg.com/80/v2-5251e9c0784871a37c693d53f7d57f92_720w.jpg)

CSPDarknet53中讲到，每个CSP模块前面的卷积核都是**3\*3大小**，**步长为2**，相当于下采样操作。

因此可以看到三个紫色箭头处的特征图是**76\*76、38\*38、19\*19。**

以及最后Prediction中用于预测的三个特征图：**①76\*76\*255，②38\*38\*255，③19\*19\*255。**

我们也看下**Neck**部分的立体图像，看下两部分是如何通过**FPN+PAN结构**进行融合的。

![img](https://pic1.zhimg.com/80/v2-a204a672779d1c2bc26777437771cda4_720w.jpg)

和Yolov3的FPN层不同，Yolov4在FPN层的后面还添加了一个**自底向上的特征金字塔。**

其中包含两个**PAN结构。**

这样结合操作，FPN层自顶向下传达**强语义特征**，而特征金字塔则自底向上传达**强定位特征**，两两联手，从不同的主干层对不同的检测层进行参数聚合,这样的操作确实很皮。

**FPN+PAN**借鉴的是18年CVPR的**PANet**，当时主要应用于**图像分割领域**，但Alexey将其拆分应用到Yolov4中，进一步提高特征提取的能力。

**注意一：**

Yolov3的FPN层输出的三个大小不一的特征图①②③直接进行预测

但Yolov4的FPN层，只使用最后的一个76*76特征图①，而经过两次PAN结构，输出预测的特征图②和③。

**注意点二：**

原本的PANet网络的**PAN结构**中，两个特征图结合是采用**shortcut**操作，而Yolov4中则采用**concat（route）**操作，特征图融合后的尺寸发生了变化。

![img](https://pic2.zhimg.com/80/v2-c2f9cb3d71bc3011f6f18adc00db3319_720w.jpg)

### Prediction创新

##### （1）CIOU_loss

目标检测任务的损失函数一般由**Classificition Loss（分类损失函数）**和**Bounding Box Regeression Loss（回归损失函数）**两部分构成。

**a.IOU_Loss**

![img](https://pic3.zhimg.com/80/v2-c812620791de642ccb7edcde9e1bd742_720w.jpg)

可以看到IOU的loss其实很简单，主要是**交集/并集**，但其实也存在两个问题。

![img](https://pic4.zhimg.com/80/v2-e3d9a882dec6bb5847be80899bb98ea3_720w.jpg)



**问题1：**即状态1的情况，当预测框和目标框不相交时，IOU=0，无法反应两个框距离的远近，此时损失函数不可导，IOU_Loss无法优化两个框不相交的情况。

**问题2：**即状态2和状态3的情况，当两个预测框大小相同，两个IOU也相同，IOU_Loss无法区分两者相交情况的不同。

**b.GIOU_Loss**

![img](https://pic4.zhimg.com/80/v2-443123f1aa540f7dfdc84b233edcdc67_720w.jpg)

可以看到右图GIOU_Loss中，增加了相交尺度的衡量方式，缓解了单纯IOU_Loss时的尴尬。

![img](https://pic3.zhimg.com/80/v2-49024c2ded9faafe7639c5207e575ed6_720w.jpg)

**问题**：状态1、2、3都是预测框在目标框内部且预测框大小一致的情况，这时预测框和目标框的差集都是相同的，因此这三种状态的**GIOU值**也都是相同的，这时GIOU退化成了IOU，无法区分相对位置关系。

**c.DIOU_Loss**

好的目标框回归函数应该考虑三个重要几何因素：**重叠面积、中心点距离，长宽比。**

针对IOU和GIOU存在的问题，作者从两个方面进行考虑

**一：如何最小化预测框和目标框之间的归一化距离？**

**二：如何在预测框和目标框重叠时，回归的更准确？**

针对第一个问题，提出了DIOU_Loss（Distance_IOU_Loss）

![img](https://pic1.zhimg.com/80/v2-029f094658e87f441bf30c80cb8d07d0_720w.jpg)

DIOU_Loss考虑了**重叠面积**和**中心点距离**，当目标框包裹预测框的时候，直接度量2个框的距离，因此DIOU_Loss收敛的更快。

**d.CIOU_Loss**

CIOU_Loss和DIOU_Loss前面的公式都是一样的，不过在此基础上还增加了一个影响因子，将预测框和目标框的长宽比都考虑了进去。

![img](https://pic2.zhimg.com/80/v2-a24dd2e0d0acef20f6ead6a13b5c33d1_720w.jpg)

其中v是衡量长宽比一致性的参数，我们也可以定义为：

![img](https://pic2.zhimg.com/80/v2-5abd8f82d7e30bdf21d2fd5851cb53a1_720w.jpg)

 这样CIOU_Loss就将目标框回归函数应该考虑三个重要几何因素：重叠面积、中心点距离，长宽比全都考虑进去了。

再来综合的看下各个Loss函数的不同点：

**IOU_Loss：**主要考虑检测框和目标框重叠面积。

**GIOU_Loss：**在IOU的基础上，解决边界框不重合时的问题。

**DIOU_Loss：**在IOU和GIOU的基础上，考虑边界框中心点距离的信息。

**CIOU_Loss：**在DIOU的基础上，考虑边界框宽高比的尺度信息。

Yolov4中采用了**CIOU_Loss**的回归方式，使得预测框回归的**速度和精度**更高一些。CIOU_Loss和DIOU_Loss前面的公式都是一样的，不过在此基础上还增加了一个影响因子，将预测框和目标框的长宽比都考虑了进去。

![img](https://pic2.zhimg.com/80/v2-a24dd2e0d0acef20f6ead6a13b5c33d1_720w.jpg)

其中v是衡量长宽比一致性的参数，我们也可以定义为：

![img](https://pic2.zhimg.com/80/v2-5abd8f82d7e30bdf21d2fd5851cb53a1_720w.jpg)

 这样CIOU_Loss就将目标框回归函数应该考虑三个重要几何因素：**重叠面积、中心点距离，长宽比**全都考虑进去了。

再来综合的看下各个Loss函数的不同点：

**IOU_Loss：**主要考虑检测框和目标框重叠面积。

**GIOU_Loss：**在IOU的基础上，解决边界框不重合时的问题。

**DIOU_Loss：**在IOU和GIOU的基础上，考虑边界框中心点距离的信息。

**CIOU_Loss：**在DIOU的基础上，考虑边界框宽高比的尺度信息。

Yolov4中采用了**CIOU_Loss**的回归方式，使得预测框回归的**速度和精度**更高一些。

##### （2）DIOU_nms

![img](https://pic3.zhimg.com/80/v2-ddb336d26adb2a2e37415b6266c88ec6_720w.jpg)

在上图重叠的摩托车检测中，中间的摩托车因为考虑边界框中心点的位置信息，也可以回归出来。

因此在重叠目标的检测中，**DIOU_nms**的效果优于**传统的nms**。

**注意：有读者会有疑问，这里为什么不用CIOU_nms，而用DIOU_nms?**

**答：**因为前面讲到的CIOU_loss，是在DIOU_loss的基础上，添加的影响因子，包含groundtruth标注框的信息，在训练时用于回归。

但在测试过程中，并没有groundtruth的信息，不用考虑影响因子，因此直接用DIOU_nms即可。

**总体来说，**YOLOv4的论文称的上良心之作，将近几年关于深度学习领域最新研究的tricks移植到Yolov4中做验证测试，将Yolov3的精度提高了不少。

虽然没有全新的创新，但很多改进之处都值得借鉴，借用Yolov4作者的总结。

Yolov4 主要带来了 3 点新贡献：

（1）提出了一种高效而强大的目标检测模型，使用 1080Ti 或 2080Ti 就能训练出超快、准确的目标检测器。

（2）在检测器训练过程中，验证了最先进的一些研究成果对目标检测器的影响。

（3）改进了 SOTA 方法，使其更有效、更适合单 GPU 训练。







concat：张量拼接，扩充两个张量的维度，与cfg文件中的route功能一样26\*26\*256和26\*26*512得到26\*26\*768

add:张量相加，不会扩充维度，与cfg文件中的shortcut功能一样104\*104*128和104\*104\*128相加，结果还是104\*104\*128

shortcut的使用，借鉴resnet的跨层连接，进行信息传递，缓解深层网络梯度消失问题

[参考链接：基于YOLOV4的人脸口罩佩戴检测](https://zhuanlan.zhihu.com/p/148673750)

[深入浅出Yolo系列之Yolov3&Yolov4&Yolov5核心基础知识完整讲解](https://zhuanlan.zhihu.com/p/143747206)

[Dropblock](https://arxiv.org/pdf/1810.12890.pdf)

[图像分割领域PANet](https://arxiv.org/abs/1803.01534)

[Yolov4可视化网络结构图](https://blog.csdn.net/nan355655600/article/details/106246422)

[python代码](https://github.com/Tianxiaomo/pytorch-Yolov4)



## 