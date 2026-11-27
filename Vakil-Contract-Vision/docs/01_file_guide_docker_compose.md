# 🗄️ Deep-Dive Guide: `docker-compose.yml` (Vakil-Contract-Vision)

> **File:** [`docker-compose.yml`](file:///c:/Users/ADMIN/Documents/hemant-python/Vakil-Contract-Vision/docker-compose.yml)  
> **Role in Architecture:** Containerized database infrastructure provisioning the **MongoDB** persistence layer for contracts, metadata, and AI-generated legal analysis reports.

---

## 🧭 Navigation
- ⬅️ **Previous File:** [`README.md`](../README.md) &mdash; Project Purpose, Architecture & Execution Protocol
- ➡️ **Next File:** [`docs/02_file_guide_config_py.md`](02_file_guide_config_py.md) &mdash; Dynamic Environment Configuration & Settings

---

## 🎯 1. Why We Use It

When developing a production-grade legal AI engine, your database must meet three strict criteria:
1. **Reproducibility:** Any developer or CI/CD runner should spin up the exact same database engine in 5 seconds without installing multi-gigabyte MSI installers or configuring Windows background services.
2. **Isolation:** The database runtime, dependencies, network sockets, and file storage must remain sandboxed from the host operating system.
3. **Data Persistence:** Database records (contract documents, parsed clauses, extracted risks) must survive container restarts, system reboots, and container rebuilds.

`docker-compose.yml` solves all three problems by declaring our database infrastructure as **code** (*Infrastructure as Code - IaC*).

```mermaid
flowchart LR
    DEV["Developer / Terminal"] -->|docker compose up -d| ENGINE["Docker Engine"]
    
    subgraph DOCKER["Docker Host Sandboxed Environment"]
        CONT["Container: mongodb\n(mongo:latest)"]
        PORT["Container Port :27017"]
        VOL_MOUNT["Mount: /data/db"]
        
        CONT --- PORT
        CONT --- VOL_MOUNT
    end
    
    subgraph STORAGE["Persistent Host Storage"]
        DOCKER_VOL[("Named Volume:\nmongodb_data\n(WiredTiger Engine)")]
    end
    
    VOL_MOUNT <==>|Synchronous Disk I/O| DOCKER_VOL
    HOST_PORT["Windows Host :27017\n(localhost:27017)"] <==>|Port Forwarding| PORT
    FASTAPI["FastAPI App (app/main.py)\n(Running on Host)"] -->|PyMongo Client| HOST_PORT
```

---

## 🔍 2. Full Code & Line-by-Line Deep Dive

Here is the exact code of [`docker-compose.yml`](file:///c:/Users/ADMIN/Documents/hemant-python/Vakil-Contract-Vision/docker-compose.yml):

```yaml
services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - 27017:27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: mypassword
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

### Detailed Breakdown

#### Line 1: `services:`
* **What it does:** The root YAML key defining the compute containers managed by Docker Compose. Each child underneath represents an isolated service container.
* **Why it matters:** Docker Compose can coordinate dozens of interdependent microservices (e.g., database, redis cache, backend API, frontend UI, worker queues) under a single shared network namespace.

#### Line 2: `mongodb:`
* **What it does:** The logical service name within Docker Compose.
* **Why it matters:** If other containers exist inside this `docker-compose.yml` (for example, if our FastAPI app was also containerized), those containers could connect to MongoDB using the DNS hostname `mongodb:27017` over Docker's internal virtual bridge network.

#### Line 3: `image: mongo:latest`
* **What it does:** Instructs Docker Engine to pull the official MongoDB Community Edition Docker image from Docker Hub (`https://hub.docker.com/_/mongo`).
* **Why it matters:** Instead of compiling MongoDB from source or running an installer on Windows, Docker downloads an immutable, pre-compiled Linux container package containing the official `mongod` server binary, the WiredTiger storage engine, and all required shared libraries.
* **Production Best Practice:** While `latest` is great for rapid local prototyping, in strict enterprise production you should pin the exact version tag (e.g., `mongo:7.0.5`) to prevent unexpected database engine upgrades between minor releases.

#### Line 4: `container_name: mongodb`
* **What it does:** Gives the instantiated container a human-readable, static name (`mongodb`) instead of Docker's auto-generated default (`<directory>_<service>_<index>`, like `vakil-contract-vision_mongodb_1`).
* **Why it matters:** Makes debugging simple. You can immediately run:
  ```powershell
  docker logs -f mongodb
  docker exec -it mongodb mongosh -u root -p mypassword
  ```

#### Lines 5–6: `ports: - 27017:27017`
* **What it does:** Maps `[HOST_PORT]:[CONTAINER_PORT]`.
  * **Left side (`27017`):** Port opened on your Windows host machine (`localhost:27017` or `127.0.0.1:27017`).
  * **Right side (`27017`):** Port the MongoDB daemon listens on inside the container.
* **Why it matters:** Without this mapping, container ports are completely isolated within Docker's private bridge network. Because our FastAPI app runs directly on the Windows host (via `uvicorn main:app --reload`), FastAPI talks to MongoDB via the host port `localhost:27017`.

#### Lines 7–9: `environment:`
```yaml
environment:
  MONGO_INITDB_ROOT_USERNAME: root
  MONGO_INITDB_ROOT_PASSWORD: mypassword
```
* **What it does:** Passes environment variables into the container during its initialization.
* **Official MongoDB Image Hooks:**
  * `MONGO_INITDB_ROOT_USERNAME`: Creates a system-level administrative superuser when the container boots for the very first time.
  * `MONGO_INITDB_ROOT_PASSWORD`: Sets the superuser's password and automatically activates MongoDB role-based authentication (`--auth`).
* **Crucial Learning Point (The Error We Solved):**
  * In YAML, `environment` can be declared as a key-value dictionary (`KEY: value`) or a list (`- KEY=value`).
  * If you write `KEY= value` without the leading hyphen `-`, Docker Compose throws:
    `services.mongodb.environment must be a mapping`
  * Using `KEY: value` (with a space after `:`) ensures clean YAML dictionary parsing.

#### Lines 10–11: `volumes: - mongodb_data:/data/db`
* **What it does:** Binds Docker's named volume `mongodb_data` to MongoDB's internal data directory `/data/db`.
* **Why it matters:** Docker containers are **ephemeral** (stateless) by default. If a container stops, crashes, or is deleted, any data written to its local filesystem is permanently lost. By mounting `/data/db` to `mongodb_data`, MongoDB writes all B-trees, collection pages, and write-ahead transaction logs (WiredTiger journal) directly to a persistent storage volume managed by the Docker daemon on your host disk.

#### Lines 13–14: `volumes: mongodb_data:`
* **What it does:** Declares the named volume `mongodb_data` at top-level scope so Docker allocates and manages its lifecycle independently of container lifecycles.

---

## ⚡ 3. The Two Classic Pitfalls & How We Solved Them

### Pitfall A: YAML Syntax Error (`must be a mapping`)
* **What Happened:**
  ```yaml
  environment:
    MONGO_INITDB_ROOT_USERNAME= root # ❌ Syntax Error! Neither a mapping nor a list
  ```
* **The Root Cause:** In YAML, dictionaries use a colon `:`, while lists use `-`. Mixing `=` inside a dictionary confuses the YAML parser.
* **The Fix:**
  ```yaml
  environment:
    MONGO_INITDB_ROOT_USERNAME: root # ✅ Valid YAML mapping
    MONGO_INITDB_ROOT_PASSWORD: mypassword
  ```

---

### Pitfall B: Hostname Resolution Error (`[Errno 11001] getaddrinfo failed`)
* **What Happened:**
  When starting FastAPI with Uvicorn on Windows, the console crashed with:
  ```text
  pymongo.errors.ServerSelectionTimeoutError: mongodb:27017: [Errno 11001] getaddrinfo failed
  ```
* **The Root Cause:**
  * The user had `MONGODB_URI=mongodb://root:mypassword@mongodb:27017` in `app/.env`.
  * The hostname `mongodb` is an internal DNS name registered *only inside Docker's virtual network bridge*.
  * Uvicorn was running **directly on Windows** (outside Docker). Windows network DNS has no idea what `mongodb` is, so `getaddrinfo` fails.
* **The Rule to Remember:**
  * If FastAPI runs **on Windows Host**: use `localhost:27017` or `127.0.0.1:27017`.
  * If FastAPI runs **inside a Docker Container**: use service name `mongodb:27017`.

---

## ⚖️ 4. Alternative Approaches vs Docker Compose

| Approach | Setup Complexity | Reproducibility | Cleanliness (Uninstall) | Dev Experience | Production Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Docker Compose (Our Choice)** | ⭐⭐⭐⭐⭐ (1 file, 1 cmd) | 100% Deterministic | Instant (`docker rm`) | Highest | High |
| **Raw Docker CLI (`docker run`)** | ⭐⭐⭐ (Long messy flags) | Moderate (Needs bash script) | Clean | Error-prone typing | Medium |
| **Local Windows MSI Installer** | ⭐ (Heavy 500MB+ installer) | Low (Config drift across team) | Messy registry & files | Clutters OS | Low for local dev |
| **Cloud Managed (Atlas / AWS DocumentDB)** | ⭐⭐ (Account & VPC setup) | High | 100% Cloud-hosted | Needs constant internet & cost | Highest for Prod |

### Equivalent Raw Docker CLI Command
If you didn't have `docker-compose.yml`, you would have to remember and type this massive command every single time:
```powershell
docker volume create mongodb_data
docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=mypassword -v mongodb_data:/data/db mongo:latest
```
> **Advantage of Compose:** All flags, volumes, and ports are documented in a version-controlled YAML file committed to Git.

---

## 🧠 5. How to Permanently Remember It (Mental Analogies)

### Analogy 1: The Furnished Apartment & The Bank Vault (Container vs Volume)
* Think of the **Docker Container (`mongodb`)** as a *fully furnished rented apartment*. You can redecorate, tear down walls, or terminate your lease and leave at any time.
* Think of the **Named Volume (`mongodb_data`)** as an *external bank safe-deposit box*. 
* Even if the apartment is demolished or renovated, your valuables (your contracts and legal analysis reports in `/data/db`) stay completely safe in the bank vault. When you rent a new apartment next month, you simply reconnect it to the same vault!

### Analogy 2: The Universal Travel Plug Adapter (`ports: 27017:27017`)
* Inside the container, MongoDB is an appliance with a 27017 socket.
* The host port mapping is a universal travel adapter connecting the host machine's wall socket (`localhost:27017`) to the container's appliance socket (`:27017`).
* Any app running on your laptop plugs into the wall socket (`localhost:27017`) and electricity flows directly into MongoDB.

---

## 💼 6. Senior Technical Interview Battle Cards

### Q1: What is the exact difference between running `docker compose down` and `docker compose down -v`?
> **Answer:**  
> `docker compose down` stops the running containers, removes them, and deletes the default network, but **leaves all named volumes intact**. When you run `docker compose up -d` again, your database data is preserved.  
> However, adding the `-v` (or `--volumes`) flag tells Docker to also **permanently delete the associated named volumes** (`mongodb_data`). In our project, `docker compose down -v` would permanently erase all uploaded contracts and legal analysis history.

### Q2: Why did `mongodb:27017` cause `[Errno 11001] getaddrinfo failed` when running Uvicorn from PowerShell?
> **Answer:**  
> Docker Compose creates an isolated user-defined bridge network where containers can resolve each other using their service names as DNS hostnames.  
> However, because Uvicorn was executed directly in the host OS (PowerShell) outside the Docker bridge network, Windows used the local DNS resolver, which cannot resolve the private container service name `mongodb`. The host must connect to `localhost:27017` via the mapped host port.

### Q3: How does MongoDB guarantee data safety inside Docker across crashes?
> **Answer:**  
> MongoDB uses the **WiredTiger storage engine**. WiredTiger writes transactional changes to write-ahead log files (the journal) in `/data/db/journal`. Checkpoints occur by default every 60 seconds or after 2GB of data. Because `/data/db` is mounted to a Docker named volume backed by the host filesystem, if the container process crashes or Docker restarts, WiredTiger plays back the uncommitted journal logs upon boot and restores data to a fully consistent state.

### Q4: In production, why should you avoid using `image: mongo:latest` in Docker Compose?
> **Answer:**  
> The `latest` tag is mutable; it pulls whatever image is newest at the time of the pull. If a major release of MongoDB drops (e.g., v8.0 with breaking storage format or deprecated commands), running `docker compose pull` could download a version that fails to read older data files or breaks client driver compatibility. Production setups should always pin an exact minor or patch version (e.g., `image: mongo:7.0.12`).

---

## 🛠️ 7. Essential Docker Compose Cheat Sheet

| Task | Command |
| :--- | :--- |
| **Start MongoDB in background** | `docker compose up -d` |
| **Check running containers** | `docker compose ps` |
| **View live database logs** | `docker compose logs -f mongodb` |
| **Open MongoDB Shell inside container** | `docker exec -it mongodb mongosh -u root -p mypassword` |
| **Stop container (preserves data)** | `docker compose down` |
| **Stop and wipe all database data** | `docker compose down -v` *(Caution!)* |
| **Restart container** | `docker compose restart mongodb` |

---

## 🔗 Next Step
Proceed to **File 2**: [`docs/02_file_guide_config_py.md`](02_file_guide_config_py.md) to explore how application settings, environment variables, upload directories, and API keys are dynamically loaded and validated.
