# BusinessIntelligence.ai

### KPI Intelligence-to-Action Engine

BusinessIntelligence.ai is an AI-assisted business intelligence platform that detects material KPI movements, identifies and ranks likely business drivers, evaluates evidence and confidence, and recommends practical actions.

The platform combines deterministic analytics, statistical analysis, business rules, governed KPI definitions, and Large Language Models (LLMs).

> **Core principle:** The LLM is not the source of quantitative truth. All KPI calculations, contribution analysis, confidence evaluation, and business rules are performed using deterministic/statistical methods. The LLM is used primarily for intent understanding, contextual synthesis, and persona-specific narrative generation.

---

## 1. Problem Statement

Businesses commonly monitor KPIs across fragmented systems such as sales, marketing, inventory, and operational platforms.

A simple dashboard can show that:

> Revenue decreased by 18%.

However, business users need to know:

- What changed?
- Why did it change?
- Which drivers contributed most?
- How reliable is the explanation?
- What action should be taken?
- Who should take the action?
- What evidence supports the conclusion?

BusinessIntelligence.ai addresses this problem by converting KPI movements into evidence-backed business insights and recommended actions.

---

## 2. Solution

The platform follows the pipeline:

```text
Data Sources
     ↓
Data Reconciliation
     ↓
KPI / Semantic Layer
     ↓
Material Movement Detection
     ↓
Driver Analysis
     ↓
Evidence & Confidence Engine
     ↓
Action Recommendation
     ↓
LLM Narrative Generation
     ↓
Persona-Specific Insight
```

---

## 3. Key Features

### KPI Movement Detection

Automatically detects significant changes in business KPIs using configurable materiality thresholds and business impact.

Example:

```text
Revenue:
Previous Period: ₹10,00,000
Current Period:  ₹8,20,000

Change: -18%
Status: Material Movement
```

### Driver Analysis

Breaks down KPI changes into potential explanatory drivers.

Example:

```text
Revenue ↓ 18%

Top Drivers:
1. Paid Channel Orders     → 52%
2. Inventory Availability  → 28%
3. AOV Decline             → 15%
4. Other                   → 5%
```

### Evidence-Based Insights

Each insight provides traceable evidence such as:

- Source dataset
- Source freshness
- KPI values
- Driver contribution
- Analytical method
- Confidence score
- KPI lineage

### Confidence & Abstention

The system does not force an explanation when evidence is insufficient.

Example:

```text
Confidence: 42%

Unable to determine the primary driver because:
- Sales data is stale
- Inventory data is incomplete
- Historical baseline is insufficient
```

The system can therefore abstain instead of generating an unsupported explanation.

### Sparse-History Handling

New products and categories may not have enough historical data for reliable anomaly detection.

The system detects insufficient history and avoids presenting misleading conclusions.

### Persona-Specific Narratives

The same analytical result is presented differently based on the user's role.

#### CEO

Focuses on:

- Business impact
- Major drivers
- Strategic action

#### Marketing Manager

Focuses on:

- Campaign performance
- Marketing levers
- Tactical recommendations

#### Data Analyst

Focuses on:

- KPI values
- Contribution
- Evidence
- Analytical methodology
- Confidence

### Action Recommendations

Recommendations follow:

```text
Driver
   ↓
Controllable Lever
   ↓
Action
   ↓
Expected Impact
   ↓
Owner
   ↓
Confidence
   ↓
Monitoring Plan
```

### Role-Based Security

The system supports role-based access to business information.

Example:

```text
CEO
 └── Business KPIs

Marketing Manager
 ├── Marketing
 ├── Sales
 └── Campaign Performance

Restricted
 └── Financial / sensitive KPIs
```

### Feedback Loop

Users can provide feedback on generated insights.

Feedback can capture:

- Correct / incorrect insight
- Actual driver
- User comments
- Timestamp
- Insight ID

This feedback can be used for continuous evaluation and future improvement.

### Runtime Telemetry

The system tracks:

- API latency
- Analytical processing time
- LLM latency
- Number of LLM calls
- Input tokens
- Output tokens
- Estimated LLM cost
- Errors

---

# 4. Data Sources

The prototype uses three heterogeneous business data sources.

## Sales

Contains transactional information such as:

```text
Order ID
Date
Product
Region
Channel
Quantity
Revenue
```

Used for:

- Revenue
- Orders
- AOV
- Product performance
- Regional performance
- Channel performance

## Marketing

Contains campaign-level information such as:

