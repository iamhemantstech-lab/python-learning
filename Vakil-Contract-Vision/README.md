# ⚖️ Vakil-Contract-Vision (Legal AI Contract Analysis Engine)

> **An AI-powered legal intelligence backend specializing in Indian Contract Law (The Indian Contract Act, 1872).**  
> Automatically analyzes contracts (NDAs, Service Agreements, Employment contracts), extracts clauses, detects legal risks, and provides negotiation recommendations.

---

## 🎯 1. Purpose of the Project

In business, startups, and everyday work, non-lawyers are routinely required to sign long, complex, and predatory legal contracts. Reviewing a 20-page agreement with an attorney costs hundreds of dollars and takes days.

**Vakil-Contract-Vision** ("Vakil" means *Lawyer/Advocate* in Hindi) acts as an automated, AI-powered legal co-pilot:

1. **Document Ingestion:** Accepts PDF and TXT contract uploads, extracts raw text, and computes page/word metrics.
2. **Key Clause Extraction:** Automatically isolates critical sections (Confidentiality, Non-Compete, Indemnification, Liability Caps, Termination, Governing Law).
3. **Legal Risk Detection:** Flags one-sided or unenforceable terms under **Indian Contract Law** (e.g., post-termination non-compete clauses void under **Section 27 of the Indian Contract Act, 1872**).
4. **Actionable Recommendations:** Translates dense legal jargon into plain-English negotiation counter-proposals for business owners.
5. **Auditable Storage:** Stores all contracts and historical analysis reports in a containerized **MongoDB** database.

---

## 🏛️ 2. Project Architecture

```mermaid
flowchart TD
    subgraph CLIENT["1. Client & API Consumers"]
        USER["User / Frontend / Swagger UI"]
    end

    subgraph API_GW["2. FastAPI Application Gateway (app/main.py)"]
        FASTAPI["FastAPI Engine (:8000)"]
        STARTUP["Startup Event (init_db)"]
        FASTAPI --> STARTUP
    end

    subgraph ROUTERS["3. Modular Routing Layer (app/routes/)"]
        C_ROUTE["contracts_routes.py\n• POST /contracts/upload\n• GET /contracts/\n• GET /contracts/{id}"]
        A_ROUTE["analysis_routes.py\n• POST /analysis/analys/{id}\n• GET /analysis/\n• GET /analysis/{id}\n• GET /analysis/contract/{id}"]
    end

    subgraph SERVICES["4. Business Logic & Processing (app/service/)"]
        PARSER["document_parser.py\n(PyPDF2 & Text Extractor)"]
        PROMPT["prompt.py\n(Indian Contract Law Rules)"]
        AI_ENGINE["gemini_analyze.py\n(Google GenAI Interactions)"]
    end

    subgraph DATABASE["5. Database Layer (Docker Container)"]
        MONGO[("MongoDB Engine (:27017)\nDatabase: vakilvisiondb")]
        C_COLL[("contracts Collection\n(Unique filename index)")]
        A_COLL[("analysis Collection\n(analysis_id index)")]
        VOL[("mongodb_data Volume\n(Persistent Docker Storage)")]
        
        MONGO <--> VOL
        MONGO --> C_COLL
        MONGO --> A_COLL
    end

    subgraph AI_CLOUD["6. External AI Intelligence"]
        GEMINI["Google Gemini API\n(gemini-3.5-flash-lite)"]
    end

    %% Connections
    USER -->|HTTP Requests| FASTAPI
    FASTAPI --> C_ROUTE
    FASTAPI --> A_ROUTE
    
    C_ROUTE --> PARSER
    C_ROUTE --> C_COLL
    
    A_ROUTE --> C_COLL
    A_ROUTE --> AI_ENGINE
    A_ROUTE --> A_COLL
    
    AI_ENGINE --> PROMPT
    AI_ENGINE <-->|JSON Prompt / Analysis| GEMINI
```

---

## 🔄 3. End-to-End Execution Flow

