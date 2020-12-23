# -*- coding = utf-8 -*-
# /usr/bin/env python
# 复杂链表的复制

# 请实现 copyRandomList 函数，复制一个复杂链表。在复杂链表中，
# 每个节点除了有一个 next 指针指向下一个节点，还有一个 random 指针指向链表中
#  的任意节点或者 null。

# 给定链表的头节点 head ，复制普通链表很简单，只需遍历链表，每轮建立新节点 + 构建前驱节点 pre 和当前节点 node 的引用指向即可。
# 新增了 random 指针，指向链表中的 任意节点 或者 nullnullnull 。这个 random 指针意味着在复制过程中，除了构建前驱节点和当前节点的引用指向 pre.next ，
# 还要构建前驱节点和其随机节点的引用指向 pre.random
"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        cur = head
        dum = pre = Node(0)
        while cur:
            node = Node(cur.val) # 复制节点 cur
            pre.next = node      # 新链表的 前驱节点 -> 当前节点
            # pre.random = '???' # 新链表的 「 前驱节点 -> 当前节点 」 无法确定
            cur = cur.next       # 遍历下一节点
            pre = node           # 保存当前新节点
        return dum.next

# 方法一 ： hash表
# 利用哈希表的查询特点，考虑构建 原链表节点 和 新链表对应节点 的键值对映射关系，再遍历构建新链表各节点的 next 和 random 引用指向即可。
# 算法流程：
#     1.若头节点 head 为空节点，直接返回null；
#     2.初始化： 哈希表dic， 节点cur指向头节点；
#     3.复制链表：
#         a.建立新节点，并向 dic 添加键值对(原cur节点,新cur节点） ；
#         b.cur 遍历至原链表下一节点；
#     4.构建新链表的引用指向：
#         a.构建新节点的next和random引用指向；
#         b.cur遍历至原链表下一节点；
#     5.返回值：新链表的头节点dic[cur] ；
# 复杂度分析：
#     时间复杂度O(N)： 两轮遍历链表，使用O(N)时间。
#     空间复杂度O(N)： 哈希表dic使用线性大小的额外空间。
class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        if not head: return
        dic = {}
        # 3. 复制各节点，并建立 “原节点 -> 新节点” 的 Map 映射
        cur = head
        while cur:
            dic[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        # 4. 构建新节点的 next 和 random 指向
        while cur:
            dic[cur].next = dic.get(cur.next)
            dic[cur].random = dic.get(cur.random)
            cur = cur.next
        # 5. 返回新链表的头节点
        return dic[head]
# 方法二：考虑构建 原节点 1 -> 新节点 1 -> 原节点 2 -> 新节点 2 -> …… 的拼接链表，
# 如此便可在访问原节点的 random 指向节点的同时找到新对应新节点的 random 指向节点。
# 算法流程：
#     复制各节点，构建拼接链表:
#         设原链表为 node1→node2→⋯，构建的拼接链表如下所示：
#           node1→node1new→node2→node2new→⋯
#     构建新链表各节点的 random 指向：
#         当访问原节点 cur 的随机指向节点 cur.random 时，对应新节点 cur.next 的随机指向节点为 cur.random.next 。
#     拆分原 / 新链表：
#         设置 pre / cur 分别指向原 / 新链表头节点，遍历执行 pre.next = pre.next.next 和 cur.next = cur.next.next 将两链表拆分开。
#     返回新链表的头节点 res 即可。
#
# 复杂度分析：
#
#     时间复杂度O(N)： 三轮遍历链表，使用O(N)时间。
#     空间复杂度O(1)： 节点引用变量使用常数大小的额外空间。
class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        if not head: return
        cur = head
        # 1. 复制各节点，并构建拼接链表
        while cur:
            tmp = Node(cur.val)
            tmp.next = cur.next
            cur.next = tmp
            cur = tmp.next
        # 2. 构建各新节点的 random 指向
        cur = head
        while cur:
            if cur.random:
                cur.next.random = cur.random.next
            cur = cur.next.next
        # 3. 拆分两链表
        cur = res = head.next
        pre = head
        while cur.next:
            pre.next = pre.next.next
            cur.next = cur.next.next
            pre = pre.next
            cur = cur.next
        pre.next = None # 单独处理原链表尾节点
        return res      # 返回新链表头节点





