from django.test import TestCase, RequestFactory
from .models import NodeTree, NodeTreeNames
import json


class NodeTreeModelTest(TestCase):
    """Test cases for NodeTree model"""
    
    def setUp(self):
        # Set up test data
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
        # Test node properties
        self.assertFalse(self.root_node.is_leaf)
        self.assertTrue(self.child_node.is_leaf)
        self.assertEqual(self.root_node.depth, 2)
        self.assertEqual(self.child_node.depth, 0)
    
    def test_get_node_name(self):
        # Test getting node name
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
        # Set up test data
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
        # Test successful listing of all nodes
        from .views import list_all_nodes
        
        request = self.factory.get('/api/nodes/')
        response = list_all_nodes(request)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']['nodes']), 2)
    
    def test_list_all_nodes_with_pagination(self):
        # Test pagination functionality
        from .views import list_all_nodes
        
        request = self.factory.get('/api/nodes/', {'page_size': '1'})
        response = list_all_nodes(request)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(len(data['data']['nodes']), 1)
        self.assertEqual(data['data']['pagination']['total_pages'], 2)


class GetNodeViewTest(TestCase):
    """Test cases for get_node view"""

    def setUp(self):
        #  Set up test data
        self.factory = RequestFactory()
        

        self.node = NodeTree.objects.create(
            lft=1, rgt=2, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=self.node, language='en', nodeName='Test Node'
        )
    
    def test_get_node_success(self):
        # Test successful node retrieval
        from .views import get_node
        
        request = self.factory.get(f'/api/nodes/{self.node.id}/')
        response = get_node(request, self.node.id)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], self.node.id)
        self.assertEqual(data['data']['name'], 'Test Node')
    
    def test_get_node_not_found(self):
        # Test node not found
        from .views import get_node
        
        request = self.factory.get('/api/nodes/999/')
        response = get_node(request, 999)
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')


class SearchChildrenViewTest(TestCase):
    """Test cases for search_children view"""
    
    def setUp(self):
        # Set up test data
        self.factory = RequestFactory()
        
        # Create hierarchical structure
        self.parent = NodeTree.objects.create(
            lft=1, rgt=6, children_count=2
        )
        self.child1 = NodeTree.objects.create(
            lft=2, rgt=3, children_count=0
        )
        self.child2 = NodeTree.objects.create(
            lft=4, rgt=5, children_count=0
        )
        
        # Create names
        NodeTreeNames.objects.create(
            nodeTree=self.parent, language='en', nodeName='Parent'
        )
        NodeTreeNames.objects.create(
            nodeTree=self.child1, language='en', nodeName='Child 1'
        )
        NodeTreeNames.objects.create(
            nodeTree=self.child2, language='en', nodeName='Child 2'
        )
    
    def test_search_children_success(self):
        # Test successful children search
        from .views import search_children
        
        request = self.factory.get(f'/api/nodes/{self.parent.id}/children/')
        response = search_children(request, self.parent.id)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']['children']), 2)
    
    def test_search_children_no_children(self):
        # Test node with no children
        from .views import search_children
        
        request = self.factory.get(f'/api/nodes/{self.child1.id}/children/')
        response = search_children(request, self.child1.id)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(len(data['data']['children']), 0)
