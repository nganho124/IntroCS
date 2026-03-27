from typing import Tuple, List, Union


class BST:
    """
    A class that represents a Binary Search Tree (BST).

    Attributes:
    ----------
    root: BST
        The root node of the BST.

    """

    # The root node of the BST
    root = None

    def __init__(self, username: str) -> None:
        """
        Constructor for the BST objects.

        Parameters:
        ----------
        username: str
            The username to be stored in a BST object.
        """
        self.username = username
        self.left = None
        self.right = None

    @staticmethod
    def add(username: str) -> None:
        """
        Creates a root if the BST does not have one yet, otherwise adds a new BST object at the right place in the mastodon_tree.

        Parameters:
        ----------
        username: str
            The username of the added node (vertex).
        """

        if BST.root is None:
            BST.root = BST(username)
        else:
            BST._add_helper(BST.root, username)

    @staticmethod
    def _add_helper(node: 'BST', username: str) -> None:
        """
        Recursive helper function for adding a username to the BST.

        Parameters:
        ----------
        node: BST
            The current node.
        username: str
            The username to add.
        """
        if username < node.username:
            # Go left
            if node.left is None:
                node.left = BST(username)
            else:
                BST._add_helper(node.left, username)

        elif username > node.username:
            # Go right
            if node.right is None:
                node.right = BST(username)
            else:
                BST._add_helper(node.right, username)

    @staticmethod
    def iterative_search(root: 'BST', to_find: str) -> Union['BST', bool]:
        """
        Searches for a node in the BST using an iterative approach.

        Parameters:
        ----------
        root: BST
            The current root node for the search.
        to_find: str
            The username to find in the BST.

        Returns:
        -------
        Union[BST, bool]
            The found BST node or False if not found or root is None
        """
        current = BST.root

        while current is not None:
            if to_find < current.username:
                current = current.left
            elif to_find > current.username:
                current = current.right
            else:
                # Found it
                return current

        # Not found
        return False

    @staticmethod
    def recursive_search(root: 'BST', to_find: str) -> Union['BST', bool]:
        """
        Searches for a node in the BST using a binary search approach.

        Parameters:
        ----------
        root: BST
            The current root node for the search.
        to_find: str
            The username to find in the BST.

        Returns:
        -------
        Union[BST, bool]
            The found BST node or False if not found or root is None.
        """
        if root is None:
            return False

        # Base case: node found
        if to_find == root.username:
            return root

        # Recursive cases
        if to_find < root.username:
            return BST.recursive_search(root.left, to_find)
        else:
            return BST.recursive_search(root.right, to_find)

    @staticmethod
    def preorder() -> List[str]:
        """
        Performs a preorder Depth-First Search (DFS) on the BST.

        Returns:
        -------
        List[str]
            A list of the usernames in preorder.
        """
        result = []
        BST._preorder_helper(BST.root, result)
        return result

    @staticmethod
    def _preorder_helper(node: 'BST', result: List[str]) -> None:
        """
        Helper function for preorder traversal.

        Parameters:
        ----------
        node: BST
            The current node.
        result: List[str]
            The list to accumulate usernames.
        """
        if node is None:
            return

        result.append(node.username)
        BST._preorder_helper(node.left, result)
        BST._preorder_helper(node.right, result)

    @staticmethod
    def inorder() -> List[str]:
        """
        Performs an inorder Depth-First Search (DFS) on the BST.

        Returns:
        -------
        List[str]
            A list of the usernames in inorder.
        """
        result = []
        BST._inorder_helper(BST.root, result)
        return result

    @staticmethod
    def _inorder_helper(node: 'BST', result: List[str]) -> None:
        """
        Helper function for inorder traversal.

        Parameters:
        ----------
        node: BST
            The current node.
        result: List[str]
            The list to accumulate usernames.
        """
        if node is None:
            return

        BST._inorder_helper(node.left, result)
        result.append(node.username)
        BST._inorder_helper(node.right, result)

    @staticmethod
    def postorder() -> List[str]:
        """
        Performs a postorder Depth-First Search (DFS) on the BST.

        Returns:
        -------
        List[str]
            A list of the usernames in postorder.
        """
        result = []
        BST._postorder_helper(BST.root, result)
        return result

    @staticmethod
    def _postorder_helper(node: 'BST', result: List[str]) -> None:
        """
        Helper function for postorder traversal.

        Parameters:
        ----------
        node: BST
            The current node.
        result: List[str]
            The list to accumulate usernames.
        """
        if node is None:
            return

        BST._postorder_helper(node.left, result)
        BST._postorder_helper(node.right, result)
        result.append(node.username)
