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
