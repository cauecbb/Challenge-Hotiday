from django.core.management.base import BaseCommand
from nodes.models import NodeTree, NodeTreeNames


class Command(BaseCommand):
    help = 'Load initial test data for the node tree'

    def handle(self, *args, **options):
        self.stdout.write('Loading initial test data...')
        
        # Clear existing data
        NodeTreeNames.objects.all().delete()
        NodeTree.objects.all().delete()
        
        # Create hierarchical structure based on the test data
        # Root - Company/Azienda
        company = NodeTree.objects.create(
            lft=1, rgt=26, children_count=11
        )
        NodeTreeNames.objects.create(
            nodeTree=company, language='en', nodeName='Company'
        )
        NodeTreeNames.objects.create(
            nodeTree=company, language='it', nodeName='Azienda'
        )
        
        # Marketing
        marketing = NodeTree.objects.create(
            lft=2, rgt=3, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=marketing, language='en', nodeName='Marketing'
        )
        NodeTreeNames.objects.create(
            nodeTree=marketing, language='it', nodeName='Marketing'
        )
        
        # Helpdesk/Supporto tecnico
        helpdesk = NodeTree.objects.create(
            lft=4, rgt=5, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=helpdesk, language='en', nodeName='Helpdesk'
        )
        NodeTreeNames.objects.create(
            nodeTree=helpdesk, language='it', nodeName='Supporto tecnico'
        )
        
        # Managers
        managers = NodeTree.objects.create(
            lft=6, rgt=7, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=managers, language='en', nodeName='Managers'
        )
        NodeTreeNames.objects.create(
            nodeTree=managers, language='it', nodeName='Managers'
        )
        
        # Customer Account/Assistenza Cliente
        customer_account = NodeTree.objects.create(
            lft=8, rgt=9, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=customer_account, language='en', nodeName='Customer Account'
        )
        NodeTreeNames.objects.create(
            nodeTree=customer_account, language='it', nodeName='Assistenza Cliente'
        )
        
        # Accounting/Amministrazione
        accounting = NodeTree.objects.create(
            lft=10, rgt=11, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=accounting, language='en', nodeName='Accounting'
        )
        NodeTreeNames.objects.create(
            nodeTree=accounting, language='it', nodeName='Amministrazione'
        )
        
        # Sales/Supporto Vendite
        sales = NodeTree.objects.create(
            lft=12, rgt=13, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=sales, language='en', nodeName='Sales'
        )
        NodeTreeNames.objects.create(
            nodeTree=sales, language='it', nodeName='Supporto Vendite'
        )
        
        # Italy/Italia
        italy = NodeTree.objects.create(
            lft=14, rgt=15, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=italy, language='en', nodeName='Italy'
        )
        NodeTreeNames.objects.create(
            nodeTree=italy, language='it', nodeName='Italia'
        )
        
        # Europe/Europa
        europe = NodeTree.objects.create(
            lft=16, rgt=17, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=europe, language='en', nodeName='Europe'
        )
        NodeTreeNames.objects.create(
            nodeTree=europe, language='it', nodeName='Europa'
        )
        
        # Developers/Sviluppatori
        developers = NodeTree.objects.create(
            lft=18, rgt=19, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=developers, language='en', nodeName='Developers'
        )
        NodeTreeNames.objects.create(
            nodeTree=developers, language='it', nodeName='Sviluppatori'
        )
        
        # North America/Nord America
        north_america = NodeTree.objects.create(
            lft=20, rgt=21, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=north_america, language='en', nodeName='North America'
        )
        NodeTreeNames.objects.create(
            nodeTree=north_america, language='it', nodeName='Nord America'
        )
        
        # Quality Assurance/Controllo Qualità
        qa = NodeTree.objects.create(
            lft=22, rgt=23, children_count=0
        )
        NodeTreeNames.objects.create(
            nodeTree=qa, language='en', nodeName='Quality Assurance'
        )
        NodeTreeNames.objects.create(
            nodeTree=qa, language='it', nodeName='Controllo Qualità'
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded initial test data!')
        )
        self.stdout.write(f'Created {NodeTree.objects.count()} nodes')
        self.stdout.write(f'Created {NodeTreeNames.objects.count()} node names')
        
        # Show the structure
        self.stdout.write('\nHierarchical structure created:')
        self.stdout.write('Company/Azienda (Root)')
        self.stdout.write('├── Marketing')
        self.stdout.write('├── Helpdesk/Supporto tecnico')
        self.stdout.write('├── Managers')
        self.stdout.write('├── Customer Account/Assistenza Cliente')
        self.stdout.write('├── Accounting/Amministrazione')
        self.stdout.write('├── Sales/Supporto Vendite')
        self.stdout.write('├── Italy/Italia')
        self.stdout.write('├── Europe/Europa')
        self.stdout.write('├── Developers/Sviluppatori')
        self.stdout.write('├── North America/Nord America')
        self.stdout.write('└── Quality Assurance/Controllo Qualità') 