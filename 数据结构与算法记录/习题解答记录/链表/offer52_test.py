# -*- coding = utf-8 -*-
# /usr/bin/env python

# 两个链表的第一个公共节点
# 输入两个链表，找出它们的第一个公共节点。

# 思路：我们使用两个指针 node1，node2 分别指向两个链表 headA，headB 的头结点，然后同时分别逐结点遍历，
# 当 node1 到达链表 headA 的末尾时，重新定位到链表 headB 的头结点；当 node2 到达链表 headB 的末尾时，
# 重新定位到链表 headA 的头结点。当它们相遇时，所指向的结点就是第一个公共结点。

# 复杂度分析
# - 时间复杂度：O(M+N)。
# - 空间复杂度：O(1)。


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        node1, node2 = headA, headB

        while node1 != node2:
            node1 = node1.next if node1 else headB
            node2 = node2.next if node2 else headA

        return node1
