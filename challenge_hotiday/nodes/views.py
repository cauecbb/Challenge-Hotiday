from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import F
from .models import NodeTree, NodeTreeNames
from typing import Dict, Any, List
import json


@require_http_methods(["GET"])
def list_all_nodes(request: HttpRequest) -> JsonResponse:
    """
    List all nodes in the tree (with pagination and language).
    
    parameters:
    - page_num: Page number (default: 0)
    - page_size: Items per page (default: 5, max: 1000)
    - language: Language code for node names (default: 'en')
    """
    try:
        page_num: int = int(request.GET.get('page_num', 0))
        page_size: int = min(int(request.GET.get('page_size', 5)), 1000)
        language: str = request.GET.get('language', 'en')
        
        # Get all nodes in the specified language
        nodes = NodeTree.objects.select_related().prefetch_related('names')
        
        # Prepare data for response
        nodes_data: List[Dict[str, Any]] = []
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
def get_node(request: HttpRequest, node_id: int) -> JsonResponse:
    """
    Get a specific node by id.
    
    parameters:
    - language: Language code for node names (default: 'en')
    """
    try:
        # Get language parameter
        language: str = request.GET.get('language', 'en')
        
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
def search_children(request: HttpRequest, node_id: int) -> JsonResponse:
    """
    Search for children of a specific node
    
    parameters:
    - page: Page number (default: 0)
    - page_size: Items per page (default: 5, max: 1000)
    - language: Language code for node names (default: 'en')
    """
    try:
        # Get parameters
        page_num: int = int(request.GET.get('page_num', 0))
        page_size: int = min(int(request.GET.get('page_size', 5)), 1000)
        language: str = request.GET.get('language', 'en')

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
        direct_children: List[NodeTree] = []
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
        children_data: List[Dict[str, Any]] = []
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
def create_node(request: HttpRequest) -> JsonResponse:
    """
    Create a new node in the tree.
    
    Request body:
    {
        "parent_id": 1,  // Optional: ID of parent node (null for root)
        "names": {
            "en": "Node Name in English",
            "it": "Nome del Nodo in Italiano"
        }
    }
    """
    try:
        # Parse JSON request body
        try:
            data: Dict[str, Any] = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format'
            }, status=400)
        
        # Validate required fields
        if 'names' not in data:
            return JsonResponse({
                'status': 'error',
                'message': 'Names field is required'
            }, status=400)
        
        if not isinstance(data['names'], dict) or not data['names']:
            return JsonResponse({
                'status': 'error',
                'message': 'Names must be a non-empty object'
            }, status=400)
        
        # Validate at least one language is provided
        if not any(data['names'].values()):
            return JsonResponse({
                'status': 'error',
                'message': 'At least one name must be provided'
            }, status=400)
        
        parent_id: Optional[int] = data.get('parent_id')
        
        # Handle root node creation
        if parent_id is None:
            # Create root node
            new_node = NodeTree.objects.create(
                lft=1,
                rgt=2,
                children_count=0
            )
        else:
            # Create child node
            try:
                parent_node = NodeTree.objects.get(id=parent_id)
            except NodeTree.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Parent node with ID {parent_id} not found'
                }, status=404)
            
            # Update parent's children count
            parent_node.children_count += 1
            parent_node.save()
            
            # Create new node with Nested Set Model logic
            new_node = NodeTree.objects.create(
                lft=parent_node.rgt,
                rgt=parent_node.rgt + 1,
                children_count=0
            )
            
            # Update all nodes that need to be shifted
            NodeTree.objects.filter(rgt__gte=parent_node.rgt).update(rgt=F('rgt') + 2)
            NodeTree.objects.filter(lft__gt=parent_node.rgt).update(lft=F('lft') + 2)
            
            # Update the new node's lft and rgt values
            new_node.lft = parent_node.rgt
            new_node.rgt = parent_node.rgt + 1
            new_node.save()
        
        # Create names for the new node
        created_names: List[Dict[str, str]] = []
        for language, name in data['names'].items():
            if name:  # Only create if name is not empty
                try:
                    name_obj = NodeTreeNames.objects.create(
                        nodeTree=new_node,
                        language=language,
                        nodeName=name
                    )
                    created_names.append({
                        'language': language,
                        'name': name
                    })
                except Exception as e:
                    # If there's an error creating names, delete the node
                    new_node.delete()
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Error creating name for language {language}'
                    }, status=400)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Node created successfully',
            'data': {
                'node_id': new_node.id,
                'lft': new_node.lft,
                'rgt': new_node.rgt,
                'children_count': new_node.children_count,
                'is_leaf': new_node.is_leaf,
                'depth': new_node.depth,
                'names': created_names
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error'
        }, status=500)
