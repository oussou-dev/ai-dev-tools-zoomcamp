# ☁️ AWS ECS/Fargate Deployment Guide

Complete guide to deploy the **AI News Aggregator** on AWS using ECS (Elastic Container Service) and Fargate.

---

## 📋 Prerequisites

- AWS account (https://aws.amazon.com)
- AWS CLI configured locally
- ECR (Elastic Container Registry) repository
- RDS PostgreSQL instance
- IAM permissions for ECS, ECR, RDS
- Docker images built and pushed to ECR

---

## **Step 1: Create RDS PostgreSQL Database**

### via AWS Console:
1. Go to **RDS Dashboard** → **"Create database"**
2. Configure:
   - **Engine**: PostgreSQL
   - **Version**: 15 or later
   - **DB instance class**: `db.t3.micro` (free tier)
   - **Storage**: 20GB
   - **DB name**: `ai_news_aggregator`
   - **Master username**: `postgres`
   - **Password**: Your secure password
   - **VPC**: Default or create new
   - **Publicly accessible**: Yes (for simplicity, restrict in production)

3. Click **"Create database"**
4. Wait for creation (5-10 minutes)
5. Note the **Endpoint** (e.g., `xxx.rds.amazonaws.com`)

### Connection String:
```
postgresql://postgres:password@xxx.rds.amazonaws.com:5432/ai_news_aggregator
```

---

## **Step 2: Push Docker Images to ECR**

### Create ECR Repositories:

```bash
# Create backend repository
aws ecr create-repository --repository-name ai-news-api --region us-east-1

# Create frontend repository
aws ecr create-repository --repository-name ai-news-frontend --region us-east-1
```

### Get Login Token:

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin xxx.dkr.ecr.us-east-1.amazonaws.com
```

### Build and Push Backend:

```bash
# Build image
docker build -t ai-news-api:latest -f docker/Dockerfile.api .

# Tag image
docker tag ai-news-api:latest xxx.dkr.ecr.us-east-1.amazonaws.com/ai-news-api:latest

# Push to ECR
docker push xxx.dkr.ecr.us-east-1.amazonaws.com/ai-news-api:latest
```

### Build and Push Frontend:

```bash
# Build image
docker build -t ai-news-frontend:latest -f docker/Dockerfile.frontend .

# Tag image
docker tag ai-news-frontend:latest xxx.dkr.ecr.us-east-1.amazonaws.com/ai-news-frontend:latest

# Push to ECR
docker push xxx.dkr.ecr.us-east-1.amazonaws.com/ai-news-frontend:latest
```

---

## **Step 3: Create ECS Cluster**

### via AWS Console:
1. Go to **ECS Dashboard** → **"Create Cluster"**
2. Configure:
   - **Cluster name**: `ai-news-cluster`
   - **Networking**: Default VPC
   - **Infrastructure**: Fargate
   - **Monitoring**: Enable CloudWatch (optional)

3. Click **"Create"**

---

## **Step 4: Create ECS Task Definition for Backend**

### via AWS Console:
1. Go to **ECS** → **"Task Definitions"** → **"Create new task definition"**
2. Configure:
   - **Task Definition Name**: `ai-news-api`
   - **Launch Type**: Fargate
   - **OS**: Linux
   - **CPU**: 256 (0.25 vCPU)
   - **Memory**: 512 MB

### Add Container:
1. Click **"Add Container"**
2. Configure:
   - **Name**: `api`
   - **Image**: `xxx.dkr.ecr.us-east-1.amazonaws.com/ai-news-api:latest`
   - **Port**: `8000`
   - **Essential**: Yes

### Add Environment Variables:
Click **"Add environment variables"**

```
OPENAI_API_KEY=sk-xxx...
ANTHROPIC_API_KEY=claude-xxx...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
DATABASE_URL=postgresql://postgres:password@xxx.rds.amazonaws.com:5432/ai_news_aggregator
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
POSTGRES_DB=ai_news_aggregator
POSTGRES_HOST=xxx.rds.amazonaws.com
POSTGRES_PORT=5432
```

3. Click **"Create"**

---

## **Step 5: Create ECS Task Definition for Frontend**

### via AWS Console:
1. Go to **ECS** → **"Task Definitions"** → **"Create new task definition"**
2. Configure:
   - **Task Definition Name**: `ai-news-frontend`
   - **Launch Type**: Fargate
   - **OS**: Linux
   - **CPU**: 256
   - **Memory**: 512 MB

### Add Container:
1. Click **"Add Container"**
2. Configure:
   - **Name**: `frontend`
   - **Image**: `xxx.dkr.ecr.us-east-1.amazonaws.com/ai-news-frontend:latest`
   - **Port**: `8501`
   - **Essential**: Yes

### Add Environment Variables:
```
API_URL=http://ai-news-api-alb-xxx.us-east-1.elb.amazonaws.com:8000
```

Replace with your backend ALB DNS name (created next).

3. Click **"Create"**

---

## **Step 6: Create Application Load Balancer (ALB)**

### Create ALB:
1. Go to **EC2** → **"Load Balancers"** → **"Create load balancer"**
2. Select **"Application Load Balancer"**
3. Configure:
   - **Name**: `ai-news-alb`
   - **Scheme**: Internet-facing
   - **VPC**: Same as ECS cluster
   - **Subnets**: Select multiple (2+)

### Create Target Groups:

**For Backend:**
1. Go to **"Target Groups"** → **"Create target group"**
2. Configure:
   - **Name**: `ai-news-api-tg`
   - **Protocol**: HTTP
   - **Port**: 8000
   - **VPC**: Same as ALB

**For Frontend:**
1. Create another target group:
   - **Name**: `ai-news-frontend-tg`
   - **Protocol**: HTTP
   - **Port**: 8501

### Create Listeners:
1. On ALB → **"Listeners"** → **"Add listener"**
2. Configure:
   - **Protocol**: HTTP
   - **Port**: 8000
   - **Target Group**: `ai-news-api-tg`

3. Add another listener:
   - **Port**: 8501
   - **Target Group**: `ai-news-frontend-tg`

---

## **Step 7: Create ECS Services**

### Create Backend Service:
1. Go to **ECS Cluster** → **"Services"** → **"Create service"**
2. Configure:
   - **Launch Type**: Fargate
   - **Task Definition**: `ai-news-api`
   - **Service Name**: `ai-news-api-service`
   - **Desired Count**: 1

### Configure Network:
1. **VPC**: Same as cluster
2. **Subnets**: Select 2+
3. **Security Group**: Create or select (allow port 8000)

### Load Balancer:
1. **Load Balancer Type**: Application Load Balancer
2. **Target Group**: `ai-news-api-tg`
3. Click **"Create service"**

### Create Frontend Service:
Repeat the same steps for frontend:
- **Task Definition**: `ai-news-frontend`
- **Service Name**: `ai-news-frontend-service`
- **Desired Count**: 1
- **Target Group**: `ai-news-frontend-tg`

---

## **Step 8: Verify Deployment**

### Check Services Running:
```bash
aws ecs list-services --cluster ai-news-cluster --region us-east-1
```

### Get ALB DNS Name:
```bash
aws elbv2 describe-load-balancers --region us-east-1 --query 'LoadBalancers[0].DNSName'
```

### Access Frontend:
```bash
http://<ALB-DNS>:8501
```

### Check Backend:
```bash
curl http://<ALB-DNS>:8000/health
# Response: {"status": "ok"}
```

---

## **Quick Reference: AWS Environment Variables**

### **Backend Task Definition:**
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
DATABASE_URL=postgresql://postgres:password@xxx.rds.amazonaws.com:5432/ai_news_aggregator
POSTGRES_HOST=xxx.rds.amazonaws.com
POSTGRES_PORT=5432
```

### **Frontend Task Definition:**
```
API_URL=http://ai-news-alb-xxx.us-east-1.elb.amazonaws.com:8000
```

---

## **Complete AWS Architecture**

```
┌─────────────────────────────────────────────────────────┐
│              AWS ECS/Fargate Deployment                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐     ┌──────────────┐                │
│  │  RDS         │ ←── │  ECS Task    │                │
│  │  PostgreSQL  │     │  (Backend)   │                │
│  └──────────────┘     └──────┬───────┘                │
│                              │                        │
│  ┌─────────────────────────────────────────────────┐ │
│  │     Application Load Balancer (ALB)             │ │
│  │  Port 8000 → Backend | Port 8501 → Frontend    │ │
│  └─────────────────────────────────────────────────┘ │
│                              │                        │
│                       ┌──────▼───────┐               │
│                       │  ECS Task    │               │
│                       │  (Frontend)  │               │
│                       └──────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘

         ↓ (External Access via ALB)
    http://ai-news-alb-xxx.elb.amazonaws.com
```

---

## **Troubleshooting on AWS**

### ❌ Tasks won't start

**Check CloudWatch Logs:**
```bash
aws logs tail /ecs/ai-news-api --follow --region us-east-1
```

**Common causes:**
- Image not found in ECR
- Environment variables missing
- Port mapping issues
- IAM permissions

### ❌ Tasks keep stopping

**Check task status:**
```bash
aws ecs describe-tasks --cluster ai-news-cluster --tasks <task-arn> --region us-east-1
```

**Common causes:**
- Insufficient memory/CPU
- Database connection failure
- Application crash (check logs)

### ❌ Frontend can't reach backend

**Check ALB target groups:**
1. Go to **EC2** → **"Target Groups"**
2. Verify both are "Healthy"
3. Check security groups allow communication

**Update API_URL if needed:**
1. Go to **ECS** → **Frontend Task Definition**
2. Update environment variable
3. Create new revision
4. Update service to use new revision

### ❌ Database connection errors

**Check RDS security group:**
- Allows inbound traffic on port 5432
- From ECS security group

**Test connection from ECS task:**
```bash
aws ecs execute-command \
  --cluster ai-news-cluster \
  --task <task-id> \
  --container api \
  --interactive \
  --command "/bin/bash"

# Inside container:
psql -h xxx.rds.amazonaws.com -U postgres -d ai_news_aggregator
```

---

## **Production Tips**

### 1. **Use Auto-Scaling**
```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/ai-news-cluster/ai-news-api-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 1 \
  --max-capacity 5
```

### 2. **Enable CloudWatch Monitoring**
- Monitor CPU, memory, request count
- Set up alarms for errors

### 3. **Use Secrets Manager for Sensitive Data**
```bash
aws secretsmanager create-secret --name ai-news/openai-key --secret-string "sk-xxx"
```

### 4. **Enable RDS Backup**
- Automated daily backups
- Multi-AZ for production

### 5. **Use HTTPS with Certificate Manager**
- Create SSL certificate
- Attach to ALB listener

---

## **Cost Estimation**

| Resource | Monthly Cost |
|----------|--------------|
| ECS Fargate (0.25 vCPU x2) | ~$10 |
| RDS PostgreSQL (db.t3.micro) | ~$15 |
| ALB | ~$16 |
| Data transfer | ~$5 |
| **Total** | **~$46/month** |

---

## **Next Steps**

After deployment:

1. **Test the pipeline** - Click "🚀 Run Pipeline" in frontend
2. **Check CloudWatch logs** - Verify no errors
3. **Monitor performance** - Use CloudWatch dashboards
4. **Set up alerts** - For errors and high resource usage
5. **Configure custom domain** - Point Route53 to ALB

```
Frontend: http://ai-news-alb-xxx.us-east-1.elb.amazonaws.com:8501
API Docs: http://ai-news-alb-xxx.us-east-1.elb.amazonaws.com:8000/docs
```

---

## **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| Image not found | Push image to ECR first |
| Tasks fail immediately | Check CloudWatch logs |
| Timeout errors | Increase task timeout, check DB connection |
| API_URL not working | Update frontend task definition, restart service |
| High latency | Check ALB health, upgrade instance size |

---

## **Need Help?**

If you get stuck:

1. **Check CloudWatch logs**: Task logs visible in ECS console
2. **Verify ECR images**: `aws ecr list-images --repository-name ai-news-api`
3. **Check ALB status**: EC2 → Load Balancers → Target Groups
4. **AWS support**: https://console.aws.amazon.com/support
5. **Repository README**: See main README.md for more context

---

**You're all set!** 🚀 Your application is now deployed on AWS ECS/Fargate!
