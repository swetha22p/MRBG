class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invertTree(root):
    if not root:
        return None
    # Recursive inversion of left and right subtrees
    left = invertTree(root.left)
    right = invertTree(root.right)
    root.left, root.right = right, left  # Swap the left and right children
    return root

def listToTreeNode(lst):
    """Helper function to convert a list into a binary tree"""
    if not lst:
        return None
    nodes = [TreeNode(val) if val is not None else None for val in lst]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids: node.left = kids.pop()
            if kids: node.right = kids.pop()
    return root

def treeNodeToList(root):
    """Helper function to convert a binary tree into a list"""
    if not root:
        return []
    queue = [root]
    result = []
    while queue:
        node = queue.pop(0)
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    # Trim trailing `None` values
    while result and result[-1] is None:
        result.pop()
    return result

# Input tree as a list
root = listToTreeNode([4, 2, 7, 1, 3, 6, 9])
print(root,'kkkk')
# Invert the binary tree
inverted_root = invertTree(root)

# Convert the inverted binary tree back to a list and print it
print(treeNodeToList(inverted_root))
