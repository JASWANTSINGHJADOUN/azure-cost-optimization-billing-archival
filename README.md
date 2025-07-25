# azure-cost-optimization-billing-archival

# Azure Cost Optimization: Billing Records Archival

This project provides a serverless and cost-efficient solution for managing billing records in Azure. It archives old records from Cosmos DB to Blob Storage to reduce costs without affecting data availability or API contracts.

---

## 🏗️ Architecture

- **Cosmos DB** stores recent billing records (< 90 days).
- **Azure Function (Python)** automatically moves older records to **Blob Storage**.
- **API read logic** looks up Cosmos DB first; if not found, it checks archive storage.
- The system avoids downtime and retains all historical data.

![Architecture Diagram](./docs/architecture-diagram.png)

---

## 🔧 Technologies Used

- Azure Cosmos DB
- Azure Blob Storage (Cool tier)
- Azure Functions (Python)
- Azure SDK for Python
- Serverless architecture

---

## 📂 Project Structure

| Path | Description |
|------|-------------|
| `/archive-function/` | Contains the archival function to move records to Blob |
| `/api-logic/` | Contains the logic for reading records from both sources |
| `/docs/` | Architecture diagram |
| `requirements.txt` | Python dependencies |
| `chatgpt_conversation.md` | Solution conversation with ChatGPT |

---

## 🚀 How It Works

1. An Azure Function runs daily to find billing records older than 90 days.
2. These records are stored as `.json` files in Blob Storage.
3. They are then deleted from Cosmos DB to save RU and storage cost.
4. Read API logic transparently fetches data from archive if needed.

---

## ⏱️ Scheduling the Function

Use a Timer Trigger in Azure Functions to run `archive_old_records.py` daily:

```json
"schedule": "0 0 * * * *"  // every day at midnight UTC