Here is the exact lifecycle of how a contract is uploaded, parsed, analyzed by AI, and retrieved:

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client
    participant API as FastAPI (main.py)
    participant C_Route as contracts_routes.py
    participant Parser as document_parser.py
    participant DB as MongoDB (:27017)
    participant A_Route as analysis_routes.py
    participant AI as gemini_analyze.py
    participant Gemini as Google Gemini API

    %% Phase 1: Upload
    rect rgb(20, 35, 60)
        Note over User,DB: PHASE 1: CONTRACT UPLOAD & INGESTION
        User->>API: POST /contracts/upload (sample_nda.txt)
        API->>C_Route: upload_contract(file)
        C_Route->>Parser: extract_text(file_path)
        Parser-->>C_Route: {text, page_count, word_count}
        C_Route->>DB: contracts_collection.insert_one(Contract)
        DB-->>C_Route: Inserted ID: 6b094bb0b...
        C_Route-->>User: 200 OK { message: "Contract uploaded", contract_id: "6b094bb..." }
    end

    %% Phase 2: Analysis
    rect rgb(30, 45, 30)
        Note over User,Gemini: PHASE 2: AI ANALYSIS EXECUTION
        User->>API: POST /analysis/analys/6b094bb...
        API->>A_Route: analyse_contract(contract_id)
        A_Route->>DB: contracts.find_one({"_id": contract_id})
        DB-->>A_Route: Returns Contract text_content
        A_Route->>DB: contracts.update_one({"analysis_status": "in_progress"})
        
        A_Route->>AI: analyze_contract(contract_id, text_content)
        AI->>AI: Formats CONTRACT_ANALYSIS_PROMPT with contract text
        AI->>Gemini: client.interactions.create(model, input=prompt)
        Gemini-->>AI: Returns structured JSON (clauses, risk_flags, risk_level)
        AI-->>A_Route: Returns AnalysisResult (Pydantic model)
        
        A_Route->>DB: analysis_collection.insert_one(doc)
        A_Route->>DB: contracts.update_one({"analysis_status": "completed"})
        A_Route-->>User: 200 OK { message: "Analyzed successfully", analysis: {...} }
    end

    %% Phase 3: Auditing & Retrieval
    rect rgb(50, 30, 45)
        Note over User,DB: PHASE 3: AUDITING & QUERYING
        User->>API: GET /analysis/contract/6b094bb...
        API->>A_Route: get_analyses_for_contract(contract_id)
        A_Route->>DB: analysis.find({"contract_id": contract_id})
        DB-->>A_Route: Returns all historical analysis reports
        A_Route-->>User: 200 OK { analyses: [...], total: 1 }
    end
```

---

## 🛠️ 4. Tech Stack & Infrastructure

| Layer | Technology | Role | Details |
| :--- | :--- | :--- | :--- |
| **API Framework** | **FastAPI** | Web framework & routing | Asynchronous ASGI, automatic Swagger UI (`/docs`) |
| **Server** | **Uvicorn** | High-performance web server | Runs FastAPI application with live code reloading |
| **Database** | **MongoDB** (in Docker) | Document database | Stores unstructured contracts and nested analysis JSON |
| **Containerization**| **Docker Compose** | Database containerization | Runs `mongo:latest` with volume `mongodb_data` on `:27017` |
| **AI Intelligence** | **Google Gemini** | Legal reasoning LLM | Uses `google-genai` SDK (`gemini-3.5-flash-lite`) |
| **Data Validation** | **Pydantic v2** | Strict schema validation | `Contract`, `ClauseAnalysis`, `RiskFlag`, `AnalysisResult` |
| **File Parsing** | **PyPDF2 & Python I/O** | Document text extraction | Supports `.pdf` and `.txt` files up to 10 MB |

---

## 📂 5. Project Directory Structure

```text
Vakil-Contract-Vision/
├── .env.example               # Git-safe environment variable template
├── .gitignore                  # Blocks .env, uploads/, cache, and venvs from Git
├── docker-compose.yml          # Containerized MongoDB service configuration
├── README.md                   # Master project architecture & execution guide
├── sample/
│   └── sample_nda.txt          # Sample Non-Disclosure Agreement for testing
└── app/
    ├── .env                    # Private local credentials (MONGODB_URI, GEMINI_API_KEY)
    ├── .env.example            # App-level environment variable template
    ├── config.py               # Centralized configuration & environment loader
    ├── database.py             # MongoDB connection client & index creator
    ├── main.py                 # FastAPI application factory & router registration
    ├── models.py               # Pydantic schemas (Contract, Clause, RiskFlag, Analysis)
    ├── routes/
    │   ├── contracts_routes.py # Contract upload, listing, and file retrieval endpoints
    │   └── analysis_routes.py  # AI analysis trigger, report fetching, and querying
    ├── service/
    │   ├── document_parser.py  # Text extraction from PDF (PyPDF2) and TXT
    │   ├── gemini_analyze.py   # Google Gemini API interaction & JSON parsing
    │   └── prompt.py           # Specialized Indian Contract Law system prompts
    └── uploads/
        └── .gitkeep            # Upload directory (contract files are ignored by git)
