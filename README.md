# Challenge Hotiday - Hierarchical Structure API

## Description

Django REST API for managing hierarchical node structures using the Nested Set Model. Supports CRUD operations and internationalization (i18n) for node names.

## Features

- Hierarchical structure using Nested Set Model
- REST API with endpoints for listing, searching and creating nodes
- Multilingual support (English and Italian)
- Pagination for listings
- Direct children search
- Unit tests
- Pre-loaded initial data

## Technologies

- Django 5.2.4
- SQLite
- Nested Set Model
- Django REST

## Installation

### Prerequisites
- Python 3.12+
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/cauecbb/Challenge-Hotiday.git
cd Challenge-Hotiday/challenge_hotiday
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Load initial data**
```bash
python manage.py load_initial_data
```

7. **Start server**
```bash
python manage.py runserver
```

API will be available at: `http://localhost:8000`

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### 1. List All Nodes
**GET** `/api/nodes/`

**Parameters:**
- `page_num` (optional): Page number (default: 0)
- `page_size` (optional): Items per page (default: 5, max: 1000)
- `language` (optional): Language code (default: 'en')

**Example:**
```bash
curl "http://localhost:8000/api/nodes/?page_size=3&language=it"
```

**Response:**
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

#### 2. Get Specific Node
**GET** `/api/nodes/{id}/`

**Example:**
```bash
curl "http://localhost:8000/api/nodes/1/"
```

**Response:**
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

#### 3. Search Node Children
**GET** `/api/nodes/{id}/children/`

**Parameters:**
- `language` (optional): Language code (default: 'en')

**Example:**
```bash
curl "http://localhost:8000/api/nodes/1/children/?language=it"
```

**Response:**
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

#### 4. Create New Node
**POST** `/api/nodes/create/`

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

**Example:**
```bash
curl -X POST "http://localhost:8000/api/nodes/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_id": 1,
    "names": {
      "en": "New Department",
      "it": "Nuovo Dipartimento"
    }
  }'
```

**Response:**
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

## Testing

### Run All Tests
```bash
python manage.py test nodes.tests -v 2
```

### Run Specific Tests
```bash
# Model tests
python manage.py test nodes.tests.NodeTreeModelTest -v 2

# View tests
python manage.py test nodes.tests.ListAllNodesViewTest -v 2
python manage.py test nodes.tests.GetNodeViewTest -v 2
python manage.py test nodes.tests.SearchChildrenViewTest -v 2
python manage.py test nodes.tests.CreateNodeViewTest -v 2
```

## Initial Data

The project comes with pre-loaded data including:

- Company/Azienda (root node)
- Marketing
- Helpdesk/Supporto tecnico
- Managers
- Customer Account/Assistenza Cliente
- Accounting/Amministrazione
- Sales/Supporto Vendite
- Italy/Italia
- Europe/Europa
- Developers/Sviluppatori
- North America/Nord America
- Quality Assurance/Controllo Qualità

## Project Structure

```
challenge_hotiday/
├── challenge_hotiday/          # Django settings
├── nodes/                      # Main app
│   ├── models.py              # NodeTree and NodeTreeNames models
│   ├── views.py               # API views
│   ├── urls.py                # API URLs
│   ├── tests.py               # Unit tests
│   └── management/            # Custom commands
│       └── commands/
│           └── load_initial_data.py
├── manage.py                  # Management script
├── requirements.txt           # Dependencies
└── .gitignore                # Git ignore file
```

## Useful Commands

### Load Initial Data
```bash
python manage.py load_initial_data
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Django Shell
```bash
python manage.py shell
```

## Technical Notes

- **Nested Set Model**: Implemented for efficient hierarchical queries
- **Internationalization**: Multi-language support with English fallback
- **Pagination**: Implemented for better performance
- **Validation**: Input validation and error handling
- **Transactions**: Database transactions for data consistency

## License

This project was developed as part of a technical test.
