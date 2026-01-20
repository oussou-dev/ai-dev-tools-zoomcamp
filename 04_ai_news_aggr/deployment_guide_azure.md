# 🔷 Azure Cloud Deployment Guide

Complete guide to deploy the **AI News Aggregator** on Microsoft Azure using Container Instances and Azure Database for PostgreSQL.

---

## 📋 Prerequisites

- Azure account (https://azure.microsoft.com)
- Azure CLI installed and configured
- Resource Group created
- Docker images ready
- Azure Container Registry (ACR)
- Azure Database for PostgreSQL

---

## **Step 1: Create Azure Resource Group**

```bash
# Set variables
export RESOURCE_GROUP=ai-news-rg
export LOCATION=eastus
export ACR_NAME=ainewsacr
export DB_SERVER=ai-news-db-server

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

---

## **Step 2: Create Azure Container Registry**

```bash
# Create ACR
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic

# Login to ACR
az acr login --name $ACR_NAME
```

---

## **Step 3: Build and Push Docker Images**

### Build Backend Image:

```bash
# Build and push backend
az acr build \
  --registry $ACR_NAME \
  --image ai-news-api:latest \
  --file docker/Dockerfile.api .

# Or manually:
docker build -t $ACR_NAME.azurecr.io/ai-news-api:latest -f docker/Dockerfile.api .
az acr login --name $ACR_NAME
docker push $ACR_NAME.azurecr.io/ai-news-api:latest
```

### Build Frontend Image:

```bash
# Build and push frontend
az acr build \
  --registry $ACR_NAME \
  --image ai-news-frontend:latest \
  --file docker/Dockerfile.frontend .

# Or manually:
docker build -t $ACR_NAME.azurecr.io/ai-news-frontend:latest -f docker/Dockerfile.frontend .
docker push $ACR_NAME.azurecr.io/ai-news-frontend:latest
```

---

## **Step 4: Create Azure Database for PostgreSQL**

```bash
# Create PostgreSQL server
az postgres server create \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER \
  --location $LOCATION \
  --admin-user dbadmin \
  --admin-password YourPassword123! \
  --sku-name B_Gen5_1 \
  --storage-size 51200 \
  --version 11

# Create database
az postgres db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER \
  --name ai_news_aggregator

# Allow access from Azure services
az postgres server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER \
  --name allow-azure-services \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Get connection string
az postgres server show \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER \
  --query fullyQualifiedDomainName
```

---

## **Step 5: Create Virtual Network (VNet) - Optional but Recommended**

```bash
# Create VNet
az network vnet create \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-vnet \
  --address-prefix 10.0.0.0/16

# Create subnet
az network vnet subnet create \
  --resource-group $RESOURCE_GROUP \
  --vnet-name ai-news-vnet \
  --name ai-news-subnet \
  --address-prefix 10.0.0.0/24
```

---

## **Step 6: Deploy Backend Container Instance**

### Create Environment File:

```bash
cat > backend.env << EOF
OPENAI_API_KEY=sk-xxx...
ANTHROPIC_API_KEY=claude-xxx...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
DATABASE_URL=postgresql://dbadmin:YourPassword123!@$DB_SERVER.postgres.database.azure.com:5432/ai_news_aggregator
POSTGRES_USER=dbadmin
POSTGRES_PASSWORD=YourPassword123!
POSTGRES_DB=ai_news_aggregator
POSTGRES_HOST=$DB_SERVER.postgres.database.azure.com
POSTGRES_PORT=5432
EOF
```

### Deploy Backend:

```bash
az container create \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-api \
  --image $ACR_NAME.azurecr.io/ai-news-api:latest \
  --ports 8000 \
  --protocol TCP \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $(az acr credential show --name $ACR_NAME --query username -o tsv) \
  --registry-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv) \
  --environment-variables \
    OPENAI_API_KEY=sk-xxx... \
    ANTHROPIC_API_KEY=claude-xxx... \
    MY_EMAIL=your-email@gmail.com \
    APP_PASSWORD=your-app-password \
    DATABASE_URL=postgresql://dbadmin:YourPassword123!@$DB_SERVER.postgres.database.azure.com:5432/ai_news_aggregator \
    POSTGRES_USER=dbadmin \
    POSTGRES_DB=ai_news_aggregator \
    POSTGRES_HOST=$DB_SERVER.postgres.database.azure.com \
    POSTGRES_PORT=5432 \
  --cpu 1 \
  --memory 1
