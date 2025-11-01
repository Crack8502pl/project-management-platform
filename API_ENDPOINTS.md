# API Endpoints Reference

Complete reference of all API endpoints available in the Project Management Platform.

## Base URL
```
http://localhost:8000
```

## Authentication Endpoints

### JWT Token Management
```
POST   /api/auth/token/              # Obtain access and refresh tokens
POST   /api/auth/token/refresh/      # Refresh access token
POST   /api/auth/token/verify/       # Verify token validity
```

### Users & Roles
```
GET    /api/auth/users/              # List all users
POST   /api/auth/users/              # Create new user (public)
GET    /api/auth/users/{id}/         # Get user details
PUT    /api/auth/users/{id}/         # Update user
PATCH  /api/auth/users/{id}/         # Partial update user
DELETE /api/auth/users/{id}/         # Delete user
GET    /api/auth/users/me/           # Get current user profile
PUT    /api/auth/users/me/           # Update current user profile
PATCH  /api/auth/users/me/           # Partial update current user
POST   /api/auth/users/change_password/  # Change password

GET    /api/auth/roles/              # List all roles
GET    /api/auth/roles/{id}/         # Get role details
```

## Projects Endpoints

### Projects
```
GET    /api/projects/                # List all projects
POST   /api/projects/                # Create new project
GET    /api/projects/{id}/           # Get project details
PUT    /api/projects/{id}/           # Update project
PATCH  /api/projects/{id}/           # Partial update project
DELETE /api/projects/{id}/           # Delete project

Query Parameters:
  ?status=planning|in_progress|on_hold|completed|cancelled
  ?priority=low|medium|high|critical
  ?manager={user_id}
  ?search={query}
  ?ordering=name|-name,created_at,-created_at
```

### Contracts
```
GET    /api/projects/contracts/              # List all contracts
POST   /api/projects/contracts/              # Create new contract
GET    /api/projects/contracts/{id}/         # Get contract details
PUT    /api/projects/contracts/{id}/         # Update contract
PATCH  /api/projects/contracts/{id}/         # Partial update contract
DELETE /api/projects/contracts/{id}/         # Delete contract

Query Parameters:
  ?project={project_id}
  ?status=draft|pending|active|completed|cancelled
  ?search={query}
```

## Tasks Endpoints

### Tasks
```
GET    /api/tasks/                   # List all tasks
POST   /api/tasks/                   # Create new task
GET    /api/tasks/{id}/              # Get task details
PUT    /api/tasks/{id}/              # Update task
PATCH  /api/tasks/{id}/              # Partial update task
DELETE /api/tasks/{id}/              # Delete task
POST   /api/tasks/{id}/complete/    # Mark task as complete
GET    /api/tasks/{id}/subtasks/    # Get task subtasks

Query Parameters:
  ?project={project_id}
  ?status=todo|in_progress|review|testing|done|blocked|cancelled
  ?priority=low|medium|high|critical
  ?task_type=SMW|CSDIP|LAN_PKP_PLK|SMOK_IP|SSWiN|SSP|SUG|OTHER
  ?assigned_to={user_id}
  ?parent={task_id}|null
  ?search={query}
  ?ordering=title,-title,status,priority,due_date
```

## BOM (Bill of Materials) Endpoints

### Components
```
GET    /api/bom/components/          # List all components
POST   /api/bom/components/          # Create new component
GET    /api/bom/components/{id}/     # Get component details
PUT    /api/bom/components/{id}/     # Update component
PATCH  /api/bom/components/{id}/     # Partial update component
DELETE /api/bom/components/{id}/     # Delete component

Query Parameters:
  ?category=cable|connector|device|enclosure|power|accessory|other
  ?is_active=true|false
  ?low_stock=true
  ?search={query}
```

### BOM Templates
```
GET    /api/bom/templates/           # List all BOM templates
POST   /api/bom/templates/           # Create new BOM template
GET    /api/bom/templates/{id}/      # Get BOM template details
PUT    /api/bom/templates/{id}/      # Update BOM template
PATCH  /api/bom/templates/{id}/      # Partial update BOM template
DELETE /api/bom/templates/{id}/      # Delete BOM template

Query Parameters:
  ?task_type={task_type}
  ?is_active=true|false
  ?search={query}
```