```text
Date
Campaign
Channel
Region
Spend
Clicks
Conversions
```

Used for:

- Marketing spend
- Campaign performance
- Channel performance
- Marketing-related drivers

## Inventory

Contains product availability information such as:

```text
Date
Product
Region
Stock
Reorder Level
Stockout Status
```

Used for:

- Inventory availability
- Stockout detection
- Product availability analysis
- Inventory-related drivers

---

# 5. KPIs

The prototype supports the following KPIs.

| KPI | Formula |
|---|---|
| Revenue | SUM(revenue) |
| Orders | COUNT(order_id) |
| AOV | Revenue / Orders |
| Marketing Spend | SUM(spend) |
| Conversion Rate | Conversions / Clicks |

Each KPI is associated with:

- Definition
- Formula
- Source
- Owner
- Refresh frequency
- Materiality threshold
- Drivers
- Access restrictions
- Lineage

---

# 6. Example Insight

Suppose the system detects:

```text
Revenue decreased by 18%.
```

The analytical layer identifies:

```text
Orders decreased by 12%.
AOV decreased by 6%.
Paid-channel orders decreased by 24%.
Marketing spend decreased by 15%.
```

The driver analysis produces:

```text
Paid-channel performance → 52%
AOV decline             → 25%
Inventory availability → 18%
Other                   → 5%
```

The evidence and confidence engine produces:

```text
Confidence: 87%
Evidence quality: High
Sales freshness: 2 hours
Marketing freshness: 1 hour
Inventory freshness: 3 hours
```

The LLM then converts these verified results into a narrative:

> Revenue declined 18%, primarily driven by lower paid-channel orders. Paid-channel performance contributed approximately 52% of the decline, following a reduction in marketing spend. The marketing team should review campaign allocation and prioritize high-performing campaigns.

The LLM does not calculate the 18%, 52%, or 87%.

---

# 7. LLM vs Non-LLM Architecture

## Deterministic / Statistical Layer

Used for:

- Data validation
- KPI calculation
- Aggregation
- Materiality detection
- Contribution analysis
- Statistical analysis
- Confidence scoring
- Data freshness
- Business rules
- Access control
- Lineage

Technologies:

```text
SQL
Python
Pandas
NumPy
Scikit-learn
```

## LLM Layer

Used for:

- User intent understanding
- Contextual synthesis
- Persona-specific narrative generation
- Evidence summarization
- Natural-language recommendations

This separation prevents hallucinated quantitative results from becoming business decisions.

---

# 8. Architecture

```text
                    ┌─────────────────┐
                    │   Sales Data    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Marketing Data  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Inventory Data  │
                    └────────┬────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Data Reconciliation  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ KPI Semantic Layer   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Movement Detection   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Driver Analysis      │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Evidence + Confidence│
                  └──────────┬───────────┘
                             │
                   ┌─────────┴─────────┐
                   │                   │
                   ▼                   ▼
              Strong Evidence     Weak Evidence
                   │                   │
                   ▼                   ▼
              Recommendation       Abstention
                   │
                   ▼
             ┌──────────────┐
             │     LLM      │
             └──────┬───────┘
                    │
                    ▼
          Persona-Specific Insight
                    │
                    ▼
             Streamlit UI
```

---

# 9. Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | PostgreSQL |
| Data Processing | Pandas, NumPy |
| Analytics / ML | Scikit-learn |
| Visualization | Plotly |
| LLM | OpenAI API |
| Authentication | Role-Based Access Control |
| Containerization | Docker |
| Version Control | Git / GitHub |
| Deployment | AWS / Cloud Environment |

---

# 10. Project Structure

```text
BusinessIntelligence.ai/
│
├── app/
│   ├── api/
│   ├── analytics/
│   ├── services/
│   ├── models/
│   ├── database/
│   ├── security/
│   ├── llm/
│   └── utils/
│
├── data/
│   ├── sales.csv
│   ├── marketing.csv
│   └── inventory.csv
│
├── frontend/
│   └── streamlit_app.py
│
├── tests/
│
├── scripts/
│
├── docs/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Adjust the structure above to match the actual implementation.

---

# 11. Installation

## Prerequisites

Make sure the following are installed:

```text
Python 3.x
PostgreSQL
Git
Docker (optional)
```

## Clone Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd BusinessIntelligence.ai
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 12. Environment Variables

Create a `.env` file:

```env
DATABASE_URL=<YOUR_DATABASE_URL>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

Never commit `.env` to Git.

Use `.env.example` for sharing the required configuration structure.

