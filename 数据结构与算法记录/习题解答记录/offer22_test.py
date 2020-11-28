# -*- coding = utf-8 -*-
# /usr/bin/env python
# 链表中第K个节点
# 输入一个链表，输出该链表中倒数第k个节点。为了符合大多数人的习惯，本题从1开始计数，
# 即链表的尾节点是倒数第1个节点。例如，一个链表有6个节点，从头节点开始，
# 它们的值依次是1、2、3、4、5、6。这个链表的倒数第3个节点是值为4的节点。

# 解题思路：
#  1.先遍历统计链表长度，记为n；
#  2.设置一个指针走(n−k)步，即可找到链表倒数第k个节点。

# 使用双指针则可以不用统计链表长度。
# 算法流程：
#   1.初始化： 前指针former、后指针latter，双指针都指向头节点 head​ 。
#   2.构建双指针距离：前指针former先向前走kkk步（结束后，双指针former和latter间相距 k步）。
#   3.双指针共同移动：循环中，双指针former和latter每轮都向前走一步，直至 former 走过链表尾节点时跳出（跳出后，latter与尾节点距离为 k−1
#                   即latter指向倒数第k个节点）。
#   4.返回值： 返回latter即可。

# 复杂度分析：
#
#     时间复杂度O(N)：N为链表长度；总体看，former走了N步，latter走了(N−k)步。
#     空间复杂度O(1)：双指针former,latter使用常数大小的额外空间。


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def getKthFromEnd(self, head: ListNode, k: int) -> ListNode:
        former, latter = head, head
        for _ in range(k):
            former = former.next
        while former:
            former, latter = former.next, latter.next
        return latter