```

### Get Backend URL:

```bash
az container show \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-api \
  --query ipAddress.fqdn -o tsv
# Format: ai-news-api.eastus.azurecontainer.io
```

### Verify Backend:

```bash
BACKEND_URL=$(az container show --resource-group $RESOURCE_GROUP --name ai-news-api --query ipAddress.fqdn -o tsv)
curl http://$BACKEND_URL:8000/health
# Response: {"status": "ok"}
```

---

## **Step 7: Deploy Frontend Container Instance**

### ✨ **CRITICAL: Deploy with API_URL**

```bash
# Get backend URL
BACKEND_URL=$(az container show --resource-group $RESOURCE_GROUP --name ai-news-api --query ipAddress.fqdn -o tsv)

# Deploy frontend
az container create \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-frontend \
  --image $ACR_NAME.azurecr.io/ai-news-frontend:latest \
  --ports 8501 \
  --protocol TCP \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $(az acr credential show --name $ACR_NAME --query username -o tsv) \
  --registry-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv) \
  --environment-variables \
    API_URL=http://$BACKEND_URL:8000 \
  --cpu 1 \
  --memory 1
```

### Get Frontend URL:

```bash
az container show \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-frontend \
  --query ipAddress.fqdn -o tsv
# Format: ai-news-frontend.eastus.azurecontainer.io
```

---

## **Step 8: Verify Deployment**

### Check Containers Running:

```bash
az container list --resource-group $RESOURCE_GROUP
```

### Access Frontend:

```bash
FRONTEND_URL=$(az container show --resource-group $RESOURCE_GROUP --name ai-news-frontend --query ipAddress.fqdn -o tsv)
echo "Frontend: http://$FRONTEND_URL:8501"
# Open in browser
```

### Check Backend Health:

```bash
BACKEND_URL=$(az container show --resource-group $RESOURCE_GROUP --name ai-news-api --query ipAddress.fqdn -o tsv)
curl http://$BACKEND_URL:8000/health
# Response: {"status": "ok"}
```

---

## **Quick Reference: Azure Environment Variables**

### **Backend Container:**
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
DATABASE_URL=postgresql://dbadmin:password@server.postgres.database.azure.com:5432/ai_news_aggregator
POSTGRES_HOST=server.postgres.database.azure.com
POSTGRES_PORT=5432
```

### **Frontend Container:**
```
API_URL=http://ai-news-api.eastus.azurecontainer.io:8000
```

---

## **Complete Azure Architecture**

```
┌──────────────────────────────────────────┐
│        Microsoft Azure                   │
├──────────────────────────────────────────┤
│                                          │
│  ┌──────────────┐   ┌──────────────┐   │
│  │ Azure DB     │ ←─┤  Container   │   │
│  │ PostgreSQL   │   │  (Backend)   │   │
│  └──────────────┘   └──────┬───────┘   │
│                            │           │
│  ┌────────────────────────────────┐   │
│  │  Azure Virtual Network (VNet)  │   │
│  └────────────────────────────────┘   │
│                            │           │
│                     ┌──────▼──────┐   │
│                     │  Container  │   │
│                     │  (Frontend) │   │
│                     └─────────────┘   │
│                                          │
└──────────────────────────────────────────┘

    ↓ (External Access)
http://ai-news-frontend.eastus.azurecontainer.io
http://ai-news-api.eastus.azurecontainer.io
```

---

## **Troubleshooting on Azure**

### ❌ Container won't start

**Check container logs:**
```bash
az container logs \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-api
```