```

---

## 🚀 6. How to Run the Entire Project (From Zero to Running)

### Step 1: Start the MongoDB Container
Open PowerShell in the root directory:
```powershell
cd C:\Users\ADMIN\Documents\hemant-python\Vakil-Contract-Vision
docker compose up -d
```
* **Verify:** Check container status with `docker ps` (Image: `mongo:latest`, Port: `0.0.0.0:27017->27017`).

---

### Step 2: Configure Environment Variables
Ensure [`app/.env`](app/.env) exists with your credentials:
```env
MONGODB_URI=mongodb://root:mypassword@localhost:27017
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### Step 3: Start the FastAPI Web Server
Navigate into the `app` folder and launch Uvicorn:
```powershell
cd C:\Users\ADMIN\Documents\hemant-python\Vakil-Contract-Vision\app
uvicorn main:app --reload
```
* **Server runs at:** `http://127.0.0.1:8000`
* **Interactive Swagger UI:** **`http://127.0.0.1:8000/docs`**

---

### Step 4: Test in Your Browser (Swagger UI)

1. Open **`http://127.0.0.1:8000/docs`**
2. **Upload Contract:** Go to `POST /contracts/upload` &rarr; upload `sample/sample_nda.txt` &rarr; copy the returned `contract_id`.
3. **Analyze with AI:** Go to `POST /analysis/analys/{contract_id}` &rarr; paste the `contract_id` &rarr; click **Execute**.
4. **View Legal Insights:** Gemini returns structured key clauses, risk flags (with references to Indian Contract Act Section 27), and negotiation counter-proposals!
5. **Query Reports:** Go to `GET /analysis/contract/{contract_id}` to retrieve historical reports.

---

## 📚 7. File-by-File Master Study Guides Roadmap

As we did in RAG-learning, we will create dedicated, line-by-line master guides for every single file in this project:

- [x] **File 0 (Master):** [`README.md`](README.md) &rarr; Full Architecture, Sequence Diagrams, Execution Protocol
- [x] **File 1:** [`docs/01_file_guide_docker_compose.md`](docs/01_file_guide_docker_compose.md) &rarr; MongoDB containerization, root credentials, volume persistence
- [x] **File 2:** [`docs/02_file_guide_config_py.md`](docs/02_file_guide_config_py.md) &rarr; Dynamic environment loading, upload restrictions, and secret management
- [x] **File 3:** [`docs/03_file_guide_database_py.md`](docs/03_file_guide_database_py.md) &rarr; PyMongo connection, database collections, and unique index creation
- [x] **File 4:** [`docs/04_file_guide_models_py.md`](docs/04_file_guide_models_py.md) &rarr; Pydantic v2 data modeling, Enums, and automatic ISO timestamp lifecycle
- [x] **File 5:** [`docs/05_file_guide_document_parser.py.md`](docs/05_file_guide_document_parser_py.md) &rarr; Document parsing, PyPDF2 page extraction, word counts
- [x] **File 6:** [`docs/06_file_guide_prompt_py.md`](docs/06_file_guide_prompt_py.md) &rarr; Prompt engineering for Indian Contract Law, JSON structuring
- [x] **File 7:** [`docs/07_file_guide_gemini_analyze_py.md`](docs/07_file_guide_gemini_analyze_py.md) &rarr; Google GenAI interactions, markdown-to-JSON cleaning
- [x] **File 8:** [`docs/08_file_guide_contracts_routes_py.md`](docs/08_file_guide_contracts_routes_py.md) &rarr; Multipart file upload, size checks, UUID naming
- [x] **File 9:** [`docs/09_file_guide_analysis_routes_py.md`](docs/09_file_guide_analysis_routes_py.md) &rarr; Analysis orchestration, ObjectId conversion, risk reporting
- [x] **File 10:** [`docs/10_file_guide_main_py.md`](docs/10_file_guide_main_py.md) &rarr; FastAPI application gateway, startup lifespan events, and router registration
