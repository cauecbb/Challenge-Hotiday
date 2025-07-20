from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import F
from .models import NodeTree, NodeTreeNames
import json


@require_http_methods(["GET"])
def list_all_nodes(request):
    """
    List all nodes in the tree (with pagination and language).
    
    parameters:
    - page_num: Page number (default: 0)
    - page_size: Items per page (default: 5, max: 1000)
    - language: Language code for node names (default: 'en')
    """
    try:
        page_num = int(request.GET.get('page_num', 0))
        page_size = min(int(request.GET.get('page_size', 5)), 1000)
        language = request.GET.get('language', 'en')
        
        # Get all nodes in the specified language
        nodes = NodeTree.objects.select_related().prefetch_related('names')
        
        # Prepare data for response
        nodes_data = []
        for node in nodes:
            # Get node name in specified language
            try:
                name_obj = node.names.get(language=language)
                node_name = name_obj.nodeName
            except NodeTreeNames.DoesNotExist:
                # fallback to english
                try:
                    name_obj = node.names.get(language='en')
                    node_name = name_obj.nodeName
                except NodeTreeNames.DoesNotExist:
                    node_name = f"Node {node.id}"
            
            nodes_data.append({
                'id': node.id,
                'name': node_name,
                'lft': node.lft,
                'rgt': node.rgt,
                'children_count': node.children_count,
                'is_leaf': node.is_leaf,
                'depth': node.depth
            })
        
        # pagination
        paginator = Paginator(nodes_data, page_size)
        page_obj = paginator.get_page(page_num)
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'nodes': list(page_obj),
                'pagination': {
                    'current_page': page_obj.number,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'page_size': page_size
                }
            }
        })
        
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid parameter value'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error'
        }, status=500)


@require_http_methods(["GET"])
def get_node(request, node_id):
    """
    Get a specific node by id.
    
    parameters:
    - language: Language code for node names (default: 'en')
    """
    try:
        # Get language parameter
        language = request.GET.get('language', 'en')
        
        # Get the node
        try:
            node = NodeTree.objects.get(id=node_id)
        except NodeTree.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Node with ID {node_id} not found'
            }, status=404)
        
        # Get node name 
        try:
            name_obj = node.names.get(language=language)
            node_name = name_obj.nodeName
        except NodeTreeNames.DoesNotExist:
            # fallback to english
            try:
                name_obj = node.names.get(language='en')
                node_name = name_obj.nodeName
            except NodeTreeNames.DoesNotExist:
                node_name = f"Node {node.id}"
        
        # Prepare response data for single node
        node_data = {
            'id': node.id,
            'name': node_name,
            'lft': node.lft,
            'rgt': node.rgt,
            'children_count': node.children_count,
            'is_leaf': node.is_leaf,
            'depth': node.depth
        }
        
        return JsonResponse({
            'status': 'success',
            'data': node_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error'
        }, status=500)


@require_http_methods(["GET"])
def search_children(request, node_id):
    """
    Search for children of a specific node
    
    parameters:
    - page: Page number (default: 0)
    - page_size: Items per page (default: 5, max: 1000)
    - language: Language code for node names (default: 'en')
    """
    try:
        # Get parameters
        page_num = int(request.GET.get('page_num', 0))
        page_size = min(int(request.GET.get('page_size', 5)), 1000)
        language = request.GET.get('language', 'en')

        # Get the parent node
        try:
            parent_node = NodeTree.objects.get(id=node_id)
        except NodeTree.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Parent node with ID {node_id} not found'
            }, status=404)
        
        # Get direct children nodes using Nested Set Model
        children = NodeTree.objects.filter(
            lft__gt=parent_node.lft,
            rgt__lt=parent_node.rgt
        ).prefetch_related('names')
        
        # Filter to get only direct children (not descendants)
        direct_children = []
        for child in children:
            # Check if this is a direct child by verifying no other node is between parent and child
            is_direct_child = True
            for other_child in children:
                if other_child.id != child.id:
                    if (other_child.lft < child.lft and other_child.rgt > child.rgt):
                        is_direct_child = False
                        break
            if is_direct_child:
                direct_children.append(child)
        
        # Prepare children data
        children_data = []
        for child in direct_children:
            # Get child name in specified language
            try:
                name_obj = child.names.get(language=language)
                child_name = name_obj.nodeName
            except NodeTreeNames.DoesNotExist:
                # fallback to english
                try:
                    name_obj = child.names.get(language='en')
                    child_name = name_obj.nodeName
                except NodeTreeNames.DoesNotExist:
                    child_name = f"Node {child.id}"
            
            children_data.append({
                'id': child.id,
                'name': child_name,
                'lft': child.lft,
                'rgt': child.rgt,
                'children_count': child.children_count,
                'is_leaf': child.is_leaf,
                'depth': child.depth
            })
        
        # pagination
        paginator = Paginator(children_data, page_size)
        page_obj = paginator.get_page(page_num)
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'parent_id': node_id,
                'parent_name': parent_node.names.get(language=language).nodeName if parent_node.names.filter(language=language).exists() else parent_node.names.get(language='en').nodeName if parent_node.names.filter(language='en').exists() else f"Node {parent_node.id}",
                'children': list(page_obj),
                'pagination': {
                    'current_page': page_obj.number,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'page_size': page_size
                }
            }
        })
        
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid parameter value'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def create_node(request):
    """
    Create a new node in the tree.
    """
    # to do - implement node creation logic
    return JsonResponse({
        'status': 'success',
        'message': 'Create node endpoint - to be implemented',
        'data': {}
    })
