from django.test import TestCase
from .models import NodeTree, NodeTreeNames


class NodeTreeModelTest(TestCase):
    """Test cases for NodeTree model"""
    
    def setUp(self):
        """Set up test data"""
        self.root_node = NodeTree.objects.create(
            lft=1, rgt=6, children_count=2
        )
        self.child_node = NodeTree.objects.create(
            lft=2, rgt=3, children_count=0
        )
        
        NodeTreeNames.objects.create(
            nodeTree=self.root_node, language='en', nodeName='Root Node'
        )
        NodeTreeNames.objects.create(
            nodeTree=self.child_node, language='en', nodeName='Child Node'
        )
    
    def test_node_properties(self):
        """Test node properties"""
        self.assertFalse(self.root_node.is_leaf)
        self.assertTrue(self.child_node.is_leaf)
        self.assertEqual(self.root_node.depth, 2)
        self.assertEqual(self.child_node.depth, 0)
    
    def test_get_node_name(self):
        """Test getting node name"""
        name = NodeTreeNames.get_node_name(self.root_node.id, 'en')
        self.assertEqual(name, 'Root Node')
        
        # Test fallback 
        name_fallback = NodeTreeNames.get_node_name(self.child_node.id, 'it')
        self.assertEqual(name_fallback, 'Child Node')
        
        # Test non-existent node
        name_nonexistent = NodeTreeNames.get_node_name(999, 'en')
        self.assertEqual(name_nonexistent, 'Node 999')
