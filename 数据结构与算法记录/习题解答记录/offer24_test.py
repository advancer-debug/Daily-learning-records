# -*- coding = utf-8 -*-
# /usr/bin/env python

# @Time    : 20-11-28 下午3:21
# @File    : offer24_test.py
# @Software: PyCharm
# 反转链表
# 方法一：迭代
# 遍历链表，并在访问各节点时修改 next 引用指向
# 复杂度分析：
#     时间复杂度O(N)：遍历链表使用线性大小时间。
#     空间复杂度O(1)：变量pre和cur使用常数大小额外空间。

# 定义一个函数，输入一个链表的头节点，反转该链表并输出反转后链表的头节点。


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        cur, pre = head, None
        while cur:
            tmp = cur.next  # 暂存后继节点 cur.next
            cur.next = pre  # 修改 next 引用指向
            pre = cur  # pre 暂存 cur
            cur = tmp  # cur 访问下一节点
        return pre

# 或简化


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        cur, pre = head, None
        while cur:
            cur.next, pre, cur = pre, cur, cur.next
        return pre

# 方法2 使用递归法遍历链表，当越过尾节点后终止递归，在回溯时修改各节点的 next 引用指向。
# recur(cur, pre) 递归函数：
#     终止条件：当cur为空，则返回尾节点pre 即反转链表的头节点）；
#     递归后继节点，记录返回值（即反转链表的头节点）为res；
#     修改当前节点cur引用指向前驱节点pre；
#     返回反转链表的头节点res；
# reverseList(head) 函数：
# 调用并返回 recur(head, null)。传入null是因为反转链表后，head节点指向null ；
# 复杂度分析：
#
#     时间复杂度O(N)：遍历链表使用线性大小时间。
#     空间复杂度O(N)：遍历链表的递归深度达到N，系统使用O(N)大小额外空间。


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        def recur(cur, pre):
            if not cur: return pre  # 终止条件
            res = recur(cur.next, cur)  # 递归后继节点
            cur.next = pre  # 修改节点引用指向
            return res  # 返回反转链表的头节点

        return recur(head, None)  # 调用递归并返回
