# -*- coding = utf-8 -*-
# /usr/bin/env python

# 二维数组的查找
# 在一个 n * m 的二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个高效的函数，
# 输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。

# 现有矩阵 matrix 如下：
# [
#   [1,   4,  7, 11, 15],
#   [2,   5,  8, 12, 19],
#   [3,   6,  9, 16, 22],
#   [10, 13, 14, 17, 24],
#   [18, 21, 23, 26, 30]
# ]
# 给定 target = 5，返回 true。
# 给定 target = 20，返回 false。
# 限制：
# 0 <= n <= 1000
# 0 <= m <= 1000

# 方法一：若使用暴力法遍历矩阵 matrix ，则时间复杂度为 O(NM)O(NM)O(NM) 。暴力法未利用矩阵 “从上到下递增、从左到右递增” 的特点，显然不是最优解法。
# 方法二：从矩阵 matrix 左下角元素（索引设为 (i, j) ）开始遍历，并与目标值对比：
#
#     当 matrix[i][j] > target 时，执行 i-- ，即消去第 i 行元素；
#     当 matrix[i][j] < target 时，执行 j++ ，即消去第 j 列元素；
#     当 matrix[i][j] = target 时，返回 truetruetrue ，代表找到目标值。
#       若行索引或列索引越界，则代表矩阵中无目标值，返回 falsefalsefalse
# 每轮 i 或 j 移动后，相当于生成了“消去一行（列）的新矩阵”， 索引(i,j) 指向新矩阵的左下角元素（标志数），因此可重复使用以上性质消去行（列）。
#
# 时间复杂度 O(M+N)：其中，N和 M分别为矩阵行数和列数，此算法最多循环M+N次。
# 空间复杂度 O(1):i,j指针使用常数大小额外空间。


class Solution:
    def findNumberIn2DArray(self, matrix: list[list[int]], target: int) -> bool:
        i, j = len(matrix)-1, 0
        while i >= 0 and j < len(matrix[0]):
            if matrix[i][j] > target:
                i -= 1
            elif matrix[i][j] < target:
                j += 1
            else:
                return True
        return False

