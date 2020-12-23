# -*- coding = utf-8 -*-
# /usr/bin/env python

# 删除链表的节点
# 给定单向链表的头指针和一个要删除的节点的值，定义一个函数删除该节点。返回删除后的链表的头节点。
# 测试示例 head= [4, 5, 1, 9], val = 5

# 删除值为 val 的节点可分为两步：定位节点、修改引用
# 1.定位节点： 遍历链表，直到 head.val == val 时跳出，即可定位目标节点。
# 2.修改引用： 设节点 cur 的前驱节点为 pre ，后继节点为 cur.next ；则执行 pre.next = cur.next ，即可实现删除 cur 节点。

# 算法流程：
# a.特例处理： 当应删除头节点 head 时，直接返回 head.next 即可。
# b.初始化： pre = head , cur = head.next 。
# c.定位节点： 当 cur 为空 或 cur 节点值等于 val 时跳出。
#
#     保存当前节点索引，即 pre = cur 。
#     遍历下一节点，即 cur = cur.next 。
#
# d.删除节点： 若 cur 指向某节点，则执行 pre.next = cur.next 。（若 cur 指向 nullnullnull ，代表链表中不包含值为 val 的节点。
# e.返回值： 返回链表头部节点 head 即可。

# 复杂度分析：
#     时间复杂度O(N)： N为链表长度，删除操作平均需循环N/2次，最差N次。
#     空间复杂度O(1)： cur, pre 占用常数大小额外空间。


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def deleteNode(self, head: ListNode, val:int)->ListNode:
        if head.val == val: return head.next
        pre, cur = head, head.next
        while cur and cur.val != val:
            pre, cur = cur, cur.next
        if cur: pre.next = cur.next
        return head



