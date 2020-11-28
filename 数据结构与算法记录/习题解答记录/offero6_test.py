# -*- coding = utf-8 -*-
# /usr/bin/env python

# @Time    : 20-11-28 下午2:02
# @File    : offero6_test.py
# @Software: PyCharm

# 输入一个链表的头节点，从尾到头反过来返回每个节点的值（用数组返回）。

# 方法一递归法

# 利用递归： 先走至链表末端，回溯时依次将节点值加入列表 ，这样就可以实现链表值的倒序输出。
# python算法流程
# 递推阶段： 每次传入 head.next ，以 head == None（即走过链表尾部节点）为递归终止条件，此时返回空列表 [] 。
# 回溯阶段： 利用 Python 语言特性，递归回溯时每次返回 当前 list + 当前节点值 [head.val] ，
#           即可实现节点的倒序输出。
# 复杂度分析：
#
#     时间复杂度 O(N)： 遍历链表，递归 N 次。
#     空间复杂度 O(N)： 系统递归需要使用 O(N) 的栈空间。

# Definition for singly-linked list.


# 1.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def reverseprint(self, head: ListNode)->List[int]:
        return self.reverseprint(head.next)+[head.val] if head else []


# 2.
class Solution:
    def reverseprint(self, head: ListNode)->List[int]:
        p, rev = head, None
        while p:
            rev, rev.next, p = p, rev, p.next
        result = []
        while rev:
            result.append(rev.val)
            rev = rev.next
        return result

# 辅助栈法
# 解题思路：
#     链表特点： 只能从前至后访问每个节点。
#     题目要求： 倒序输出节点值。
#     这种 先入后出 的需求可以借助 栈 来实现。
# 算法流程：
#     入栈： 遍历链表，将各节点值 push 入栈。（Python​ 使用 append() 方法，​Java​借助 LinkedList 的addLast()方法）。
#     出栈： 将各节点值 pop 出栈，存储于数组并返回。（Python​ 直接返回 stack 的倒序列表，Java ​新建一个数组，通过 popLast() 方法将各元素存入数组，实现倒序输出）。
# 复杂度分析：
#     时间复杂度O(N)：入栈和出栈共使用O(N)时间。
#     空间复杂度O(N)：辅助栈stack和数组res共使用 O(N)的额外空间。


class Solution:
    def reversePrint(self, head: ListNode) -> List[int]:
        stack = []
        while head:
            stack.append(head.val)
            head = head.next
        return stack[::-1]       # stack.reverse()  return stack

