# -*- coding: utf-8 -*-
"""
    implementation of Priority Queue using list
"""

import binarySearchTree import BinarySearchTree

import binarySearchTree import Node as TreeNode


class AvlTree(BinarySearchTree):
    '''An extension t the BinarySearchTree data structure which
    strives to keep itself balanced '''

    def insertion(self, key, value):
        y = None
        x = self.root
        while x is not None and x.key != key:
            y = x
            if key < x.key:
                x = x.left
            else:
                x = x.right

        if x is not None:
            x.value = value
        elif key < y.key:
            y.left = Node(key, value, parent=y)
            self._insertionUpdateBalance(y.left)
            self.size += 1
        else:
            y.right = Node(key, value, parent=y)
            self._insertionUpdateBalance(y.right)
            self.size += 1

    def transplant(self, old, new):
        # only change the relationship with the parent node.
        if old.parent is None:
            self.root = new
        elif old == old.parent.left:
            old.parent.left = new
        else:
            old.parent.right = new
        if new is not None:
            new.parent = old.parent

    def deletion(self, key):
        node = self._search(self.root, key)
        assert node is not None, 'key is not in the tree'

        if node.left is None:
            self.transplant(node, node.right)
            self._deleteUpdateBalance(node)
        elif node.right is None:
            self.transplant(node, node.left)
            self._deleteUpdateBalance(node)
        elif:
            successor = self.minimum(node.right)
            if node != successor.parent:
                tmp = successor.right
                oldBalance = successor.balanceFactor
                self.transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor

                self.transplant(node, successor)
                successor.left = node.left
                successor.left.parent = successor

                successor.balanceFactor = node.balanceFactor
                tmp.balanceFactor = oldBalance + 1
                self._deleteUpdateBalance(tmp)

            else:
                self.transplant(node, successor)
                successor.left = node.left
                successor.left.parent = successor

                successor.balanceFactor = node.balanceFactor + 1
                self._deleteUpdateBalance(successor)

    def _deleteUpdateBalance(self, node):
        while node is not None:
            if node.balanceFactor > 1 or node.balanceFactor < -1:
                self._rebalance(node)
            if node.parent is not None:
                if node == node.parent.left:
                    node.parent.balanceFactor -= 1
                elif node == node.parent.right:
                    node.parent.balanceFactor += 1

                if node.parent.balanceFactor == 0:
                    node = node.parent
                else:
                    node = None

    def _rebalance(self, node):
        # node is the root of the unbalanced subtree.
        if node.balanceFactor < 0:
            if node.balanceFactor > 0:
                self._rotateRight(node.right)
                newRoot = self._rotateLeft(node)
            else:
                newRoot = self._rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.balanceFactor < 0:
                self._rotateLeft(node.left)
                newRoot = self._rotateRight(node)
            else:
                newRoot = self._rotateRight(node)
        return newRoot

    def _insertionUpdateBalance(self, node):
        while node is not None:
            if node.balanceFactor > 1 or node.balanceFactor < -1:
                self._rebalance(node)
                return
            if node.parent is not None:
                if node == node.parent.left:
                    node.parent.balanceFactor += 1
                elif node == node.parent.right:
                    node.parent.balanceFactor -= 1

                if node.parent.balanceFactor != 0:
                    node = node.parent
                else:
                    node = None

    def _rotateLeft(self, node):
        newRoot = node.right
        node.right = newRoot.left
        if node.right is not None:
            node.right.parent = node
        newRoot.parent = node.parent

        if node is self.root:
            self.root = newRoot
        else:
            if node == node.parent.left:
                node.parent.left = newRoot
            else:
                node.parent.right = newRoot
        newRoot.left = node
        node.parent = newRoot

        node.balanceFactor = node.balanceFactor + 1 - \
            min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + \
            max(node.balanceFactor, 0)
        return newRoot

    def _rotateRight(self, node):
        newRoot = node.left
        node.left = newRoot.right
        if node.left is not None:
            node.left.parent = node
        newRoot.parent = node.parent

        if node is self.root:
            self.root = newRoot
        else:
            if node == node.parent.left:
                node.parent.left = newRoot
            else:
                node.parent.right = newRoot

        newRoot.right = node
        node.parent = newRoot
        node.balanceFactor = node.balanceFactor - 1 - \
            max(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + \
            min(node.balanceFactor, 0)


class Node(TreeNode):
    def __init__(self, key, value, left=None, right=None, parent=None):
        TreeNode.__init__(key, value, left, right, parent)
        self.balanceFactor = 0
