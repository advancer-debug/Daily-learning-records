# -*- coding = utf-8 -*-
# /usr/bin/env python

# 找出数组中重复的数字。

# 在一个长度为 n 的数组 nums 里的所有数字都在 0～n-1 的范围内。数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。
# 请找出数组中任意一个重复的数字。
# [2, 3, 1, 0, 2, 5, 3] 输出：2或3

# 方法一：遍历数组
# 由于只需要找出数组中任意一个重复的数字，因此遍历数组，遇到重复的数字即返回。为了判断一个数字是否重复遇到，使用集合存储已经遇到的数字，
# 如果遇到的一个数字已经在集合中，则当前的数字是重复数字。
#
#     初始化集合为空集合，重复的数字 repeat = -1
#     遍历数组中的每个元素：
#         将该元素加入集合中，判断是否添加成功
#             如果添加失败，说明该元素已经在集合中，因此该元素是重复元素，将该元素的值赋给 repeat，并结束遍历
#     返回 repeat
# 哈希表 时间O(n)，空间O（n）


class Solution:
    def findRepeatNumber(self, nums: list[int])->int:
        repeat_dict = dict()
        for num in nums:
            if num not in repeat_dict:
                repeat_dict[num] = 1
            else:
                return num














