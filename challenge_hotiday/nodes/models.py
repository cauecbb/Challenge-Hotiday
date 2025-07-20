from django.db import models

# Create your models here.


class NodeTree(models.Model):

    lft = models.IntegerField(help_text="Right value of the Nested Set  ")
    rgt = models.IntegerField(help_text="Left value of the Nested Set")
    children_count = models.IntegerField(default=0, help_text="Number of direct children")
    
    class Meta:
        db_table = 'nodes'
        verbose_name = 'Node'
        verbose_name_plural = 'Nodes'
    
    def __str__(self):
        return f"Node {self.id} (lft: {self.lft}, rgt: {self.rgt})"
    
    @property
    def is_leaf(self):
        """Check if the node is a leaf (no children)"""
        return self.children_count == 0
    
    @property
    def depth(self):
        """Calculate the depth of the node in the tree"""
        return (self.rgt - self.lft - 1) // 2


class NodeTreeNames(models.Model):
    """
    This model allows each node to have names in different languages,
    supporting internationalization (i18n) for the API.
    """
    nodeTree = models.ForeignKey(NodeTree, on_delete=models.CASCADE, related_name='names')
    language = models.CharField(max_length=10, help_text="Language code ('en', 'it')")
    nodeName = models.CharField(max_length=255, help_text="Name of the node in the specified language")
    
    class Meta:
        db_table = 'node_tree_names'
        verbose_name = 'Node Name'
        verbose_name_plural = 'Node Names'
        unique_together = ['nodeTree', 'language']
        indexes = [
            models.Index(fields=['language']),
            models.Index(fields=['nodeTree', 'language']),
        ]
    
    def __str__(self):
        return f"{self.nodeName} ({self.language})"
    
    @classmethod
    def get_node_name(cls, node_id, language='en'):
        """
        Get the name of a node in the specified language ('en' or 'it')
        Falls back to English if the requested language is not available.
        """
        try:
            # Try to get the name in the requested language
            name_obj = cls.objects.get(nodeTree_id=node_id, language=language)
            return name_obj.nodeName
        except cls.DoesNotExist:
            # Fallback to English
            try:
                name_obj = cls.objects.get(nodeTree_id=node_id, language='en')
                return name_obj.nodeName
            except cls.DoesNotExist:
                return f"Node {node_id}"
