from django.test import TestCase, RequestFactory
from .models import NodeTree, NodeTreeNames
import json


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


class ListAllNodesViewTest(TestCase):
    """Test cases for list_all_nodes view"""
    
    def setUp(self):
        """Set up test data"""
        self.factory = RequestFactory()
        
        # Create test nodes
        self.root_node = NodeTree.objects.create(
            lft=1, rgt=6, children_count=2
        )
        self.child_node = NodeTree.objects.create(
            lft=2, rgt=3, children_count=0
        )
        
        # Create names
        NodeTreeNames.objects.create(
            nodeTree=self.root_node, language='en', nodeName='Root'
        )
        NodeTreeNames.objects.create(
            nodeTree=self.child_node, language='en', nodeName='Child'
        )
    
    def test_list_all_nodes_success(self):
        """Test successful listing of all nodes"""
        from .views import list_all_nodes
        
        request = self.factory.get('/api/nodes/')
        response = list_all_nodes(request)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']['nodes']), 2)
    
    def test_list_all_nodes_with_pagination(self):
        """Test pagination functionality"""
        from .views import list_all_nodes
        
        request = self.factory.get('/api/nodes/', {'page_size': '1'})
        response = list_all_nodes(request)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(len(data['data']['nodes']), 1)
        self.assertEqual(data['data']['pagination']['total_pages'], 2)