---

# 13. Database Setup

Create the PostgreSQL database and configure the connection using `DATABASE_URL`.

Run the application's database initialization or migration command:

```bash
<YOUR_DATABASE_COMMAND>
```

Replace the command above with the actual command used in the project.

---

# 14. Run the Application

## Start Backend

```bash
uvicorn app.main:app --reload
```

## Start Streamlit

```bash
streamlit run frontend/streamlit_app.py
```

The application can then be accessed through the local URLs shown by the backend and Streamlit.

---

# 15. Docker

Build and start the application:

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

---

# 16. Required Demo Scenarios

The prototype demonstrates five important business scenarios.

### Scenario 1 — Material KPI Movement

Revenue decreases significantly.

Expected behavior:

```text
Alert
→ Driver analysis
→ Contribution
→ Evidence
→ Confidence
→ Recommended action
```

### Scenario 2 — Low Confidence

Introduce stale or incomplete data.

Expected behavior:

```text
Low confidence
→ Evidence warning
→ Abstention
→ Request for additional information
```

### Scenario 3 — New Product

Introduce a product with insufficient historical data.

Expected behavior:

```text
Sparse history detected
→ Reliable baseline unavailable
→ Low confidence / abstention
```

### Scenario 4 — Role-Based Security

Login using different personas.

Expected behavior:

```text
Different roles
→ Different data access
→ Different insight depth
→ Different recommendations
```

### Scenario 5 — Analyst Feedback

Mark an insight as incorrect and provide the actual driver.

Expected behavior:

```text
User feedback
→ Stored
→ Available for evaluation
→ Can support future improvements
```

---

# 17. Testing

Run the test suite:

```bash
pytest
```

The test suite covers:

- KPI calculations
- Movement detection
- Driver analysis
- Confidence scoring
- Abstention
- API behavior
- Role-based access
- Error handling

---

# 18. Security Considerations

The prototype considers:

- Role-based access
- Restricted KPIs
- Environment-based secrets
- API authentication
- Data access controls
- Auditability
- LLM prompt/data boundaries

Sensitive information should not be sent to the LLM unless explicitly permitted by the application's access policy.

---

# 19. Design Principles

### Quantitative Truth

```text
SQL / Python / Statistics
        ↓
Verified Numbers
```

### Business Context

```text
KPI Metadata
+
Business Rules
+
Evidence
```

### Language Generation

```text
Verified Results
        ↓
       LLM
        ↓
Human-readable Insight
```

### Uncertainty

```text
Strong Evidence
     → Explain

Weak / Contradictory Evidence
     → Abstain
```

---

# 20. Future Enhancements

Potential future improvements include:

- Causal inference for stronger driver attribution
- Forecast-based anomaly detection
- Real-time streaming data
- Knowledge graphs for business context
- Advanced data lineage
- Automated model/data drift detection
- Feedback-driven model improvement
- Insight caching
- Multi-model LLM routing for cost optimization
- Enterprise SSO
- Row-level and column-level security
- Additional BI platform integrations

---

# 21. Project Outcome

BusinessIntelligence.ai transforms traditional KPI monitoring from:

```text
"What changed?"
```

into:

```text
"What changed?"
        ↓
"Why did it change?"
        ↓
"How confident are we?"
        ↓
"What evidence supports it?"
        ↓
"What should we do?"
        ↓
"Who should act?"
```

The result is an evidence-backed KPI intelligence system that helps business users move from **metrics to decisions**.

---

## 22. Submission Highlights

This prototype demonstrates:

- ✅ Material KPI movement detection
- ✅ Multi-source data reconciliation
- ✅ Driver contribution analysis
- ✅ Governed KPI semantics
- ✅ Evidence-backed explanations
- ✅ Confidence scoring
- ✅ Abstention under uncertainty
- ✅ Sparse-history handling
- ✅ Persona-specific narratives
- ✅ Action recommendations
- ✅ Role-based security
- ✅ Analyst feedback loop
- ✅ Runtime and LLM cost telemetry
- ✅ Clear separation of LLM and deterministic analytics

---

## 23. Team

**Project:** BusinessIntelligence.ai

**Track:** Problem Track 3 — BusinessIntelligence.ai

**Round:** Round 2

**Team Members:**
- <NAME>
- <NAME>
- <NAME>

**Repository:** <GITHUB_REPOSITORY_URL>

**Demo:** <DEPLOYED_APPLICATION_URL>

**Presentation:** <PRESENTATION_URL>

---