### BOM Template Items
```
GET    /api/bom/template-items/      # List all template items
POST   /api/bom/template-items/      # Create template item
GET    /api/bom/template-items/{id}/ # Get template item details
PUT    /api/bom/template-items/{id}/ # Update template item
DELETE /api/bom/template-items/{id}/ # Delete template item

Query Parameters:
  ?template={template_id}
```

### BOM Instances
```
GET    /api/bom/instances/           # List all BOM instances
POST   /api/bom/instances/           # Create new BOM instance
GET    /api/bom/instances/{id}/      # Get BOM instance details
PUT    /api/bom/instances/{id}/      # Update BOM instance
PATCH  /api/bom/instances/{id}/      # Partial update BOM instance
DELETE /api/bom/instances/{id}/      # Delete BOM instance

Query Parameters:
  ?project={project_id}
  ?status=draft|approved|ordered|received|installed
  ?search={query}
```

### BOM Instance Items
```
GET    /api/bom/instance-items/      # List all instance items
POST   /api/bom/instance-items/      # Create instance item
GET    /api/bom/instance-items/{id}/ # Get instance item details
PUT    /api/bom/instance-items/{id}/ # Update instance item
DELETE /api/bom/instance-items/{id}/ # Delete instance item

Query Parameters:
  ?bom_instance={instance_id}
```

## Devices Endpoints

### Devices
```
GET    /api/devices/                 # List all devices
POST   /api/devices/                 # Create new device
GET    /api/devices/{id}/            # Get device details
PUT    /api/devices/{id}/            # Update device
PATCH  /api/devices/{id}/            # Partial update device
DELETE /api/devices/{id}/            # Delete device

Query Parameters:
  ?project={project_id}
  ?device_type=camera|switch|router|server|sensor|controller|other
  ?status=planned|ordered|received|configured|installed|operational|maintenance|decommissioned
  ?search={query}
```

## IPAM (IP Address Management) Endpoints

### IP Address Pools
```
GET    /api/ipam/pools/              # List all IP pools
POST   /api/ipam/pools/              # Create new IP pool
GET    /api/ipam/pools/{id}/         # Get IP pool details
PUT    /api/ipam/pools/{id}/         # Update IP pool
PATCH  /api/ipam/pools/{id}/         # Partial update IP pool
DELETE /api/ipam/pools/{id}/         # Delete IP pool

Query Parameters:
  ?project={project_id}
  ?search={query}
```

### IP Addresses
```
GET    /api/ipam/addresses/          # List all IP addresses
POST   /api/ipam/addresses/          # Create new IP address
GET    /api/ipam/addresses/{id}/     # Get IP address details
PUT    /api/ipam/addresses/{id}/     # Update IP address
PATCH  /api/ipam/addresses/{id}/     # Partial update IP address
DELETE /api/ipam/addresses/{id}/     # Delete IP address

Query Parameters:
  ?pool={pool_id}
  ?device={device_id}
  ?status=available|allocated|reserved|deprecated
  ?search={query}
```

## Documents Endpoints

### Documents
```
GET    /api/documents/documents/             # List all documents
POST   /api/documents/documents/             # Upload new document
GET    /api/documents/documents/{id}/        # Get document details
PUT    /api/documents/documents/{id}/        # Update document
PATCH  /api/documents/documents/{id}/        # Partial update document
DELETE /api/documents/documents/{id}/        # Delete document

Query Parameters:
  ?project={project_id}
  ?task={task_id}
  ?document_type=manual|specification|drawing|report|contract|certificate|other
  ?search={query}
```

### Photos
```
GET    /api/documents/photos/                # List all photos
POST   /api/documents/photos/                # Upload new photo
GET    /api/documents/photos/{id}/           # Get photo details
PUT    /api/documents/photos/{id}/           # Update photo
PATCH  /api/documents/photos/{id}/           # Partial update photo
DELETE /api/documents/photos/{id}/           # Delete photo

Query Parameters:
  ?project={project_id}
  ?task={task_id}
  ?search={query}
```

