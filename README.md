# Challenge Hotiday - API de Estrutura Hierárquica

## 📋 Descrição

Este projeto implementa uma API REST em Django para gerenciar uma estrutura hierárquica de nós usando o modelo **Nested Set**. A API suporta operações CRUD básicas e internacionalização (i18n) para nomes dos nós.

## 🚀 Funcionalidades

- ✅ **Estrutura hierárquica** usando Nested Set Model
- ✅ **API REST** com endpoints para listar, buscar e criar nós
- ✅ **Suporte multilíngue** (inglês e italiano)
- ✅ **Paginação** nas listagens
- ✅ **Busca de filhos** diretos
- ✅ **Testes unitários** completos
- ✅ **Dados iniciais** pré-carregados

## 🛠️ Tecnologias

- **Django 5.2.4** - Framework web
- **SQLite** - Banco de dados
- **Nested Set Model** - Estrutura hierárquica
- **Django REST** - API endpoints

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clone o repositório**
```bash
git clone <repository-url>
cd Challenge-Hotiday/challenge_hotiday
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Carregue os dados iniciais**
```bash
python manage.py load_initial_data
```

7. **Execute o servidor**
```bash
python manage.py runserver
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### 1. Listar Todos os Nós
**GET** `/api/nodes/`

**Parâmetros:**
- `page_num` (opcional): Número da página (padrão: 0)
- `page_size` (opcional): Itens por página (padrão: 5, máximo: 1000)
- `language` (opcional): Código do idioma (padrão: 'en')

**Exemplo:**
```bash
curl "http://localhost:8000/api/nodes/?page_size=3&language=it"
```

**Resposta:**
```json
{
  "status": "success",
  "data": {
    "nodes": [
      {
        "id": 1,
        "name": "Azienda",
        "lft": 1,
        "rgt": 26,
        "children_count": 11,
        "is_leaf": false,
        "depth": 12
      }
    ],
    "pagination": {
      "current_page": 0,
      "total_pages": 4,
      "total_items": 12,
      "has_next": true,
      "has_previous": false
    }
  }
}
```

#### 2. Buscar Nó Específico
**GET** `/api/nodes/{id}/`

**Exemplo:**
```bash
curl "http://localhost:8000/api/nodes/1/"
```

**Resposta:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Company",
    "lft": 1,
    "rgt": 26,
    "children_count": 11,
    "is_leaf": false,
    "depth": 12
  }
}
```

#### 3. Buscar Filhos de um Nó
**GET** `/api/nodes/{id}/children/`

**Parâmetros:**
- `language` (opcional): Código do idioma (padrão: 'en')

**Exemplo:**
```bash
curl "http://localhost:8000/api/nodes/1/children/?language=it"
```

**Resposta:**
```json
{
  "status": "success",
  "data": {
    "parent_id": 1,
    "children": [
      {
        "id": 2,
        "name": "Marketing",
        "lft": 2,
        "rgt": 3,
        "children_count": 0,
        "is_leaf": true,
        "depth": 0
      }
    ]
  }
}
```

#### 4. Criar Novo Nó
**POST** `/api/nodes/`

**Body:**
```json
{
  "parent_id": 1,
  "names": {
    "en": "New Department",
    "it": "Nuovo Dipartimento"
  }
}
```

**Exemplo:**
```bash
curl -X POST "http://localhost:8000/api/nodes/" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_id": 1,
    "names": {
      "en": "New Department",
      "it": "Nuovo Dipartimento"
    }
  }'
```

**Resposta:**
```json
{
  "status": "success",
  "data": {
    "id": 13,
    "names": [
      {
        "language": "en",
        "name": "New Department"
      },
      {
        "language": "it",
        "name": "Nuovo Dipartimento"
      }
    ],
    "parent_id": 1,
    "lft": 24,
    "rgt": 25,
    "children_count": 0,
    "is_leaf": true,
    "depth": 0
  }
}
```

## 🧪 Testes

### Executar Todos os Testes
```bash
python manage.py test nodes.tests -v 2
```

### Executar Testes Específicos
```bash
# Testes de modelo
python manage.py test nodes.tests.NodeTreeModelTest -v 2

# Testes de views
python manage.py test nodes.tests.ListAllNodesViewTest -v 2
python manage.py test nodes.tests.GetNodeViewTest -v 2
python manage.py test nodes.tests.SearchChildrenViewTest -v 2
python manage.py test nodes.tests.CreateNodeViewTest -v 2
```

## 📊 Dados Iniciais

O projeto vem com dados iniciais pré-carregados incluindo:

- **Company/Azienda** (nó raiz)
- **Marketing**
- **Helpdesk/Supporto tecnico**
- **Managers**
- **Customer Account/Assistenza Cliente**
- **Accounting/Amministrazione**
- **Sales/Supporto Vendite**
- **Italy/Italia**
- **Europe/Europa**
- **Developers/Sviluppatori**
- **North America/Nord America**
- **Quality Assurance/Controllo Qualità**

## 🏗️ Estrutura do Projeto

```
challenge_hotiday/
├── challenge_hotiday/          # Configurações do Django
├── nodes/                      # App principal
│   ├── models.py              # Modelos NodeTree e NodeTreeNames
│   ├── views.py               # Views da API
│   ├── urls.py                # URLs da API
│   ├── tests.py               # Testes unitários
│   └── management/            # Comandos personalizados
│       └── commands/
│           └── load_initial_data.py
├── manage.py                  # Script de gerenciamento
├── requirements.txt           # Dependências
└── .gitignore                # Arquivos ignorados pelo Git
```

## 🔧 Comandos Úteis

### Carregar Dados Iniciais
```bash
python manage.py load_initial_data
```

### Criar Superusuário
```bash
python manage.py createsuperuser
```

### Shell do Django
```bash
python manage.py shell
```

## 📝 Notas Técnicas

- **Nested Set Model**: Implementado para eficiência em consultas hierárquicas
- **Internacionalização**: Suporte a múltiplos idiomas com fallback para inglês
- **Paginação**: Implementada para melhor performance em grandes datasets
- **Validação**: Validação de dados de entrada e tratamento de erros
- **Transações**: Uso de transações para garantir consistência dos dados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto foi desenvolvido como parte de um teste técnico.