"""
Advanced Tree Data Structures GUI Application
=============================================
Integrating DSA trees with real-world projects using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import time
from typing import Any, List, Optional, Tuple, Dict, Deque
from collections import deque
import json
from abc import ABC, abstractmethod

# =============================================================================
# TREE DATA STRUCTURES (From previous implementation)
# =============================================================================

class TreeInterface(ABC):
    @abstractmethod
    def insert(self, value: Any) -> bool: pass
    @abstractmethod
    def search(self, value: Any) -> bool: pass
    @abstractmethod
    def delete(self, value: Any) -> bool: pass
    @abstractmethod
    def get_height(self) -> int: pass
    @abstractmethod
    def get_size(self) -> int: pass
    @abstractmethod
    def traverse_inorder(self) -> List[Any]: pass
    @abstractmethod
    def traverse_preorder(self) -> List[Any]: pass
    @abstractmethod
    def traverse_postorder(self) -> List[Any]: pass
    @abstractmethod
    def find_min(self) -> Any: pass
    @abstractmethod
    def find_max(self) -> Any: pass

class BSTNode:
    def __init__(self, value: Any):
        self.value = value
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None
        self.parent: Optional['BSTNode'] = None

class BinarySearchTree(TreeInterface):
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._size = 0
        
    def insert(self, value: Any) -> bool:
        if self.root is None:
            self.root = BSTNode(value)
            self._size += 1
            return True
        return self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: BSTNode, value: Any) -> bool:
        if value == node.value:
            return False
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
                node.left.parent = node
                self._size += 1
                return True
            return self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = BSTNode(value)
                node.right.parent = node
                self._size += 1
                return True
            return self._insert_recursive(node.right, value)
    
    def search(self, value: Any) -> bool:
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: Optional[BSTNode], value: Any) -> bool:
        if node is None: return False
        if value == node.value: return True
        return (self._search_recursive(node.left, value) if value < node.value 
                else self._search_recursive(node.right, value))
    
    def delete(self, value: Any) -> bool:
        node_to_delete = self._find_node(self.root, value)
        if node_to_delete is None: return False
        self._delete_node(node_to_delete)
        self._size -= 1
        return True
    
    def _find_node(self, node: Optional[BSTNode], value: Any) -> Optional[BSTNode]:
        if node is None: return None
        if value == node.value: return node
        return (self._find_node(node.left, value) if value < node.value 
                else self._find_node(node.right, value))
    
    def _delete_node(self, node: BSTNode):
        if node.left is None and node.right is None:
            self._transplant(node, None)
        elif node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        else:
            successor = self._find_min_node(node.right)
            if successor.parent != node:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
    
    def _transplant(self, u: BSTNode, v: Optional[BSTNode]):
        if u.parent is None: self.root = v
        elif u == u.parent.left: u.parent.left = v
        else: u.parent.right = v
        if v: v.parent = u.parent
    
    def _find_min_node(self, node: BSTNode) -> BSTNode:
        while node.left: node = node.left
        return node
    
    def get_height(self) -> int:
        return self._calculate_height(self.root)
    
    def _calculate_height(self, node: Optional[BSTNode]) -> int:
        if node is None: return 0
        return 1 + max(self._calculate_height(node.left), 
                      self._calculate_height(node.right))
    
    def get_size(self) -> int: return self._size
    
    def traverse_inorder(self) -> List[Any]:
        result = []; self._inorder_recursive(self.root, result); return result
    
    def _inorder_recursive(self, node: Optional[BSTNode], result: List[Any]):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def traverse_preorder(self) -> List[Any]:
        result = []; self._preorder_recursive(self.root, result); return result
    
    def _preorder_recursive(self, node: Optional[BSTNode], result: List[Any]):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def traverse_postorder(self) -> List[Any]:
        result = []; self._postorder_recursive(self.root, result); return result
    
    def _postorder_recursive(self, node: Optional[BSTNode], result: List[Any]):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def find_min(self) -> Any:
        if self.root is None: return None
        current = self.root
        while current.left: current = current.left
        return current.value
    
    def find_max(self) -> Any:
        if self.root is None: return None
        current = self.root
        while current.right: current = current.right
        return current.value

class AVLNode:
    def __init__(self, value: Any):
        self.value = value
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height = 1

class AVLTree(TreeInterface):
    def __init__(self):
        self.root: Optional[AVLNode] = None
        self._size = 0
        
    def insert(self, value: Any) -> bool:
        if self.root is None:
            self.root = AVLNode(value)
            self._size += 1
            return True
        self.root, inserted = self._insert_recursive(self.root, value)
        if inserted: self._size += 1
        return inserted
    
    def _insert_recursive(self, node: AVLNode, value: Any) -> Tuple[AVLNode, bool]:
        if value == node.value: return node, False
        if value < node.value:
            if node.left is None:
                node.left = AVLNode(value)
            else:
                node.left, inserted = self._insert_recursive(node.left, value)
                if not inserted: return node, False
        else:
            if node.right is None:
                node.right = AVLNode(value)
            else:
                node.right, inserted = self._insert_recursive(node.right, value)
                if not inserted: return node, False
        self._update_height(node)
        return self._balance_node(node), True
    
    def _update_height(self, node: AVLNode):
        left_h = node.left.height if node.left else 0
        right_h = node.right.height if node.right else 0
        node.height = 1 + max(left_h, right_h)
    
    def _balance_node(self, node: AVLNode) -> AVLNode:
        balance = self._get_balance(node)
        if balance > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node
    
    def _get_balance(self, node: AVLNode) -> int:
        left_h = node.left.height if node.left else 0
        right_h = node.right.height if node.right else 0
        return left_h - right_h
    
    def _rotate_left(self, z: AVLNode) -> AVLNode:
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self._update_height(z)
        self._update_height(y)
        return y
    
    def _rotate_right(self, z: AVLNode) -> AVLNode:
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        self._update_height(z)
        self._update_height(y)
        return y
    
    def search(self, value: Any) -> bool:
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node: Optional[AVLNode], value: Any) -> bool:
        if node is None: return False
        if value == node.value: return True
        return (self._search_recursive(node.left, value) if value < node.value 
                else self._search_recursive(node.right, value))
    
    def delete(self, value: Any) -> bool:
        if self.root is None: return False
        self.root, deleted = self._delete_recursive(self.root, value)
        if deleted: self._size -= 1
        return deleted
    
    def _delete_recursive(self, node: AVLNode, value: Any) -> Tuple[Optional[AVLNode], bool]:
        if value < node.value:
            if node.left is None: return node, False
            node.left, deleted = self._delete_recursive(node.left, value)
            if not deleted: return node, False
        elif value > node.value:
            if node.right is None: return node, False
            node.right, deleted = self._delete_recursive(node.right, value)
            if not deleted: return node, False
        else:
            if node.left is None: return node.right, True
            elif node.right is None: return node.left, True
            temp = self._find_min_node(node.right)
            node.value = temp.value
            node.right, _ = self._delete_recursive(node.right, temp.value)
            deleted = True
        self._update_height(node)
        return self._balance_node(node), True
    
    def _find_min_node(self, node: AVLNode) -> AVLNode:
        while node.left: node = node.left
        return node
    
    def get_height(self) -> int:
        return self.root.height if self.root else 0
    
    def get_size(self) -> int: return self._size
    
    def traverse_inorder(self) -> List[Any]:
        result = []; self._inorder_recursive(self.root, result); return result
    
    def _inorder_recursive(self, node: Optional[AVLNode], result: List[Any]):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def traverse_preorder(self) -> List[Any]:
        result = []; self._preorder_recursive(self.root, result); return result
    
    def _preorder_recursive(self, node: Optional[AVLNode], result: List[Any]):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def traverse_postorder(self) -> List[Any]:
        result = []; self._postorder_recursive(self.root, result); return result
    
    def _postorder_recursive(self, node: Optional[AVLNode], result: List[Any]):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def find_min(self) -> Any:
        if self.root is None: return None
        current = self.root
        while current.left: current = current.left
        return current.value
    
    def find_max(self) -> Any:
        if self.root is None: return None
        current = self.root
        while current.right: current = current.right
        return current.value

# =============================================================================
# PROJECT 1: SMART INVENTORY MANAGEMENT SYSTEM
# =============================================================================

class Product:
    def __init__(self, product_id: int, name: str, price: float, quantity: int, category: str):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
    
    def __lt__(self, other):
        return self.product_id < other.product_id
    
    def __eq__(self, other):
        return self.product_id == other.product_id
    
    def __str__(self):
        return f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price}, Qty: {self.quantity}, Category: {self.category}"

class InventoryManager:
    def __init__(self):
        self.products_bst = BinarySearchTree()  # For quick search by ID
        self.categories_avl = AVLTree()  # For category-based organization
        self.product_counter = 1
    
    def add_product(self, name: str, price: float, quantity: int, category: str) -> bool:
        product = Product(self.product_counter, name, price, quantity, category)
        if self.products_bst.insert(product):
            self.categories_avl.insert((category, product))
            self.product_counter += 1
            return True
        return False
    
    def find_product(self, product_id: int) -> Optional[Product]:
        # Create a dummy product for search
        dummy = Product(product_id, "", 0, 0, "")
        def search_func(node_value):
            return node_value.product_id == product_id
        
        # We need to traverse to find the product
        products = self.products_bst.traverse_inorder()
        for product in products:
            if product.product_id == product_id:
                return product
        return None
    
    def delete_product(self, product_id: int) -> bool:
        product = self.find_product(product_id)
        if product:
            self.products_bst.delete(product)
            self.categories_avl.delete((product.category, product))
            return True
        return False
    
    def get_products_by_category(self, category: str) -> List[Product]:
        products = []
        all_products = self.categories_avl.traverse_inorder()
        for cat, product in all_products:
            if cat == category:
                products.append(product)
        return products
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        low_stock = []
        products = self.products_bst.traverse_inorder()
        for product in products:
            if product.quantity <= threshold:
                low_stock.append(product)
        return low_stock
    
    def update_stock(self, product_id: int, new_quantity: int) -> bool:
        product = self.find_product(product_id)
        if product:
            product.quantity = new_quantity
            return True
        return False

# =============================================================================
# PROJECT 2: AI-BASED RECOMMENDATION SYSTEM
# =============================================================================

class User:
    def __init__(self, user_id: int, name: str, preferences: List[str]):
        self.user_id = user_id
        self.name = name
        self.preferences = preferences
        self.rating_history = []  # List of (item_id, rating)
    
    def __lt__(self, other):
        return self.user_id < other.user_id
    
    def __eq__(self, other):
        return self.user_id == other.user_id
    
    def __str__(self):
        return f"User {self.user_id}: {self.name}"

class ContentItem:
    def __init__(self, item_id: int, title: str, categories: List[str], features: Dict):
        self.item_id = item_id
        self.title = title
        self.categories = categories
        self.features = features  # e.g., {"genre": "action", "duration": 120}
        self.avg_rating = 0.0
        self.rating_count = 0
    
    def __lt__(self, other):
        return self.item_id < other.item_id
    
    def __eq__(self, other):
        return self.item_id == other.item_id
    
    def update_rating(self, new_rating: float):
        total = self.avg_rating * self.rating_count + new_rating
        self.rating_count += 1
        self.avg_rating = total / self.rating_count

class RecommendationEngine:
    def __init__(self):
        self.users_bst = BinarySearchTree()
        self.content_avl = AVLTree()
        self.user_counter = 1
        self.content_counter = 1
    
    def add_user(self, name: str, preferences: List[str]) -> int:
        user = User(self.user_counter, name, preferences)
        self.users_bst.insert(user)
        self.user_counter += 1
        return user.user_id
    
    def add_content(self, title: str, categories: List[str], features: Dict) -> int:
        item = ContentItem(self.content_counter, title, categories, features)
        self.content_avl.insert(item)
        self.content_counter += 1
        return item.item_id
    
    def rate_content(self, user_id: int, item_id: int, rating: float):
        user = self._find_user(user_id)
        item = self._find_content(item_id)
        if user and item:
            user.rating_history.append((item_id, rating))
            item.update_rating(rating)
    
    def get_recommendations(self, user_id: int, limit: int = 5) -> List[ContentItem]:
        user = self._find_user(user_id)
        if not user:
            return []
        
        # Simple collaborative filtering based on user preferences
        all_content = self.content_avl.traverse_inorder()
        recommendations = []
        
        for item in all_content:
            score = self._calculate_match_score(user, item)
            recommendations.append((item, score))
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [item for item, score in recommendations[:limit]]
    
    def _calculate_match_score(self, user: User, item: ContentItem) -> float:
        # Simple scoring based on category overlap and ratings
        category_match = len(set(user.preferences) & set(item.categories))
        rating_score = item.avg_rating / 5.0  # Normalize to 0-1
        return category_match * 0.6 + rating_score * 0.4
    
    def _find_user(self, user_id: int) -> Optional[User]:
        users = self.users_bst.traverse_inorder()
        for user in users:
            if user.user_id == user_id:
                return user
        return None
    
    def _find_content(self, item_id: int) -> Optional[ContentItem]:
        items = self.content_avl.traverse_inorder()
        for item in items:
            if item.item_id == item_id:
                return item
        return None

# =============================================================================
# PROJECT 3: REAL-TIME TASK SCHEDULER
# =============================================================================

class Task:
    def __init__(self, task_id: int, name: str, priority: int, duration: int, deadline: str):
        self.task_id = task_id
        self.name = name
        self.priority = priority  # 1-10, 10 being highest
        self.duration = duration  # in minutes
        self.deadline = deadline  # YYYY-MM-DD
        self.status = "pending"  # pending, in-progress, completed
    
    def __lt__(self, other):
        # Sort by priority first, then deadline
        if self.priority != other.priority:
            return self.priority > other.priority  # Higher priority first
        return self.deadline < other.deadline
    
    def __eq__(self, other):
        return self.task_id == other.task_id
    
    def __str__(self):
        return f"Task {self.task_id}: {self.name} (Priority: {self.priority}, Duration: {self.duration}min, Deadline: {self.deadline})"

class TaskScheduler:
    def __init__(self):
        self.priority_bst = BinarySearchTree()  # For priority-based scheduling
        self.deadline_avl = AVLTree()  # For deadline monitoring
        self.task_counter = 1
    
    def add_task(self, name: str, priority: int, duration: int, deadline: str) -> int:
        task = Task(self.task_counter, name, priority, duration, deadline)
        self.priority_bst.insert(task)
        self.deadline_avl.insert((deadline, task))
        self.task_counter += 1
        return task.task_id
    
    def get_next_task(self) -> Optional[Task]:
        # Get highest priority task
        if self.priority_bst.get_size() == 0:
            return None
        return self.priority_bst.find_max()  # Since we defined higher priority as "greater"
    
    def complete_task(self, task_id: int) -> bool:
        task = self._find_task(task_id)
        if task:
            self.priority_bst.delete(task)
            self.deadline_avl.delete((task.deadline, task))
            return True
        return False
    
    def get_urgent_tasks(self) -> List[Task]:
        urgent = []
        deadline_tasks = self.deadline_avl.traverse_inorder()
        # Simple urgency detection (tasks due soon)
        for deadline, task in deadline_tasks:
            if task.status == "pending":
                urgent.append(task)
        return urgent[:5]  # Return top 5 urgent tasks
    
    def _find_task(self, task_id: int) -> Optional[Task]:
        tasks = self.priority_bst.traverse_inorder()
        for task in tasks:
            if task.task_id == task_id:
                return task
        return None

# =============================================================================
# TKINTER GUI APPLICATION
# =============================================================================

class TreeDSAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Tree DSA Applications")
        self.root.geometry("1200x800")
        
        # Initialize project managers
        self.inventory_manager = InventoryManager()
        self.recommendation_engine = RecommendationEngine()
        self.task_scheduler = TaskScheduler()
        
        self.setup_gui()
    
    def setup_gui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        
        # Project 1: Inventory Management
        inventory_frame = ttk.Frame(notebook)
        self.setup_inventory_tab(inventory_frame)
        
        # Project 2: Recommendation System
        recommendation_frame = ttk.Frame(notebook)
        self.setup_recommendation_tab(recommendation_frame)
        
        # Project 3: Task Scheduler
        task_frame = ttk.Frame(notebook)
        self.setup_task_tab(task_frame)
        
        # Tree Visualization
        tree_frame = ttk.Frame(notebook)
        self.setup_tree_viz_tab(tree_frame)
        
        notebook.add(inventory_frame, text="Inventory Management")
        notebook.add(recommendation_frame, text="AI Recommendation")
        notebook.add(task_frame, text="Task Scheduler")
        notebook.add(tree_frame, text="Tree Visualization")
        notebook.pack(expand=True, fill='both')
    
    def setup_inventory_tab(self, parent):
        # Left side - Input controls
        input_frame = ttk.LabelFrame(parent, text="Add Product", padding=10)
        input_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        ttk.Label(input_frame, text="Product Name:").grid(row=0, column=0, sticky='w')
        self.name_entry = ttk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Price:").grid(row=1, column=0, sticky='w')
        self.price_entry = ttk.Entry(input_frame, width=20)
        self.price_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Quantity:").grid(row=2, column=0, sticky='w')
        self.quantity_entry = ttk.Entry(input_frame, width=20)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Category:").grid(row=3, column=0, sticky='w')
        self.category_entry = ttk.Entry(input_frame, width=20)
        self.category_entry.grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Button(input_frame, text="Add Product", 
                  command=self.add_product).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Search section
        search_frame = ttk.LabelFrame(parent, text="Search Product", padding=10)
        search_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        ttk.Label(search_frame, text="Product ID:").grid(row=0, column=0, sticky='w')
        self.search_id_entry = ttk.Entry(search_frame, width=15)
        self.search_id_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Button(search_frame, text="Search", 
                  command=self.search_product).grid(row=1, column=0, columnspan=2, pady=5)
        
        # Right side - Display
        display_frame = ttk.LabelFrame(parent, text="Inventory", padding=10)
        display_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        self.inventory_text = scrolledtext.ScrolledText(display_frame, width=60, height=20)
        self.inventory_text.pack(expand=True, fill='both')
        
        # Buttons for inventory operations
        button_frame = ttk.Frame(display_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Show All Products", 
                  command=self.show_all_products).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Show Low Stock", 
                  command=self.show_low_stock).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Clear Display", 
                  command=self.clear_inventory_display).pack(side='left', padx=2)
        
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def setup_recommendation_tab(self, parent):
        # Left side - User Management
        user_frame = ttk.LabelFrame(parent, text="User Management", padding=10)
        user_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        ttk.Label(user_frame, text="User Name:").grid(row=0, column=0, sticky='w')
        self.user_name_entry = ttk.Entry(user_frame, width=20)
        self.user_name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(user_frame, text="Preferences (comma-separated):").grid(row=1, column=0, sticky='w')
        self.preferences_entry = ttk.Entry(user_frame, width=20)
        self.preferences_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Button(user_frame, text="Add User", 
                  command=self.add_user).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Content Management
        content_frame = ttk.LabelFrame(parent, text="Content Management", padding=10)
        content_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        ttk.Label(content_frame, text="Content Title:").grid(row=0, column=0, sticky='w')
        self.content_title_entry = ttk.Entry(content_frame, width=20)
        self.content_title_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(content_frame, text="Categories (comma-separated):").grid(row=1, column=0, sticky='w')
        self.content_categories_entry = ttk.Entry(content_frame, width=20)
        self.content_categories_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Button(content_frame, text="Add Content", 
                  command=self.add_content).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Right side - Recommendations
        rec_frame = ttk.LabelFrame(parent, text="Recommendations", padding=10)
        rec_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        ttk.Label(rec_frame, text="User ID:").grid(row=0, column=0, sticky='w')
        self.rec_user_id_entry = ttk.Entry(rec_frame, width=15)
        self.rec_user_id_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Button(rec_frame, text="Get Recommendations", 
                  command=self.get_recommendations).grid(row=1, column=0, columnspan=2, pady=5)
        
        self.recommendation_text = scrolledtext.ScrolledText(rec_frame, width=60, height=15)
        self.recommendation_text.grid(row=2, column=0, columnspan=2, sticky='nsew', pady=5)
        
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
        rec_frame.rowconfigure(2, weight=1)
    
    def setup_task_tab(self, parent):
        # Left side - Task Input
        input_frame = ttk.LabelFrame(parent, text="Add Task", padding=10)
        input_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        ttk.Label(input_frame, text="Task Name:").grid(row=0, column=0, sticky='w')
        self.task_name_entry = ttk.Entry(input_frame, width=20)
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Priority (1-10):").grid(row=1, column=0, sticky='w')
        self.priority_entry = ttk.Entry(input_frame, width=20)
        self.priority_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Duration (min):").grid(row=2, column=0, sticky='w')
        self.duration_entry = ttk.Entry(input_frame, width=20)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Deadline (YYYY-MM-DD):").grid(row=3, column=0, sticky='w')
        self.deadline_entry = ttk.Entry(input_frame, width=20)
        self.deadline_entry.grid(row=3, column=1, padx=5, pady=2)
        
        ttk.Button(input_frame, text="Add Task", 
                  command=self.add_task).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Task Operations
        ops_frame = ttk.LabelFrame(parent, text="Task Operations", padding=10)
        ops_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        ttk.Button(ops_frame, text="Get Next Task", 
                  command=self.get_next_task).pack(fill='x', pady=2)
        ttk.Button(ops_frame, text="Show Urgent Tasks", 
                  command=self.show_urgent_tasks).pack(fill='x', pady=2)
        
        ttk.Label(ops_frame, text="Complete Task ID:").pack(anchor='w')
        complete_frame = ttk.Frame(ops_frame)
        complete_frame.pack(fill='x', pady=2)
        
        self.complete_id_entry = ttk.Entry(complete_frame, width=10)
        self.complete_id_entry.pack(side='left', padx=2)
        ttk.Button(complete_frame, text="Complete", 
                  command=self.complete_task).pack(side='left', padx=2)
        
        # Right side - Task Display
        display_frame = ttk.LabelFrame(parent, text="Tasks", padding=10)
        display_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        self.task_text = scrolledtext.ScrolledText(display_frame, width=60, height=20)
        self.task_text.pack(expand=True, fill='both')
        
        ttk.Button(display_frame, text="Show All Tasks", 
                  command=self.show_all_tasks).pack(pady=5)
        
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def setup_tree_viz_tab(self, parent):
        # Tree visualization and analysis
        viz_frame = ttk.LabelFrame(parent, text="Tree Analysis", padding=10)
        viz_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tree selection
        tree_selection_frame = ttk.Frame(viz_frame)
        tree_selection_frame.pack(fill='x', pady=5)
        
        ttk.Label(tree_selection_frame, text="Select Tree:").pack(side='left')
        self.tree_var = tk.StringVar(value="Inventory BST")
        tree_combo = ttk.Combobox(tree_selection_frame, textvariable=self.tree_var,
                                 values=["Inventory BST", "Inventory AVL", 
                                        "Recommendation BST", "Recommendation AVL",
                                        "Task BST", "Task AVL"])
        tree_combo.pack(side='left', padx=5)
        
        ttk.Button(tree_selection_frame, text="Analyze Tree", 
                  command=self.analyze_tree).pack(side='left', padx=5)
        
        # Analysis results
        self.analysis_text = scrolledtext.ScrolledText(viz_frame, height=15)
        self.analysis_text.pack(fill='both', expand=True, pady=5)
        
        # Performance testing
        perf_frame = ttk.LabelFrame(viz_frame, text="Performance Test", padding=10)
        perf_frame.pack(fill='x', pady=5)
        
        ttk.Button(perf_frame, text="Run Performance Comparison", 
                  command=self.run_performance_test).pack(pady=5)
    
    # Inventory Management Methods
    def add_product(self):
        try:
            name = self.name_entry.get()
            price = float(self.price_entry.get())
            quantity = int(self.quantity_entry.get())
            category = self.category_entry.get()
            
            if self.inventory_manager.add_product(name, price, quantity, category):
                messagebox.showinfo("Success", "Product added successfully!")
                self.clear_inventory_entries()
                self.show_all_products()
            else:
                messagebox.showerror("Error", "Failed to add product!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values!")
    
    def search_product(self):
        try:
            product_id = int(self.search_id_entry.get())
            product = self.inventory_manager.find_product(product_id)
            
            if product:
                self.inventory_text.delete(1.0, tk.END)
                self.inventory_text.insert(tk.END, f"Found Product:\n{product}\n")
            else:
                messagebox.showinfo("Not Found", "Product not found!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid product ID!")
    
    def show_all_products(self):
        products = self.inventory_manager.products_bst.traverse_inorder()
        self.display_products(products, "All Products")
    
    def show_low_stock(self):
        low_stock = self.inventory_manager.get_low_stock_products()
        self.display_products(low_stock, "Low Stock Products (≤10)")
    
    def display_products(self, products, title):
        self.inventory_text.delete(1.0, tk.END)
        self.inventory_text.insert(tk.END, f"{title}:\n")
        self.inventory_text.insert(tk.END, "="*50 + "\n")
        for product in products:
            self.inventory_text.insert(tk.END, f"{product}\n")
        self.inventory_text.insert(tk.END, f"\nTotal: {len(products)} products\n")
    
    def clear_inventory_entries(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
    
    def clear_inventory_display(self):
        self.inventory_text.delete(1.0, tk.END)
    
    # Recommendation System Methods
    def add_user(self):
        name = self.user_name_entry.get()
        preferences = [p.strip() for p in self.preferences_entry.get().split(',')]
        
        if name and preferences:
            user_id = self.recommendation_engine.add_user(name, preferences)
            messagebox.showinfo("Success", f"User added with ID: {user_id}")
            self.user_name_entry.delete(0, tk.END)
            self.preferences_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter name and preferences!")
    
    def add_content(self):
        title = self.content_title_entry.get()
        categories = [c.strip() for c in self.content_categories_entry.get().split(',')]
        
        if title and categories:
            # Add some sample features based on categories
            features = {"genre": categories[0] if categories else "general", "popularity": random.randint(1, 100)}
            item_id = self.recommendation_engine.add_content(title, categories, features)
            messagebox.showinfo("Success", f"Content added with ID: {item_id}")
            
            # Add some sample ratings
            for _ in range(3):
                self.recommendation_engine.rate_content(
                    random.randint(1, self.recommendation_engine.user_counter-1),
                    item_id,
                    random.uniform(3.0, 5.0)
                )
            
            self.content_title_entry.delete(0, tk.END)
            self.content_categories_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter title and categories!")
    
    def get_recommendations(self):
        try:
            user_id = int(self.rec_user_id_entry.get())
            recommendations = self.recommendation_engine.get_recommendations(user_id)
            
            self.recommendation_text.delete(1.0, tk.END)
            if recommendations:
                self.recommendation_text.insert(tk.END, f"Recommendations for User {user_id}:\n")
                self.recommendation_text.insert(tk.END, "="*50 + "\n")
                for i, item in enumerate(recommendations, 1):
                    score = self.recommendation_engine._calculate_match_score(
                        self.recommendation_engine._find_user(user_id), item
                    )
                    self.recommendation_text.insert(tk.END, 
                        f"{i}. {item.title} (Rating: {item.avg_rating:.1f}, Match: {score:.2f})\n")
                    self.recommendation_text.insert(tk.END, f"   Categories: {', '.join(item.categories)}\n\n")
            else:
                self.recommendation_text.insert(tk.END, "No recommendations found or user doesn't exist.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid user ID!")
    
    # Task Scheduler Methods
    def add_task(self):
        try:
            name = self.task_name_entry.get()
            priority = int(self.priority_entry.get())
            duration = int(self.duration_entry.get())
            deadline = self.deadline_entry.get()
            
            if 1 <= priority <= 10 and name and deadline:
                task_id = self.task_scheduler.add_task(name, priority, duration, deadline)
                messagebox.showinfo("Success", f"Task added with ID: {task_id}")
                self.clear_task_entries()
                self.show_all_tasks()
            else:
                messagebox.showerror("Error", "Please enter valid values! Priority must be 1-10.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def get_next_task(self):
        next_task = self.task_scheduler.get_next_task()
        self.task_text.delete(1.0, tk.END)
        if next_task:
            self.task_text.insert(tk.END, "Next Task (Highest Priority):\n")
            self.task_text.insert(tk.END, "="*50 + "\n")
            self.task_text.insert(tk.END, f"{next_task}\n")
        else:
            self.task_text.insert(tk.END, "No tasks available!\n")
    
    def show_urgent_tasks(self):
        urgent_tasks = self.task_scheduler.get_urgent_tasks()
        self.task_text.delete(1.0, tk.END)
        if urgent_tasks:
            self.task_text.insert(tk.END, "Urgent Tasks:\n")
            self.task_text.insert(tk.END, "="*50 + "\n")
            for task in urgent_tasks:
                self.task_text.insert(tk.END, f"{task}\n")
        else:
            self.task_text.insert(tk.END, "No urgent tasks!\n")
    
    def complete_task(self):
        try:
            task_id = int(self.complete_id_entry.get())
            if self.task_scheduler.complete_task(task_id):
                messagebox.showinfo("Success", f"Task {task_id} completed!")
                self.complete_id_entry.delete(0, tk.END)
                self.show_all_tasks()
            else:
                messagebox.showerror("Error", "Task not found!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid task ID!")
    
    def show_all_tasks(self):
        tasks = self.task_scheduler.priority_bst.traverse_inorder()
        self.task_text.delete(1.0, tk.END)
        if tasks:
            self.task_text.insert(tk.END, "All Tasks (Sorted by Priority):\n")
            self.task_text.insert(tk.END, "="*50 + "\n")
            for task in tasks:
                self.task_text.insert(tk.END, f"{task}\n")
        else:
            self.task_text.insert(tk.END, "No tasks available!\n")
    
    def clear_task_entries(self):
        self.task_name_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
    
    # Tree Analysis Methods
    def analyze_tree(self):
        tree_type = self.tree_var.get()
        self.analysis_text.delete(1.0, tk.END)
        
        if tree_type == "Inventory BST":
            tree = self.inventory_manager.products_bst
        elif tree_type == "Inventory AVL":
            tree = self.inventory_manager.categories_avl
        elif tree_type == "Recommendation BST":
            tree = self.recommendation_engine.users_bst
        elif tree_type == "Recommendation AVL":
            tree = self.recommendation_engine.content_avl
        elif tree_type == "Task BST":
            tree = self.task_scheduler.priority_bst
        elif tree_type == "Task AVL":
            tree = self.task_scheduler.deadline_avl
        else:
            return
        
        self.analysis_text.insert(tk.END, f"Analysis of {tree_type}:\n")
        self.analysis_text.insert(tk.END, "="*50 + "\n")
        self.analysis_text.insert(tk.END, f"Size: {tree.get_size()} nodes\n")
        self.analysis_text.insert(tk.END, f"Height: {tree.get_height()}\n")
        self.analysis_text.insert(tk.END, f"Minimum Value: {tree.find_min()}\n")
        self.analysis_text.insert(tk.END, f"Maximum Value: {tree.find_max()}\n")
        
        # Show first few elements
        elements = tree.traverse_inorder()[:5]
        self.analysis_text.insert(tk.END, f"\nFirst 5 elements (inorder):\n")
        for elem in elements:
            self.analysis_text.insert(tk.END, f"  {elem}\n")
    
    def run_performance_test(self):
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "Performance Test Results:\n")
        self.analysis_text.insert(tk.END, "="*50 + "\n")
        
        # Test BST vs AVL insertion performance
        test_sizes = [100, 500, 1000]
        
        for size in test_sizes:
            self.analysis_text.insert(tk.END, f"\nTesting with {size} elements:\n")
            
            # BST Performance
            bst = BinarySearchTree()
            start_time = time.time()
            for i in range(size):
                bst.insert(random.randint(1, size * 10))
            bst_time = time.time() - start_time
            
            # AVL Performance
            avl = AVLTree()
            start_time = time.time()
            for i in range(size):
                avl.insert(random.randint(1, size * 10))
            avl_time = time.time() - start_time
            
            self.analysis_text.insert(tk.END, f"  BST Insertion: {bst_time:.4f}s (Height: {bst.get_height()})\n")
            self.analysis_text.insert(tk.END, f"  AVL Insertion: {avl_time:.4f}s (Height: {avl.get_height()})\n")
            self.analysis_text.insert(tk.END, f"  AVL is {avl_time/bst_time:.2f}x slower but {bst.get_height()/avl.get_height():.2f}x more balanced\n")

def main():
    root = tk.Tk()
    app = TreeDSAGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()