## Statistics Endpoints

### Work Logs
```
GET    /api/statistics/worklogs/             # List all work logs
POST   /api/statistics/worklogs/             # Create new work log
GET    /api/statistics/worklogs/{id}/        # Get work log details
PUT    /api/statistics/worklogs/{id}/        # Update work log
PATCH  /api/statistics/worklogs/{id}/        # Partial update work log
DELETE /api/statistics/worklogs/{id}/        # Delete work log

Query Parameters:
  ?task={task_id}
  ?user={user_id}
  ?start_date={date}
  ?end_date={date}
  ?search={query}
```

### Metrics
```
GET    /api/statistics/metrics/              # List all metrics
POST   /api/statistics/metrics/              # Create new metric
GET    /api/statistics/metrics/{id}/         # Get metric details
PUT    /api/statistics/metrics/{id}/         # Update metric
PATCH  /api/statistics/metrics/{id}/         # Partial update metric
DELETE /api/statistics/metrics/{id}/         # Delete metric

Query Parameters:
  ?project={project_id}
  ?metric_type=progress|quality|performance|cost|custom
  ?search={query}
```

## Installation Endpoints

### Checklists
```
GET    /api/installation/checklists/         # List all checklists
POST   /api/installation/checklists/         # Create new checklist
GET    /api/installation/checklists/{id}/    # Get checklist details
PUT    /api/installation/checklists/{id}/    # Update checklist
PATCH  /api/installation/checklists/{id}/    # Partial update checklist
DELETE /api/installation/checklists/{id}/    # Delete checklist
POST   /api/installation/checklists/{id}/complete/  # Complete checklist

Query Parameters:
  ?task={task_id}
  ?status=draft|active|completed|cancelled
  ?assigned_to={user_id}
  ?search={query}
```

### Checklist Items
```
GET    /api/installation/items/              # List all checklist items
POST   /api/installation/items/              # Create new item
GET    /api/installation/items/{id}/         # Get item details
PUT    /api/installation/items/{id}/         # Update item
PATCH  /api/installation/items/{id}/         # Partial update item
DELETE /api/installation/items/{id}/         # Delete item
POST   /api/installation/items/{id}/toggle_complete/  # Toggle completion

Query Parameters:
  ?checklist={checklist_id}
  ?is_completed=true|false
  ?search={query}
```

## Documentation Endpoints

### API Schema & Documentation
```
GET    /api/schema/                  # OpenAPI schema (JSON)
GET    /api/schema/swagger/          # Swagger UI documentation
GET    /api/schema/redoc/            # ReDoc documentation
```

### Admin Panel
```
GET    /admin/                       # Django admin panel login
```

## Common Query Parameters

All list endpoints support:
- `?search={query}` - Full-text search
- `?ordering={field}` - Order by field (prefix with `-` for descending)
- `?page={number}` - Page number
- `?page_size={number}` - Items per page (max 100)

## Common Response Codes

- `200 OK` - Success
- `201 Created` - Resource created successfully
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Authentication

All endpoints (except `/api/auth/token/` and `POST /api/auth/users/`) require JWT authentication:

```bash
# Obtain token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Use token in requests
curl http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Example Usage

### Create a Project
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Railway Station Network",
    "code": "RSN-001",
    "status": "planning",
    "priority": "high",
    "client": "PKP PLK",
    "manager": 1
  }'
```

### Create a Task
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project": 1,
    "title": "Install SMW cameras",
    "task_type": "SMW",
    "status": "todo",
    "priority": "high",
    "assigned_to": 2
  }'
```

### Upload a Document
```bash
curl -X POST http://localhost:8000/api/documents/documents/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "project=1" \
  -F "title=Installation Manual" \
  -F "document_type=manual" \
  -F "file=@/path/to/file.pdf"
```

## For More Information

- API Documentation: http://localhost:8000/api/schema/swagger/
- Project README: [README.md](README.md)
- Quick Start Guide: [QUICKSTART.md](QUICKSTART.md)
