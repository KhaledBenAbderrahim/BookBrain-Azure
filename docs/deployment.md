# Deployment Guide

## Overview
This guide covers the deployment process for BookBrain-Azure, including environment setup, configuration, and best practices for production deployment.

## Prerequisites

### Required Tools
- Azure CLI
- Azure Functions Core Tools
- Python 3.8 or higher
- Git
- Visual Studio Code (recommended)

### Azure Resources
1. **Azure Subscription**
2. **Resource Group**
3. **Function App**
   - Python runtime
   - Consumption plan (or Premium for production)
4. **Storage Account**
5. **PostgreSQL Database**
6. **Application Insights**

## Environment Setup

### 1. Local Development Setup

```bash
# Clone repository
git clone https://github.com/YourUsername/BookBrain-Azure.git
cd BookBrain-Azure

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure local settings
cp .env.example .env
# Edit .env with your settings
```

### 2. Azure Resources Creation

```bash
# Login to Azure
az login

# Create resource group
az group create --name bookbrain-rg --location westeurope

# Create storage account
az storage account create \
    --name bookbrainstorage \
    --resource-group bookbrain-rg \
    --location westeurope \
    --sku Standard_LRS

# Create Function App
az functionapp create \
    --name bookbrain-func \
    --resource-group bookbrain-rg \
    --storage-account bookbrainstorage \
    --runtime python \
    --runtime-version 3.8 \
    --functions-version 4 \
    --os-type linux \
    --consumption-plan-location westeurope
```

## Configuration

### 1. Application Settings

Set these in Azure Portal or using Azure CLI:

```bash
az functionapp config appsettings set \
    --name bookbrain-func \
    --resource-group bookbrain-rg \
    --settings \
    AZURE_STORAGE_CONNECTION_STRING="your_connection_string" \
    DB_HOST="your_db_host" \
    DB_NAME="your_db_name" \
    DB_USER="your_db_user" \
    DB_PASSWORD="your_db_password"
```

### 2. Database Setup

```sql
-- Create required tables
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    isbn VARCHAR(13),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id),
    content TEXT,
    page_number INTEGER,
    chapter VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes
CREATE INDEX idx_books_isbn ON books(isbn);
CREATE INDEX idx_chunks_book_id ON chunks(book_id);
```

## Deployment Steps

### 1. Prepare for Deployment

```bash
# Build deployment package
func azure functionapp publish bookbrain-func --build remote
```

### 2. Deploy to Azure

```bash
# Deploy using Azure Functions Core Tools
func azure functionapp publish bookbrain-func

# Or using Azure CLI
az functionapp deployment source config-zip \
    --name bookbrain-func \
    --resource-group bookbrain-rg \
    --src dist/package.zip
```

### 3. Verify Deployment

```bash
# Test endpoints
curl https://bookbrain-func.azurewebsites.net/api/HealthCheck
```

## Security Configuration

### 1. Enable Authentication

```bash
# Enable App Service Authentication
az webapp auth update \
    --name bookbrain-func \
    --resource-group bookbrain-rg \
    --enabled true \
    --action LoginWithAzureActiveDirectory \
    --aad-allowed-token-audiences "api://bookbrain-func"
```

### 2. Network Security

```bash
# Configure network rules
az functionapp network-rule add \
    --name bookbrain-func \
    --resource-group bookbrain-rg \
    --ip-address "your_ip_range"
```

## Monitoring Setup

### 1. Application Insights

```bash
# Enable Application Insights
az functionapp config appsettings set \
    --name bookbrain-func \
    --resource-group bookbrain-rg \
    --settings APPINSIGHTS_INSTRUMENTATIONKEY="your_key"
```

### 2. Alert Rules

```bash
# Create alert rule for errors
az monitor metrics alert create \
    --name bookbrain-error-alert \
    --resource-group bookbrain-rg \
    --scopes "/subscriptions/{subscription-id}/resourceGroups/bookbrain-rg/providers/Microsoft.Web/sites/bookbrain-func" \
    --condition "count requests.failed gt 10" \
    --window-size 5m \
    --evaluation-frequency 1m
```

## Scaling Configuration

### 1. Consumption Plan Settings

```bash
# Configure scaling
az functionapp plan update \
    --name bookbrain-plan \
    --resource-group bookbrain-rg \
    --max-burst 20 \
    --min-instances 1 \
    --max-instances 10
```

### 2. Premium Plan (if needed)

```bash
# Upgrade to premium plan
az functionapp plan create \
    --name bookbrain-premium-plan \
    --resource-group bookbrain-rg \
    --sku EP1 \
    --min-instances 1 \
    --max-instances 10
```

## Backup and Disaster Recovery

### 1. Database Backup

```bash
# Configure automated backups
az postgres server update \
    --name bookbrain-db \
    --resource-group bookbrain-rg \
    --backup-retention 7
```

### 2. Application Backup

```bash
# Enable backup
az webapp backup create \
    --resource-group bookbrain-rg \
    --webapp-name bookbrain-func \
    --container-url "your_storage_container_url" \
    --backup-name initial-backup
```

## Maintenance Procedures

### 1. Update Dependencies

```bash
# Update Python packages
pip install --upgrade -r requirements.txt
```

### 2. Database Maintenance

```sql
-- Regular maintenance tasks
VACUUM ANALYZE;
REINDEX DATABASE bookbrain;
```

## Troubleshooting

### Common Issues

1. **Connection Issues**
```bash
# Test database connection
az postgres flexible-server connect \
    --name bookbrain-db \
    --admin-user your_admin \
    --admin-password your_password
```

2. **Performance Issues**
```bash
# Check function metrics
az monitor metrics list \
    --resource bookbrain-func \
    --resource-group bookbrain-rg \
    --metric "FunctionExecutionUnits"
```

## Best Practices

1. **Deployment**
   - Use staged deployments
   - Implement blue-green deployment
   - Maintain deployment scripts

2. **Monitoring**
   - Set up comprehensive logging
   - Configure appropriate alerts
   - Monitor resource usage

3. **Security**
   - Regular security audits
   - Keep dependencies updated
   - Implement proper authentication

4. **Performance**
   - Optimize database queries
   - Configure appropriate scaling
   - Monitor resource usage
