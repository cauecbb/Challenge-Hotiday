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
        page_num = int(request.GET.get('page', 0))
        page_size = min(int(request.GET.get('page_size', 5)), 1000)
        language = request.GET.get('language', 'en')
        
        # if page < 1:
        #     return JsonResponse({
        #         'status': 'error',
        #         'message': 'Page number must be greater than 0'
        #     }, status=400)
        
        # if page_size < 1:
        #     return JsonResponse({
        #         'status': 'error',
        #         'message': 'Page size must be greater than 0'
        #     }, status=400)
        
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
    """
    # to do - implement single node retrieval
    return JsonResponse({
        'status': 'success',
        'message': f'Get node {node_id} endpoint - to be implemented',
        'data': {'node_id': node_id}
    })


@require_http_methods(["GET"])
def search_children(request, node_id):
    """
    Search for children of a specific node.
    """
    # to do - implement children search logic
    return JsonResponse({
        'status': 'success',
        'message': f'Search children of node {node_id} endpoint - to be implemented',
        'data': {'parent_id': node_id, 'children': []}
    })


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