**Common causes:**
- Image not found in ACR
- Environment variables missing
- Port already in use

### ❌ Cannot connect to PostgreSQL

**Check firewall rules:**
```bash
az postgres server firewall-rule list \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER
```

**Allow your IP:**
```bash
az postgres server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER \
  --name allow-my-ip \
  --start-ip-address YOUR_IP \
  --end-ip-address YOUR_IP
```

### ❌ Frontend shows "🔴 Offline"

**Check container logs:**
```bash
az container logs \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-frontend
```

**Verify API_URL:**
```bash
az container show \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-frontend \
  --query containers[0].environmentVariables
```

**Update API_URL if needed:**
```bash
az container delete \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-frontend \
  --yes

# Redeploy with correct API_URL
```

### ❌ High latency or timeouts

**Increase CPU and memory:**
```bash
# Delete and recreate with more resources
az container delete --resource-group $RESOURCE_GROUP --name ai-news-api --yes

az container create \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-api \
  --cpu 2 \
  --memory 2 \
  # ... rest of configuration
```

---

## **Production Tips**

### 1. **Use Azure Container Registry Premium**
```bash
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Premium
```

### 2. **Enable Azure Monitor**
```bash
az container create \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-api \
  --log-analytics-workspace workspace-id \
  --log-analytics-workspace-key workspace-key
```

### 3. **Use Key Vault for Secrets**
```bash
# Create Key Vault
az keyvault create \
  --resource-group $RESOURCE_GROUP \
  --name ai-news-vault

# Store secret
az keyvault secret set \
  --vault-name ai-news-vault \
  --name openai-api-key \
  --value sk-xxx...

# Reference in container
--secure-environment-variables \
  OPENAI_API_KEY=/subscriptions/.../providers/Microsoft.KeyVault/vaults/ai-news-vault/secrets/openai-api-key
```

### 4. **Use Azure Container Instances autoscaling**
Consider upgrading to **App Service** or **Kubernetes (AKS)** for auto-scaling

### 5. **Set up Application Gateway**
For load balancing and HTTPS termination:
```bash
az network application-gateway create \
  --name ai-news-gateway \
  --resource-group $RESOURCE_GROUP
```

---

## **Cost Estimation**

| Resource | Monthly Cost |
|----------|--------------|
| Container Instances (2x) | ~$20 |
| PostgreSQL (Basic) | ~$30 |
| Container Registry | ~$5 |
| Networking | ~$3 |
| **Total** | **~$58/month** |

---

## **CLI Commands Summary**

```bash
# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy backend
az container create --resource-group $RESOURCE_GROUP --name ai-news-api ...

# Deploy frontend
az container create --resource-group $RESOURCE_GROUP --name ai-news-frontend ...

# View containers
az container list --resource-group $RESOURCE_GROUP

# View logs
az container logs --resource-group $RESOURCE_GROUP --name ai-news-api

# Update environment variable
az container delete --resource-group $RESOURCE_GROUP --name ai-news-frontend --yes
# Recreate with new variables

# Delete all resources
az group delete --resource-group $RESOURCE_GROUP --yes
```

---

## **Next Steps**

After deployment:

1. **Test the pipeline** - Click "🚀 Run Pipeline" in frontend
2. **Check logs** - Monitor Azure container logs
3. **View digests** - Should populate after pipeline runs
4. **Set up monitoring** - Use Azure Monitor
5. **Configure custom domain** - Use Azure DNS or CNAME

```
Frontend: http://ai-news-frontend.eastus.azurecontainer.io:8501
API Docs: http://ai-news-api.eastus.azurecontainer.io:8000/docs
```

---

## **Need Help?**

If you get stuck:

1. **Check container logs**: `az container logs --resource-group $RG --name service-name`
2. **Verify API_URL**: Check container environment variables
3. **Test backend**: `curl http://backend-url:8000/health`
4. **Azure support**: https://docs.microsoft.com/azure
5. **Repository README**: See main README.md for more context

---

**You're all set!** 🚀 Your application is now deployed on Azure!
