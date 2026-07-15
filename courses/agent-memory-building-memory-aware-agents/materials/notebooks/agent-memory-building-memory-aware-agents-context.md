# Agent Memory: Building Memory-Aware Agents

---

## Lesson Map

- L2/L2.ipynb → Lesson 4: Scaling Agent Tool Use with Semantic Tool Memory
- L3/L3.ipynb → Lesson 5: Memory Operations: Extraction, Consolidation, and Self-Updating Memory
- L4/L4.ipynb → Lesson 6: Memory Aware Agent

---

## Lesson 4: Scaling Agent Tool Use with Semantic Tool Memory — L2/L2.ipynb

[markdown] cell 0

# L2: Constructing the Memory Manager

[markdown] cell 1

<div style="background-color:#fff6e4; padding:15px; border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"> <p>⏳ <b>Note <code>(Database Starting)</code>:</b> This notebook takes about 30-60 seconds to be ready to use. You may start and watch the video while you wait.</p>
<p>If you see <tt>Admin connection failed</tt> after running the first cell, simply wait and re-run — it is not a credentials issue.</p>
</div>

[markdown] cell 2

This lesson introduces the principle of structured memory for AI Agents, showing how different agent memory types require distinct data models, indexing strategies, and retrieval methods, all coordinated through a unified Memory Manager. By the end of this lesson, you will be able to design and implement persistent memory stores for core agent memory types, model memory data for efficient retrieval, and build a memory manager that orchestrates how agents store, retrieve, and operate on memory during execution.

In this lab, the running use case is an **agentic research assistant** that helps users investigate complex topics over multiple sessions. The assistant must remember prior findings, source credibility, and user preferences so it can deliver consistent, context-aware answers without repeating the same discovery work each time.

**Lesson Objectives**

By the end of this lesson you will you understand how to:
- Explain core agent memory types and their role in enabling reliable, long-running agentic systems.
- Design a persistent agent memory architecture, mapping memory types to appropriate storage backends (SQL tables and vector stores).
- Implement semantic memory using Oracle Vector Search, including embeddings, OracleVS configuration, HNSW indexing, and metadata filtering.
- Build a memory manager that orchestrates how agents store, retrieve, and update memory during execution.
- Evaluate memory design trade-offs, balancing retrieval accuracy, latency, cost, and agent reliability.



[markdown] cell 3

This section demonstrates how to use **LangChain's Oracle Vector Store (OracleVS)** to store and search documents using semantic similarity. 

Vector search enables finding documents based on meaning rather than exact keyword matches.

## What You'll Learn

| Step | Description |
|------|-------------|
| **1. Initialize Embeddings** | Load a HuggingFace embedding model to convert text into vectors |
| **2. Create Vector Store** | Set up an Oracle-backed vector store with distance strategy |
| **3. Create Index** | Build an HNSW index for fast similarity search |
| **4. Add Documents** | Store text with metadata in the vector database |
| **5. Query** | Search for similar documents using natural language |
| **6. Filter Results** | Use metadata filters to narrow down search results |

**Key Components**

- **`OracleVS`**: LangChain's Oracle vector store integration
- **`HuggingFaceEmbeddings`**: Converts text to 768-dimensional vectors
- **`DistanceStrategy.EUCLIDEAN_DISTANCE`**: Measures similarity between vectors
- **HNSW Index**: Speeds up similarity search with graph-based nearest-neighbor traversal


[markdown] cell 4

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b>Access <code>requirements.txt</code> and <code>helper.py</code> files:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em>.

<p> ⬇ &nbsp; <b>Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>

</div>

[markdown] cell 5

## Part 1: Setting Up Database, Vector Stores and Embedding Models

[code] cell 6

from helper import suppress_warnings

# Warning control
suppress_warnings()

from helper import load_env, setup_oracle_database, connect_to_oracle

load_env()

# One-time admin setup: configures tablespace, vector memory, and VECTOR user
setup_oracle_database()

# Connect as the VECTOR user for all subsequent operations
database_connection = connect_to_oracle(
    user="VECTOR",
    password="VectorPwd_2025",
    dsn="127.0.0.1:1521/FREEPDB1",
    program="devrel.deeplearning.course_1",
)

print("Using user:", database_connection.username)

[markdown] cell 7

### Loading the Embedding Model

[code] cell 8

from langchain_huggingface import HuggingFaceEmbeddings

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-mpnet-base-v2"
)

[markdown] cell 9

### Define Memory Tables and Stores
First, we define table names for each memory type. 

These tables will be created in Oracle Database to persist agent memory.

### Memory Types We'll Implement

| Memory Type | Human Analogy | Purpose | Storage | Retrieval Strategies Used |
|-------------|---------------|---------|---------|---------------------------|
| **Conversational** | Short-term memory | Chat history per thread | SQL Table | Exact match by thread_id |
| **Knowledge Base** | Long-term semantic memory | Facts, documents, search results | Vector Store | Semantic similarity search |
| **Workflow** | Procedural memory | Learned action patterns | Vector Store | Semantic similarity search + metadata filtering |
| **Toolbox** | Skill memory | Available tools & capabilities | Vector Store | Semantic similarity search |
| **Entity** | Episodic memory | People, places, systems mentioned | Vector Store | Semantic similarity search |
| **Summary** | Compressed memory | Condensed context for long conversations | Vector Store | Semantic similarity search (with optional ID filter) |
| **Tool Log** | Execution audit trail | Raw tool inputs/outputs and execution status | SQL Table | Exact match by thread_id + timestamp ordering |


[code] cell 10

# Table names for each memory type
CONVERSATIONAL_TABLE   = "CONVERSATIONAL_MEMORY" # Episodic memory
KNOWLEDGE_BASE_TABLE   = "SEMANTIC_MEMORY" # Semantic memory
WORKFLOW_TABLE = "WORKFLOW_MEMORY" # Procedural memory
TOOLBOX_TABLE    = "TOOLBOX_MEMORY" # Procedural memory
ENTITY_TABLE = "ENTITY_MEMORY" # Semantic memory
SUMMARY_TABLE = "SUMMARY_MEMORY" # Semantic memory
TOOL_LOG_TABLE = "TOOL_LOG_MEMORY" # Tool execution logs

ALL_TABLES = [
    CONVERSATIONAL_TABLE, 
    KNOWLEDGE_BASE_TABLE, 
    WORKFLOW_TABLE, 
    TOOLBOX_TABLE, 
    ENTITY_TABLE, 
    SUMMARY_TABLE, 
    TOOL_LOG_TABLE]

# Drop existing tables to start fresh
for table in ALL_TABLES:
    try:
        with database_connection.cursor() as cur:
            cur.execute(f"DROP TABLE {table} PURGE")
            print(f"  - {table} (dropped)")
    except Exception as e:
        if "ORA-00942" in str(e):
            print(f"  - {table} (not exists)")
        else:
            print(f"  ✗ {table}: {e}")
            
database_connection.commit()

[markdown] cell 11

### Create Conversational Memory Table

This function below creates a SQL table to store chat history. 

Unlike vector stores, conversational memory uses a traditional table because we need exact retrieval by thread ID (not similarity search).

**What it does:**
- Creates a table with columns: `id`, `thread_id`, `role`, `content`, `timestamp`, `metadata`
- Adds an index on `thread_id` for fast conversation lookups
- Adds an index on `timestamp` for chronological ordering


[code] cell 12

def create_conversational_history_table(conn, table_name: str = "CONVERSATIONAL_MEMORY"):
    """
    Create a table to store conversational history.

    Args:
        conn: Oracle database connection
        table_name: Name of the table to create
    """
    with conn.cursor() as cur:
        # Drop table if exists
        try:
            cur.execute(f"DROP TABLE {table_name}")
        except:
            pass  # Table doesn't exist
        
        # Create table with proper schema
        cur.execute(f"""
            CREATE TABLE {table_name} (
                id VARCHAR2(100) DEFAULT SYS_GUID() PRIMARY KEY,
                thread_id VARCHAR2(100) NOT NULL,
                role VARCHAR2(50) NOT NULL,
                content CLOB NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata CLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                summary_id VARCHAR2(100) DEFAULT NULL
            )
        """)
        
        # Create index on thread_id for faster lookups
        cur.execute(f"""
            CREATE INDEX idx_{table_name.lower()}_thread_id ON {table_name}(thread_id)
        """)
        
        # Create index on timestamp for ordering
        cur.execute(f"""
            CREATE INDEX idx_{table_name.lower()}_timestamp ON {table_name}(timestamp)
        """)
        
    conn.commit()
    print(f"Table {table_name} created successfully with indexes")
    return table_name


[code] cell 13

from helper import create_tool_log_table

# Create the SQL memory tables
CONVERSATION_HISTORY_TABLE = create_conversational_history_table(database_connection, CONVERSATIONAL_TABLE)
TOOL_LOG_HISTORY_TABLE = create_tool_log_table(database_connection, TOOL_LOG_TABLE)

[markdown] cell 14

### Create Vector Stores for Each Memory Type

Here we create 5 separate vector stores—one for each memory type. 

Each vector store is backed by its own Oracle table and uses the same embedding model for consistency.

| Vector Store | Purpose |
|--------------|---------|
| `knowledge_base_vs` | Store documents, facts, and search results |
| `workflow_vs` | Store learned action patterns and tool sequences |
| `toolbox_vs` | Store tool definitions for semantic tool discovery |
| `entity_vs` | Store extracted entities (people, places, systems) |
| `summary_vs` | Store compressed summaries for long conversations |


[code] cell 15

from langchain_oracledb.vectorstores import OracleVS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_oracledb.retrievers.hybrid_search import (
    OracleVectorizerPreference
)


class StoreManager:
    """Manages all stores (vector stores and SQL tables) with getter methods for easy access."""
    
    def __init__(self, client, embedding_function, table_names, distance_strategy, conversational_table, tool_log_table: str | None = None):
        """
        Initialize all stores.
        
        Args:
            client: Oracle database connection
            embedding_function: Embedding model to use
            table_names: Dict with keys: knowledge_base, workflow, toolbox, entity, summary
            distance_strategy: Distance strategy for vector search
            conversational_table: Name of the conversational history SQL table
            tool_log_table: Name of the SQL tool log table
        """
        self.client = client
        self.embedding_function = embedding_function
        self.distance_strategy = distance_strategy
        self._conversational_table = conversational_table
        self._tool_log_table = tool_log_table
        
        # Initialize all vector stores
        self._knowledge_base_vs = OracleVS(
            client=client,
            embedding_function=embedding_function,
            table_name=table_names['knowledge_base'],
            distance_strategy=distance_strategy,
        )
        
        self._workflow_vs = OracleVS(
            client=client,
            embedding_function=embedding_function,
            table_name=table_names['workflow'],
            distance_strategy=distance_strategy,
        )
        
        self._toolbox_vs = OracleVS(
            client=client,
            embedding_function=embedding_function,
            table_name=table_names['toolbox'],
            distance_strategy=distance_strategy,
        )
        
        self._entity_vs = OracleVS(
            client=client,
            embedding_function=embedding_function,
            table_name=table_names['entity'],
            distance_strategy=distance_strategy,
        )
        
        self._summary_vs = OracleVS(
            client=client,
            embedding_function=embedding_function,
            table_name=table_names['summary'],
            distance_strategy=distance_strategy,
        )
        
        # Store hybrid search preference for knowledge base (optional)
        self._kb_vectorizer_pref = None
    
    def get_knowledge_base_store(self):
        """Return the knowledge base vector store."""
        return self._knowledge_base_vs
    
    def get_workflow_store(self):
        """Return the workflow vector store."""
        return self._workflow_vs
    
    def get_toolbox_store(self):
        """Return the toolbox vector store."""
        return self._toolbox_vs
    
    def get_entity_store(self):
        """Return the entity vector store."""
        return self._entity_vs
    
    def get_summary_store(self):
        """Return the summary vector store."""
        return self._summary_vs
    
    def get_conversational_table(self):
        """Return the conversational history table name."""
        return self._conversational_table
    

    def get_tool_log_table(self):
        """Return the tool log table name."""
        return self._tool_log_table

    def setup_hybrid_search(self, preference_name="KB_VECTORIZER_PREF"):
        """
        Set up hybrid search for knowledge base.
        Creates vectorizer preference for hybrid indexing.
        """
        self._kb_vectorizer_pref = OracleVectorizerPreference.create_preference(
            vector_store=self._knowledge_base_vs,
            preference_name=preference_name
        )
        return self._kb_vectorizer_pref


[code] cell 16

# Create StoreManager instance
store_manager = StoreManager(
    client=database_connection,
    embedding_function=embedding_model,
    table_names={
        'knowledge_base': KNOWLEDGE_BASE_TABLE,
        'workflow': WORKFLOW_TABLE,
        'toolbox': TOOLBOX_TABLE,
        'entity': ENTITY_TABLE,
        'summary': SUMMARY_TABLE,
    },
    distance_strategy=DistanceStrategy.COSINE,
    conversational_table=CONVERSATION_HISTORY_TABLE,
    tool_log_table=TOOL_LOG_HISTORY_TABLE,
)

[code] cell 17

# Get all stores via the manager
conversation_table = store_manager.get_conversational_table()
knowledge_base_vs = store_manager.get_knowledge_base_store()
workflow_vs = store_manager.get_workflow_store()
toolbox_vs = store_manager.get_toolbox_store()
entity_vs = store_manager.get_entity_store()
summary_vs = store_manager.get_summary_store()
tool_log_table = store_manager.get_tool_log_table()

[code] cell 18

from helper import safe_create_index

print("Creating vector indexes...")
safe_create_index(database_connection, knowledge_base_vs, "knowledge_base_vs_ivf")
safe_create_index(database_connection, workflow_vs, "workflow_vs_ivf")
safe_create_index(database_connection, toolbox_vs, "toolbox_vs_ivf")
safe_create_index(database_connection, entity_vs, "entity_vs_ivf")
safe_create_index(database_connection, summary_vs, "summary_vs_ivf")
print("All indexes created!")

[markdown] cell 19

### Classification of Memory operation in Agentic Systems

[markdown] cell 20

A key design decision in memory engineering is determining which operations should be **Deterministic** (executed automatically by code) versus **Agent-Triggered** (decided by the LLM at runtime).

- A **deterministic** memory operation is one that runs based on system rules, not the model’s discretion. It is executed every time (or under clearly defined, non-negotiable conditions) so the system behaves predictably.
- An **agent-triggered** memory operation runs only when the model decides it’s necessary, based on intent and situation.

| Operation | Deterministic | Agent-Triggered |
|-----------|:------------:|:-------:|
| `read_conversational_memory()` | ✅ | ❌ |
| `read_knowledge_base()` | ✅ | ❌ |
| `read_workflow()` | ✅ | ❌ |
| `read_entity()` | ✅ | ❌ |
| `read_summary_context()` | ❌ | ✅ |
| `write_conversational_memory()` | ✅ | ❌ |
| `write_workflow()` | ✅ | ❌ |
| `write_entity()` | ❌ | ✅ |
| `search_tavily()` | ❌ | ✅ |
| `expand_summary()` | ❌ | ✅ |
| `summarize_and_store()` | ❌ | ✅ |
| `read_toolbox()` | ✅ | ✅ |


[markdown] cell 21

Deterministic memory operations run:
- **every turn**, or
- under **explicit, fixed conditions** (e.g., “always at the start of the agent loop”, “always after tool execution”)

### Why Deterministic Retrieval Is Useful
Memory retrieval is commonly run **at the start of each agent loop** because:

1. **Context bootstrapping is non-negotiable**
   - The agent needs prior context to remain consistent and avoid repeating mistakes.
   - Without deterministic retrieval, the agent behaves “stateless” and starts from scratch.

2. **The agent can’t choose to look up what it doesn’t know exists**
   - If the agent must decide whether to check memory, it must guess what’s stored.
   - This creates a chicken-and-egg problem: *you need memory to know which memory you need.*

3. **Predictability**
   - Always loading memory produces consistent behavior and makes the system easier to evaluate and debug.

### Why Deterministic Storage Is Useful
Persisting conversations, workflows, and entities is often deterministic because:

1. **Reliability**
   - You don’t want the agent to “forget to save” important information.
   - If continuity matters, persistence must be consistent.

2. **Completeness**
   - Every interaction should be recorded to avoid gaps.
   - Selective saving creates missing context that later breaks long-horizon tasks.

3. **Reduced cognitive load**
   - The model should focus on task execution, not memory bookkeeping.

### Advantages of Deterministic Memory Operations
- **Predictable behavior** across runs and turns
- **Stronger continuity** (fewer “stateless resets”)
- **Fewer missed memories** (higher reliability)
- **Easier debugging and evaluation** (clear expectations of what should be loaded/saved)


[markdown] cell 22

This is appropriate for memory actions that require judgment, such as:
- “Should this be saved as a durable preference?”
- “Should I consolidate/summarize now?”
- “Do I need deeper retrieval beyond the baseline preload?”
- “Should I strengthen, update, merge, or decay this memory?”

### Why Agent-Triggered Memory Operations Are Useful

1. **Relevance**
   - Not everything deserves long-term storage.
   - The agent can distinguish signal (preferences, decisions, constraints) from noise.

2. **Cost and latency control**
   - Deep retrieval, reranking, summarization, and consolidation cost tokens/time.
   - Triggering only when needed reduces overhead.

3. **Higher-quality memory management**
   - Decisions about *what to store* and *how to compress* require semantic understanding of intent.
   - The model is well-suited to decide when a memory action is worthwhile.

### Advantages of Agent-Triggered Memory Operations
- **Higher signal-to-noise memory** (less clutter)
- **Reduced memory bloat**
- **Selective compute usage** (summarize/expand/retrieve only when valuable)
- **More human-like remembering** (store/retrieve when it matters)

[markdown] cell 23

### How Tool Calls Fit In

External tool calls (e.g., web search, external DB lookups, expensive summarization jobs) are typically **agent-triggered** because:

1. **Intent matters**
   - Only the agent can judge whether extra information is needed.
   - Automatically using tools for every query is wasteful.

2. **Cost considerations**
   - Tools often introduce latency and may incur API costs.
   - The agent should call tools only when the expected value is high.

3. **Judgment required**
   - Choosing *what* to search for or *what* to expand requires understanding the user’s goal.

---

[markdown] cell 24

## Part 2: Memory Manager Initialization

[markdown] cell 25

The `MemoryManager` class is the central abstraction that unifies all memory operations. It provides a clean interface for reading and writing to different memory types, hiding the complexity of SQL queries and vector store operations. It is a single class that manages 7 types of memory with consistent read/write patterns:

| Memory Type | Storage | Write Method | Read Method |
|-------------|---------|--------------|-------------|
| **Conversational** | SQL Table | `write_conversational_memory()` | `read_conversational_memory()` |
| **Knowledge Base** | Vector Store | `write_knowledge_base()` | `read_knowledge_base()` |
| **Workflow** | Vector Store | `write_workflow()` | `read_workflow()` |
| **Toolbox** | Vector Store | `write_toolbox()` | `read_toolbox()` |
| **Entity** | Vector Store | `write_entity()` | `read_entity()` |
| **Summary** | Vector Store | `write_summary()` | `read_summary_memory()`, `read_summary_context()` |
| **Tool Log** | SQL Table | `write_tool_log()` | `read_tool_logs()` |


[code] cell 26

from helper import MemoryManager

# Initialize the MemoryManager instance
# Note: Uses SQL table for conversational memory, vector stores for others
memory_manager = MemoryManager(
    conn=database_connection,
    conversation_table=CONVERSATION_HISTORY_TABLE, 
    knowledge_base_vs=knowledge_base_vs,
    workflow_vs=workflow_vs,
    toolbox_vs=toolbox_vs,
    entity_vs=entity_vs,
    summary_vs=summary_vs,
    tool_log_table=TOOL_LOG_HISTORY_TABLE
)

[markdown] cell 27

## Part 3: Using The Memory Manager

[markdown] cell 28

Ingest the knowledge base for **ArxivScout** from HuggingFace by streaming arXiv paper records from the `nick007x/arxiv-papers dataset`.

[code] cell 29

from datasets import load_dataset
from itertools import islice

ds = load_dataset("nick007x/arxiv-papers", split="train", streaming=True)

[markdown] cell 30

extracting only the key fields (title, subjects, abstract, submission date, and arXiv ID), concatenating title + subjects + abstract into a single searchable text payload, and writing each entry into memory_manager.write_knowledge_base(...) with the extracted fields stored as metadata for filtering and attribution.

[code] cell 31

for paper in islice(ds, 100):
    # extract the key fields
    title = (paper.get("title") or "").strip()
    abstract = (paper.get("abstract") or "").strip()
    subjects = (paper.get("subjects") or paper.get("primary_subject") or "").strip()
    submission_date = (paper.get("submission_date") or "").strip()

    # skip empty records
    if not (title or abstract or subjects):
        continue

    # concatenate the key fields containing context for semantic search
    text = "\n".join([part for part in (title, subjects, abstract) if part])

    memory_manager.write_knowledge_base(
        text=text,
        metadata={
            "arxiv_id": paper.get("arxiv_id"),
            "title": title,
            "subjects": subjects,
            "abstract": abstract,
            "submission_date": submission_date,
        },
    )

[code] cell 32

results = memory_manager.read_knowledge_base(query="space exploration")
print(results)

---

## Lesson 5: Memory Operations: Extraction, Consolidation, and Self-Updating Memory — L3/L3.ipynb

[markdown] cell 0

# L3: Scaling Agent Tool Use with Semantic Tool Memory

[markdown] cell 1

<div style="background-color:#fff6e4; padding:15px; border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"> <p>⏳ <b>Note <code>(Database Starting)</code>:</b> This notebook takes about 30-60 seconds to be ready to use. You may start and watch the video while you wait.</p>
<p>If you see <tt>Admin connection failed</tt> after running the first cell, simply wait and re-run — it is not a credentials issue.</p>
</div>

[markdown] cell 2

### The Scalability Problem with Tools

As your AI system grows, you might have **hundreds of tools** available—APIs, database queries, calculators, search engines, and more. However, passing all tools to the LLM at inference time creates serious problems:

| Problem | Impact |
|---------|--------|
| **Context bloat** | Tool definitions consume tokens, leaving less room for actual content |
| **Tool selection failure** | LLMs struggle to choose the right tool when presented with too many options |
| **Increased latency** | More tokens = slower inference |
| **Higher costs** | More tokens = higher API costs |

Model providers like OpenAI and Anthropic typically recommend limiting the number of tools exposed to an LLM (often 10-20 max for reliable selection).

### The Solution: Semantic Tool Retrieval

The `Toolbox` class solves this by treating tools as a **searchable memory**:

1. **Register hundreds of tools** — Store all available tools with their descriptions and embeddings
2. **Retrieve only relevant tools** — At inference time, use vector search to find tools semantically relevant to the current query
3. **Pass a focused toolset** — Only the retrieved tools (typically 3-5) are passed to the LLM

This approach means your system can **scale to hundreds of tools** while the LLM only sees the most relevant ones for each query.

### How the Code Works

The `Toolbox` class uses **docstrings as the retrieval key**:

```
User Query → Embed Query → Vector Search → Find tools with similar docstrings → Return relevant tools
```

| Component | Purpose |
|-----------|---------|
| `Toolbox` (from `helper.py`) | Shared class used across lessons to register and retrieve tools |
| `ToolMetadata` (inside `helper.py`) | Stores tool name, description, signature, parameters |
| `_augment_docstring()` | Uses LLM to improve the docstring for better retrieval |
| `_generate_queries()` | Creates synthetic queries that would trigger this tool |
| `register_tool()` | Decorator that stores tool with its embedding in the toolbox |

When you call `memory_manager.read_toolbox(query)`, it performs a similarity search to find tools whose docstrings are semantically similar to the query.

[markdown] cell 3

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b>Access <code>requirements.txt</code> and <code>helper.py</code> files:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em>.

<p> ⬇ &nbsp; <b>Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>

</div>

[markdown] cell 4

## Part 0: Connect to Database

[markdown] cell 5

### Step 1: Create a Live Database Session

The next cell verifies Docker, starts Oracle if needed, and prepares the database user/schema for vector operations.
Think of this as infrastructure bootstrapping before any agent memory logic runs. Now we open a connection object that every memory component will share.
This connection is the backbone for both SQL memory (conversation history) and vector memory stores.

[code] cell 6

from helper import suppress_warnings

# Warning control
suppress_warnings()

from helper import load_env, setup_oracle_database, connect_to_oracle

load_env()

# One-time admin setup: configures tablespace, vector memory, and VECTOR user
setup_oracle_database()

# Connect as the VECTOR user for all subsequent operations
database_connection = connect_to_oracle(
    user="VECTOR",
    password="VectorPwd_2025",
    dsn="127.0.0.1:1521/FREEPDB1",
    program="devrel.deeplearning.course_1",
)

print("Using user:", database_connection.username)

[markdown] cell 7

## Part 1: Loading Embedding Model

[code] cell 8

from langchain_community.embeddings import HuggingFaceEmbeddings
# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-mpnet-base-v2"
)

[markdown] cell 9

### Why Embeddings Matter for Tool Use

In the next steps, the `Toolbox` uses embeddings to map natural-language queries to the most relevant tools.
This means tool retrieval is semantic: the agent can discover capabilities even when the query wording does not exactly match a tool name.

[markdown] cell 10

### Loading Models, StoreManagers and MemoryManagers

[markdown] cell 11

### Bring in the LLM Runtime

Before we can augment tool metadata or run agent decisions, we initialize the OpenAI client used by the toolbox and later agent loops.

[code] cell 12

from openai import OpenAI

client = OpenAI()

[markdown] cell 13

### Define Memory Store Names

The next cell standardizes table names for each memory type.
Naming each store explicitly makes debugging and lesson-to-lesson continuity much easier for AI system builders.

[code] cell 14

# Table names for each memory type
CONVERSATIONAL_TABLE = "CONVERSATIONAL_MEMORY"
KNOWLEDGE_BASE_TABLE = "SEMANTIC_MEMORY"
WORKFLOW_TABLE = "WORKFLOW_MEMORY"
TOOLBOX_TABLE = "TOOLBOX_MEMORY"
ENTITY_TABLE = "ENTITY_MEMORY"
SUMMARY_TABLE = "SUMMARY_MEMORY"
TOOL_LOG_TABLE = "TOOL_LOG_MEMORY"

[markdown] cell 15

### Clean Slate: Drop Existing Tables

<p style="background-color:#ff9a94; padding:15px; border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"> ⏳ <b>Note:</b> To ensure this lesson runs correctly regardless of whether previous lessons have been executed, we drop all memory tables before recreating them by running the cell below. This guarantees a clean starting state with consistent distance strategy and no stale data for the lesson.</p>



[code] cell 16

ALL_TABLES = [
    CONVERSATIONAL_TABLE,
    KNOWLEDGE_BASE_TABLE,
    WORKFLOW_TABLE,
    TOOLBOX_TABLE,
    ENTITY_TABLE,
    SUMMARY_TABLE,
    TOOL_LOG_TABLE]

# Drop existing tables to start fresh
for table in ALL_TABLES:
    try:
        with database_connection.cursor() as cur:
            cur.execute(f"DROP TABLE {table} PURGE")
            print(f"  - {table} (dropped)")
    except Exception as e:
        if "ORA-00942" in str(e):
            print(f"  - {table} (not exists)")
        else:
            print(f"  ✗ {table}: {e}")

database_connection.commit()

[markdown] cell 17

### Provision the Conversation Table

This step ensures the SQL table for conversational memory exists.
Conversation memory is your short-horizon thread history and anchors dialogue continuity.

[code] cell 18

# Create or retrieve the conversational history table
from helper import create_conversational_history_table, create_tool_log_table

CONVERSATION_HISTORY_TABLE = create_conversational_history_table(database_connection, CONVERSATIONAL_TABLE)
TOOL_LOG_HISTORY_TABLE = create_tool_log_table(database_connection, TOOL_LOG_TABLE)


[markdown] cell 19

### Build the Vector Store Layer via `StoreManager`

The following cell wires each vector memory store (knowledge, workflow, toolbox, entity, summary) through a single manager.
This gives you clean getters instead of scattered setup logic.

[code] cell 20

from langchain_oracledb.vectorstores import OracleVS
from langchain_community.vectorstores.utils import DistanceStrategy
from helper import StoreManager

# Create StoreManager instance
store_manager = StoreManager(
    client=database_connection,
    embedding_function=embedding_model,
    table_names={
        'knowledge_base': KNOWLEDGE_BASE_TABLE,
        'workflow': WORKFLOW_TABLE,
        'toolbox': TOOLBOX_TABLE,
        'entity': ENTITY_TABLE,
        'summary': SUMMARY_TABLE,
    },
    distance_strategy=DistanceStrategy.COSINE,
    conversational_table=CONVERSATION_HISTORY_TABLE,
    tool_log_table=TOOL_LOG_HISTORY_TABLE,
)

# Get all stores via the manager
conversation_table = store_manager.get_conversational_table()
knowledge_base_vs = store_manager.get_knowledge_base_store()
workflow_vs = store_manager.get_workflow_store()
toolbox_vs = store_manager.get_toolbox_store()
entity_vs = store_manager.get_entity_store()
summary_vs = store_manager.get_summary_store()
tool_log_table = store_manager.get_tool_log_table()

print("✅ All stores loaded via StoreManager")

[markdown] cell 21

### Initialize Memory Orchestration + Toolbox Instance

Now we compose the runtime: `MemoryManager` unifies read/write access across all memory stores, and `Toolbox` registers/retrieves tools semantically.
We still initialize a concrete `toolbox` instance here so tools can be registered in this notebook.

[code] cell 22

from helper import MemoryManager, Toolbox

# Initialize the MemoryManager instance
memory_manager = MemoryManager(
    conn=database_connection,
    conversation_table=conversation_table,
    knowledge_base_vs=knowledge_base_vs,
    workflow_vs=workflow_vs,
    toolbox_vs=toolbox_vs,
    entity_vs=entity_vs,
    summary_vs=summary_vs,
    tool_log_table=TOOL_LOG_HISTORY_TABLE
)

# Initialize Toolbox
toolbox = Toolbox(memory_manager, client, embedding_model)

print("✅ MemoryManager and Toolbox initialized")

[markdown] cell 23

## Tools Overview

The following tools are created and registered with the Toolbox in this lesson:

| Tool | Purpose |
|------|---------|
| `search_tavily` | Searches the web using Tavily API and persists results to the knowledge base for future retrieval |
| `get_current_time` | Returns the current date and time (with optional detailed format including microseconds) |
| `arxiv_search_candidates` | Searches arXiv for papers matching a query and returns metadata (IDs, titles, authors, abstracts) |
| `fetch_and_save_paper_to_kb_db` | Downloads an arXiv paper PDF, extracts text, chunks it, and stores in the knowledge base |

Each tool is registered using `@toolbox.register_tool()` which stores its embedding for semantic retrieval. When the agent receives a query, only the most relevant tools are retrieved and passed to the LLM.

[markdown] cell 24

>We expose toolbox retrieval as both a programmatic operation and an agent-callable skill. This allows the agent to autonomously query for tools mid-execution when it needs capabilities beyond those initially provided.

[code] cell 25

@toolbox.register_tool(augment=True)
def read_toolbox(query: str, k: int = 3) -> list[str]:
    """
    Search the toolbox for functions that can help solve a problem or complete a task.
    
    Use this tool when:
    - You encounter an error or unexpected output and need a different approach
    - The currently available tools don't seem sufficient for the task
    - You need to discover what capabilities are available for a specific problem
    - You want to find alternative functions that might handle edge cases better
    
    Args:
        query: A natural language description of what you're trying to accomplish
               or the problem you're trying to solve. Be specific about the task
               or error you're encountering for better results.
        k: Number of relevant tools to return (default: 5)
    
    Returns:
        A list of tool definitions that semantically match your query,
        including their names, descriptions, and parameter schemas.
    
    Example queries:
        - "search for academic papers on machine learning"
        - "fetch and store document content"
        - "get the current date and time"
        - "summarize long text and save to memory"
    """
    return memory_manager.read_toolbox(query, k=k)

[markdown] cell 26

## Part 2: Web Access with Tavily

[markdown] cell 27

This section demonstrates how to create an **agentic tool** that the LLM can call to search the web. 

We use [Tavily](https://tavily.com/), an AI-optimized search API designed for LLM applications.

What This Section Does

1. **Initialize the Tavily client** — Set up the search API with an API key
2. **Register `search_tavily` as a tool** — Use `@toolbox.register_tool(augment=True)` to make it discoverable
3. **Implement the search-and-store pattern** — Results are automatically written to knowledge base memory
4. **Test tool retrieval** — Verify the tool can be found via semantic search

[markdown] cell 28

### The Search-and-Store Pattern

One thing to note is that not only do we get external context that is not available to the Agent at execution, but we persists this to the knowledge base memory and the Agent can reuse this information in subsequent iteration.
When the agent calls `search_tavily()`, it doesn't just return results—it **persists them to the knowledge base**:

```
Agent calls search_tavily("latest AI news")
       ↓
Tavily API returns results
       ↓
Each result is written to knowledge_base_vs with metadata (title, URL, timestamp)
       ↓
Future queries can retrieve this information without searching again
```

This pattern means the agent **learns** from its searches. Information discovered once becomes part of the agent's long-term memory, available for future conversations without additional API calls.

[code] cell 29

from tavily import TavilyClient
from datetime import datetime

tavily_client = TavilyClient()

@toolbox.register_tool(augment=True)
def search_tavily(query: str, max_results: int = 5):
    """
    Use this function to search the web and store the results in the knowledge base.
    """
    response = tavily_client.search(query=query, max_results=max_results)
    results = response.get("results", [])

    # Write each result to the knowledge base
    for result in results:
        # Create the text content to embed
        text = f"Title: {result.get('title', '')}\nContent: {result.get('content', '')}\nURL: {result.get('url', '')}"
        
        # Create metadata
        metadata = {
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "score": result.get("score", 0),
            "source_type": "tavily_search",
            "query": query,
            "timestamp": datetime.now().isoformat()
        }
        
        # Write to knowledge base
        memory_manager.write_knowledge_base(text, metadata)

    return results

[markdown] cell 30

### Augmented vs. Original Docstrings

When `augment=True`, the `Toolbox` sends both the **original docstring** and the **function's source code** to an LLM, which produces a richer, more detailed description. This enriched text is what gets embedded and stored — improving semantic separability and retrieval recall.

Let's compare the **original** one-line docstring for `search_tavily` with the **augmented** version the LLM produced by analyzing the code:

[code] cell 31

import inspect

# Original docstring (what the developer wrote - just one line)
original = ("Use this function to search the web"
            " and store the results in the"
            " knowledge base.")

# Get the actual source code of the function
fn = toolbox._tools_by_name["search_tavily"]
source = inspect.getsource(fn)

print("ORIGINAL DOCSTRING:")
print(f'  "{original}"')
print()

# The LLM reads both the docstring AND the source code
augmented = toolbox._augment_docstring(original, source)

print("AUGMENTED DOCSTRING (LLM-enhanced):")
print(f"  {augmented}")

[markdown] cell 32

### Add a Simple Utility Tool First

Before advanced retrieval tools, we register a deterministic utility (`get_current_time`).
This is a good pedagogical pattern: validate tool registration on a low-risk function first.

[code] cell 33

from datetime import datetime

@toolbox.register_tool(augment=True)
def get_current_time(detailed: bool = False) -> str:
    """
    Returns the current time.
    
    Args:
        detailed: If True, returns detailed format with microseconds
    
    Returns:
        str: Current time as formatted string
    """
    if detailed:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

[markdown] cell 34

### Configure Candidate Retrieval from arXiv

The next cell sets up a lightweight retriever for paper candidates (title, abstract, metadata) rather than full PDFs.
This supports fast discovery before expensive ingestion.

[code] cell 35

from langchain_community.retrievers import ArxivRetriever

arxiv_retriever = ArxivRetriever(
    load_max_docs=8,
    get_full_documents=False,
    doc_content_chars_max=4000
)

[markdown] cell 36

### Register an arXiv Discovery Tool

This section adds `arxiv_search_candidates`, which returns structured JSON candidates the agent can reason over before selecting a paper to ingest.

[code] cell 37

import json
from urllib.parse import urlparse

def _arxiv_id_from_entry_id(entry_id: str) -> str:
    """
    Convert 'http://arxiv.org/abs/2310.08560v2' -> '2310.08560v2'
    """
    if not entry_id:
        return ""
    path = urlparse(entry_id).path  # e.g. '/abs/2310.08560v2'
    return path.split("/abs/")[-1].strip("/")

@toolbox.register_tool(augment=False)
def arxiv_search_candidates(query: str, k: int = 5) -> str:
    """
    Search arXiv and return a JSON list of candidate papers with IDs + metadata.

    Output schema (JSON string):
    [
      {
        "arxiv_id": "2310.08560v2",
        "entry_id": "http://arxiv.org/abs/2310.08560v2",
        "title": "...",
        "authors": "...",
        "published": "2024-02-12",
        "abstract": "..."
      },
      ...
    ]
    """
    docs = arxiv_retriever.invoke(query)
    candidates = []
    for d in (docs or [])[:k]:
        meta = d.metadata or {}
        entry_id = meta.get("Entry ID", "")
        candidates.append({
            "arxiv_id": _arxiv_id_from_entry_id(entry_id),
            "entry_id": entry_id,
            "title": meta.get("Title", ""),
            "authors": meta.get("Authors", ""),
            "published": str(meta.get("Published", "")),
            "abstract": (d.page_content or "")[:2500],
        })
    return json.dumps(candidates, ensure_ascii=False, indent=2)

[markdown] cell 38

### Register Deep Ingestion: Fetch, Chunk, and Persist

Next we define a heavier tool that downloads full paper text, chunks it for embedding limits, and stores it in knowledge-base memory.
This demonstrates a production-grade pattern: move large payload handling out of the model context and into memory infrastructure.

[code] cell 39

from datetime import timezone
from langchain_community.document_loaders import ArxivLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


@toolbox.register_tool(augment=True)
def fetch_and_save_paper_to_kb_db(
    arxiv_id: str,
    chunk_size: int = 1500,
    chunk_overlap: int = 200,
) -> str:
    """
    Fetch full arXiv paper text (PDF -> text) and store it into the OracleVS
    knowledge base table as chunked records (avoids routing full content via the LLM).

    """

    # 1) Load full paper text from arXiv (PDF -> text)
    loader = ArxivLoader(
        query=arxiv_id,
        load_max_docs=1,
        doc_content_chars_max=None,  # "no truncation" in current LangChain docs :contentReference[oaicite:1]{index=1}
    )
    docs = loader.load()
    if not docs:
        return f"No documents found for arXiv id: {arxiv_id}"

    doc = docs[0]

    title = (
        doc.metadata.get("Title")
        or doc.metadata.get("title")
        or f"arXiv {arxiv_id}"
    )

    # Normalize common arxiv metadata keys
    entry_id = doc.metadata.get("Entry ID") or doc.metadata.get("entry_id") or ""
    published = doc.metadata.get("Published") or doc.metadata.get("published") or ""
    authors = doc.metadata.get("Authors") or doc.metadata.get("authors") or ""

    full_text = doc.page_content or ""
    if not full_text.strip():
        return f"Loaded arXiv {arxiv_id} but extracted empty text (PDF parsing issue)."

    # 2) Chunk (important: embeddings have input limits; chunking prevents failures/truncation)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    
    chunks = splitter.split_text(full_text)

    # 3) Store chunks into OracleVS (vector store table)
    ts_utc = datetime.now(timezone.utc).isoformat()
    metadatas = []
    for i in range(len(chunks)):
        metadatas.append(
            {
                "source": "arxiv",
                "arxiv_id": arxiv_id,
                "title": title,
                "entry_id": entry_id,
                "published": str(published),
                "authors": str(authors),
                "chunk_id": i,
                "num_chunks": len(chunks),
                "ingested_ts_utc": ts_utc,
            }
        )

    memory_manager.write_knowledge_base(chunks, metadatas)

    return (
        f"Saved arXiv {arxiv_id} to {KNOWLEDGE_BASE_TABLE}: "
        f"{len(chunks)} chunks (title: {title})."
    )


[markdown] cell 40

### Validate Semantic Tool Retrieval

Finally, we issue a natural-language query against toolbox memory to verify retrieval quality.
If this works, your agent can dynamically narrow tool choices at runtime instead of loading everything into prompt context.

[code] cell 41

import pprint
retrieved_tools = memory_manager.read_toolbox("Get more details on a paper on AI", k=1)
pprint.pprint(retrieved_tools)

---

## Lesson 6: Memory Aware Agent — L4/L4.ipynb

[markdown] cell 0

# L4: Memory Operations: Extraction, Consolidation, and Self-Updating Memory

[markdown] cell 1

<div style="background-color:#fff6e4; padding:15px; border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"> <p>⏳ <b>Note <code>(Database Starting)</code>:</b> This notebook takes about 30-60 seconds to be ready to use. You may start and watch the video while you wait.</p>
<p>If you see <tt>Admin connection failed</tt> after running the first cell, simply wait and re-run — it is not a credentials issue.</p>
</div>

[markdown] cell 2

This lesson explores advanced memory operations that enable AI agents to manage long-running conversations efficiently. As conversations grow, they consume valuable context window space. Without proper management, agents lose important historical context or fail due to token limits.

**Lesson Objectives**

By the end of this lesson, you will understand how to:
- Monitor context window utilization and detect when summarization is needed
- Extract and consolidate conversation history into structured summaries
- Implement self-updating memory that preserves technical details, emotional context, and entity information
- Build tools that allow agents to expand summaries back to original conversations when needed

**Key Concepts**

| Concept | Description |
|---------|-------------|
| **Context Window Management** | Tracking token usage to prevent overflow and trigger timely summarization |
| **Memory Consolidation** | Compressing verbose conversations into structured summaries while preserving critical information |
| **Summary Expansion** | Retrieving original conversation content from summary references when detail is needed |
| **Self-Updating Memory** | Automatic marking of summarized messages to prevent re-processing |

[markdown] cell 3

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b>Access <code>requirements.txt</code> and <code>helper.py</code> files:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em>.

<p> ⬇ &nbsp; <b>Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>

</div>

[markdown] cell 4

## Part 1: Setup and Configuration

This section establishes the foundational infrastructure needed for memory operations.

### What We're Setting Up

| Component | Purpose |
|-----------|---------|
| **Database Connection** | Oracle Database stores all memory persistently |
| **Embedding Model** | Converts text to vectors for semantic search |
| **Memory Stores** | Separate vector stores for different memory types |
| **MemoryManager** | Unified interface for all memory operations |

### Database Connection

[markdown] cell 5

<!-- edu-bridge:2f7cb99e -->
### Oracle Bootstrap

Oracle setup runs first to verify the database runtime is ready for memory operations. It establishes the infrastructure foundation that every later step depends on.

[markdown] cell 6

<!-- edu-bridge:b0119a96 -->
### Connection Session

A live Oracle connection is created here and shared across all memory components. With infrastructure ready from the previous step, this turns setup into an active session.

[code] cell 7

from helper import suppress_warnings

# Warning control
suppress_warnings()

from helper import load_env, setup_oracle_database, connect_to_oracle

load_env()

# One-time admin setup: configures tablespace, vector memory, and VECTOR user
setup_oracle_database()

# Connect as the VECTOR user for all subsequent operations
database_connection = connect_to_oracle(
    user="VECTOR",
    password="VectorPwd_2025",
    dsn="127.0.0.1:1521/FREEPDB1",
    program="devrel.deeplearning.course_1",
)

print("Using user:", database_connection.username)

[markdown] cell 8

### Models and Embedding

[markdown] cell 9

<!-- edu-bridge:3282ebc3 -->
### LLM And Embeddings

The OpenAI client and embedding model are initialized to power summarization and vector retrieval. After database connectivity, this adds the model-side capabilities for memory intelligence.

[code] cell 10

from openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings

client = OpenAI()

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-mpnet-base-v2"
)

[markdown] cell 11

### Memory Stores and Managers

[markdown] cell 12

<!-- edu-bridge:9add47ef -->
### Memory Table Names

Canonical names are defined for each memory store so setup and queries stay consistent. This prepares the storage schema used throughout the notebook.

[code] cell 13

# Table names for each memory type
CONVERSATIONAL_TABLE = "CONVERSATIONAL_MEMORY"
KNOWLEDGE_BASE_TABLE = "SEMANTIC_MEMORY"
WORKFLOW_TABLE = "WORKFLOW_MEMORY"
TOOLBOX_TABLE = "TOOLBOX_MEMORY"
ENTITY_TABLE = "ENTITY_MEMORY"
SUMMARY_TABLE = "SUMMARY_MEMORY"
TOOL_LOG_TABLE = "TOOL_LOG_MEMORY"

[markdown] cell 14

### Clean Slate: Drop Existing Tables

<p style="background-color:#ff9a94; padding:15px; border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"> ⏳ <b>Note:</b> To ensure this lesson runs correctly regardless of whether previous lessons have been executed, we drop all memory tables before recreating them by running the cell below. This guarantees a clean starting state with consistent distance strategy and no stale data for the lesson.</p>

[code] cell 15

ALL_TABLES = [
    CONVERSATIONAL_TABLE,
    KNOWLEDGE_BASE_TABLE,
    WORKFLOW_TABLE,
    TOOLBOX_TABLE,
    ENTITY_TABLE,
    SUMMARY_TABLE,
    TOOL_LOG_TABLE]

# Drop existing tables to start fresh
for table in ALL_TABLES:
    try:
        with database_connection.cursor() as cur:
            cur.execute(f"DROP TABLE {table} PURGE")
            print(f"  - {table} (dropped)")
    except Exception as e:
        if "ORA-00942" in str(e):
            print(f"  - {table} (not exists)")
        else:
            print(f"  ✗ {table}: {e}")

database_connection.commit()

[markdown] cell 16

<!-- edu-bridge:39b83051 -->
### Conversation Table Setup

The conversational SQL table is created or reused for thread-level message persistence. It applies the naming decisions from the previous step to a concrete memory component.

[code] cell 17

# Create or retrieve the conversational history table
from helper import create_conversational_history_table, create_tool_log_table
CONVERSATION_HISTORY_TABLE = create_conversational_history_table(database_connection, CONVERSATIONAL_TABLE)
TOOL_LOG_HISTORY_TABLE = create_tool_log_table(database_connection, TOOL_LOG_TABLE)


[markdown] cell 18

<!-- edu-bridge:35a5c92e -->
### Store Manager Wiring

Vector stores are wired through `StoreManager`, then handles are retrieved for downstream use. The storage layer now expands from conversation memory into multi-memory support.

[code] cell 19

from langchain_oracledb.vectorstores import OracleVS
from langchain_community.vectorstores.utils import DistanceStrategy
from helper import StoreManager

# Create StoreManager instance
store_manager = StoreManager(
    client=database_connection,
    embedding_function=embedding_model,
    table_names={
        'knowledge_base': KNOWLEDGE_BASE_TABLE,
        'workflow': WORKFLOW_TABLE,
        'toolbox': TOOLBOX_TABLE,
        'entity': ENTITY_TABLE,
        'summary': SUMMARY_TABLE,
    },
    distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE,
    conversational_table=CONVERSATION_HISTORY_TABLE,
    tool_log_table=TOOL_LOG_HISTORY_TABLE,
)

# Get all stores via the manager
conversation_table = store_manager.get_conversational_table()
knowledge_base_vs = store_manager.get_knowledge_base_store()
workflow_vs = store_manager.get_workflow_store()
toolbox_vs = store_manager.get_toolbox_store()
entity_vs = store_manager.get_entity_store()
summary_vs = store_manager.get_summary_store()
tool_log_table = store_manager.get_tool_log_table()

print("✅ All stores loaded via StoreManager")

[markdown] cell 20

<!-- edu-bridge:0c3f0546 -->
### Memory Runtime Assembly

`MemoryManager` and `Toolbox` are composed into the working runtime. Raw stores from the prior step become high-level operations the agent can call consistently.

[code] cell 21

from helper import MemoryManager, Toolbox

# Initialize the MemoryManager instance
memory_manager = MemoryManager(
    conn=database_connection,
    conversation_table=conversation_table,
    knowledge_base_vs=knowledge_base_vs,
    workflow_vs=workflow_vs,
    toolbox_vs=toolbox_vs,
    entity_vs=entity_vs,
    summary_vs=summary_vs,
    tool_log_table=TOOL_LOG_HISTORY_TABLE
)

# Initialize Toolbox with embedding function
toolbox = Toolbox(memory_manager, client, embedding_model)

print("✅ MemoryManager and Toolbox initialized")

[markdown] cell 22

**Part 1 Takeaway:** We now have a complete infrastructure with database connectivity, embedding capabilities, and organized memory stores. The `MemoryManager` provides a clean interface to read/write different memory types, while the `Toolbox` allows us to register functions that the agent can discover and call.

---

## Part 2: Context Window Management and Summarization

Large Language Models have finite context windows. When conversations grow long, we face a critical challenge: how do we preserve important information while staying within token limits?

This section implements the core memory consolidation pipeline:

```
Long Conversation → Monitor Usage → Summarize → Store Summary → Mark Original as Processed
```

### Why This Matters

| Problem | Solution |
|---------|----------|
| Context overflow crashes the agent | Monitor token usage and summarize proactively |
| Summaries lose important details | Capture technical, emotional, and entity information |
| Can't access original conversation | Store summary ID links back to original messages |
| Re-summarizing already processed messages | Mark messages with summary_id after processing |

### Token Counting and Monitoring

[markdown] cell 23

<!-- edu-bridge:c16580e7 -->
### Token Budget Definition

Model context limits are declared to frame when compaction should occur. This starts the transition from setup to context-window management.

[code] cell 24

# Model token limits (for context management)
MODEL_TOKEN_LIMITS = {
    "gpt-5-mini": 256000,
}

[markdown] cell 25

<!-- edu-bridge:3c626cd9 -->
### Usage Calculator

A usage estimator converts context length into token utilization percentage. It relies on the token budget above and provides the trigger signal for summarization.

[code] cell 26

# Context window calculator - returns percentage used
def calculate_context_usage(context: str, model: str = "gpt-5-mini") -> dict:
    """Calculate context window usage as percentage."""
    estimated_tokens = len(context) // 4  # ~4 chars per token
    max_tokens = MODEL_TOKEN_LIMITS.get(model, 128000)
    percentage = (estimated_tokens / max_tokens) * 100
    return {"tokens": estimated_tokens, "max": max_tokens, "percent": round(percentage, 1)}


[markdown] cell 27

### Summarization Functions

The summarization pipeline captures four types of information:
1. **Technical Information** — Facts, code, configurations, solutions
2. **Emotional Context** — Tone, sentiment, urgency levels
3. **Entities & References** — People, systems, projects mentioned
4. **Action Items & Decisions** — Next steps, agreements, pending tasks

[markdown] cell 28

<!-- edu-bridge:758e267b -->
### Summary Generation Function

Summary generation is defined with parsing and fallback behavior for robust outputs. This is the core compaction mechanism used when context becomes too large.

[code] cell 29

import uuid

def summarise_context_window(content: str, memory_manager, llm_client, model: str = "gpt-5-mini") -> dict:
    """
    Summarise content using an LLM and store in summary memory.
    """
    cleaned = (content or "").strip()
    if not cleaned:
        return {"status": "nothing_to_summarize"}

    def _message_text(resp) -> str:
        msg = resp.choices[0].message
        payload = getattr(msg, "content", None)
        if isinstance(payload, str):
            return payload.strip()
        if isinstance(payload, list):
            parts = []
            for item in payload:
                if isinstance(item, dict):
                    txt = item.get("text")
                    if isinstance(txt, str) and txt.strip():
                        parts.append(txt.strip())
            return "\n".join(parts).strip()
        return ""

    summary_prompt = f"""You are creating durable memory for an AI research assistant.
Summarize this conversation so it can be resumed accurately later.

Output with exactly these headings:
### Technical Information
### Emotional Context
### Entities & References
### Action Items & Decisions

Rules:
- Keep concrete details (names, dates, APIs, errors, decisions).
- Separate confirmed facts from open questions where relevant.
- Do not invent information.
- Keep it concise and useful for continuation.

Conversation:
{cleaned[:6000]}"""

    response = llm_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": summary_prompt}],
        max_completion_tokens=4000
    )
    summary = _message_text(response)

    # Retry once with a simpler prompt if output is empty.
    if not summary:
        retry_prompt = f"""Summarize this conversation in <= 180 words using these headings:
### Technical Information
### Emotional Context
### Entities & References
### Action Items & Decisions

Conversation:
{cleaned[:6000]}"""
        retry = llm_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": retry_prompt}],
            max_completion_tokens=4000
        )
        summary = _message_text(retry)

    if not summary:
        excerpt = cleaned[:500].replace("\n", " ").strip()
        summary = (
            "### Technical Information\n"
            f"{excerpt or '(No content provided.)'}\n\n"
            "### Emotional Context\n"
            "Not available from model output.\n\n"
            "### Entities & References\n"
            "Not available from model output.\n\n"
            "### Action Items & Decisions\n"
            "Not available from model output."
        )

    desc_prompt = f"""Create a short 8-12 word label for this summary.
Return ONLY the label.

Summary:
{summary}"""

    desc_response = llm_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": desc_prompt}],
        max_completion_tokens=2000
    )
    description = _message_text(desc_response) or "Conversation summary"

    summary_id = str(uuid.uuid4())[:8]
    memory_manager.write_summary(summary_id, cleaned, summary, description)

    return {"id": summary_id, "description": description, "summary": summary}


[markdown] cell 30

### Agent Tools for Memory Operations

These tools are registered with the Toolbox so the agent can call them during execution.

[markdown] cell 31

<!-- edu-bridge:3718c3b7 -->
### Summary Expansion Tool

`expand_summary` is registered so compressed context can be expanded on demand. Compaction and recoverability stay paired, which is critical for agent reliability.

[code] cell 32

# Summary tools for the agent
@toolbox.register_tool(augment=True)
def expand_summary(summary_id: str) -> str:
    """
    Expand a summary reference to retrieve the original conversations.

    Use when you need more details from a [Summary ID: xxx] reference.
    Returns all original messages that were summarized, in chronological order with timestamps.
    """
    # Get the summary text for context
    summary_text = memory_manager.read_summary_memory(summary_id)

    # Get the original conversations that were summarized
    original_conversations = memory_manager.read_conversations_by_summary_id(summary_id)

    return f"""
            ## Summary Context
                {summary_text}

                {original_conversations}
        """


[markdown] cell 33

<!-- edu-bridge:936738a1 -->
### Conversation Summarizer

Thread-level summarization is implemented over unsummarized rows and tagged with `summary_id`. This provides precise consolidation and traceability back to source units.

[code] cell 34

def summarize_conversation(thread_id: str) -> dict:
    """
    Summarize all unsummarized messages in a thread and mark those exact units.

    This function:
    1. Reads unsummarized message rows from the thread
    2. Generates a structured summary via LLM
    3. Stores the summary in summary memory
    4. Marks the exact source rows with summary_id
    5. Returns the summary object for continued context
    """
    thread_id = str(thread_id)

    # Read raw unsummarized conversation units (IDs + content)
    with memory_manager.conn.cursor() as cur:
        cur.execute(f"""
            SELECT id, role, content, timestamp
            FROM {memory_manager.conversation_table}
            WHERE thread_id = :thread_id AND summary_id IS NULL
            ORDER BY timestamp ASC
        """, {"thread_id": thread_id})
        rows = cur.fetchall()

    if not rows:
        return {"status": "nothing_to_summarize"}

    # Build transcript from unsummarized units only
    message_ids = []
    transcript_lines = []
    for msg_id, role, content, timestamp in rows:
        message_ids.append(msg_id)
        ts_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else "Unknown"
        transcript_lines.append(f"[{ts_str}] [{str(role).upper()}] {content}")

    transcript = "\n".join(transcript_lines)

    # Summarize the exact transcript
    result = summarise_context_window(transcript, memory_manager, client)
    if result.get("status") == "nothing_to_summarize":
        return result

    summary_id = result["id"]

    # Mark the exact source rows with the generated summary_id
    with memory_manager.conn.cursor() as cur:
        cur.executemany(f"""
            UPDATE {memory_manager.conversation_table}
            SET summary_id = :summary_id
            WHERE id = :id AND summary_id IS NULL
        """, [{"summary_id": summary_id, "id": msg_id} for msg_id in message_ids])
    memory_manager.conn.commit()

    result["num_messages_summarized"] = len(message_ids)

    print(f"✅ Conversation summarized: [Summary ID: {summary_id}]")
    print(f"   Description: {result['description']}")
    print(f"   Messages marked summarized: {len(message_ids)}")

    return result

[markdown] cell 35

<!-- edu-bridge:16abf75a -->
### Offload Policy

A simple offload policy compacts conversation-heavy context into summary references. It keeps the context window lean while preserving a retrieval path to details.

[code] cell 36

def offload_to_summary(context: str, memory_manager, llm_client, thread_id: str = None) -> tuple:
    """
    Simple context compaction:
    - If thread_id is provided, summarize unsummarized conversation units for that thread.
    - Otherwise, summarize the provided context string.
    - Replace only conversation-heavy context and keep other memory segments.
    """
    raw_context = (context or "").strip()

    if thread_id:
        result = summarize_conversation(thread_id)
    else:
        result = summarise_context_window(raw_context, memory_manager, llm_client)

    if result.get("status") == "nothing_to_summarize":
        return raw_context, []

    summary_ref = f"[Summary ID: {result['id']}] {result['description']}"
    conversation_stub = (
        "## Conversation Memory\n"
        "Older conversation content was summarized to reduce context size.\n"
        "Use Summary Memory references + expand_summary(id) for full detail."
    )

    # Replace only conversation section, preserve other memory sections.
    compact_context = raw_context
    if "## Conversation Memory" in compact_context:
        lines = compact_context.splitlines()
        rebuilt = []
        in_conversation = False
        inserted_stub = False

        for line in lines:
            if line.startswith("## "):
                heading = line.strip()
                if heading == "## Conversation Memory":
                    in_conversation = True
                    if not inserted_stub:
                        if rebuilt and rebuilt[-1].strip():
                            rebuilt.append("")
                        rebuilt.extend(conversation_stub.splitlines())
                        rebuilt.append("")
                        inserted_stub = True
                    continue
                in_conversation = False

            if not in_conversation:
                rebuilt.append(line)

        compact_context = "\n".join(rebuilt).strip()
    else:
        compact_context = f"{conversation_stub}\n\n{compact_context}".strip()

    if "## Summary Memory" in compact_context:
        compact_context = f"{compact_context}\n{summary_ref}".strip()
    else:
        compact_context = (
            f"{compact_context}\n\n"
            "## Summary Memory\n"
            "Use expand_summary(id) to retrieve full underlying content.\n"
            f"{summary_ref}"
        ).strip()

    return compact_context, [result]


[markdown] cell 37

<!-- edu-bridge:bf92accc -->
### Agent Summarize Tool

`summarize_and_store` exposes summarization as an agent-callable tool. The offload capability now becomes available during autonomous execution.

[code] cell 38

@toolbox.register_tool(augment=True)
def summarize_and_store(text: str, thread_id: str = None) -> str:
    """
    Summarize long text and store in memory.

    If thread_id is provided, summarize unsummarized conversation units from that thread
    and mark exactly those units with the generated summary_id.
    """
    if thread_id:
        result = summarize_conversation(thread_id)
        if result.get("status") == "nothing_to_summarize":
            return f"No unsummarized messages found for thread {thread_id}."
        return f"Stored as [Summary ID: {result['id']}] {result['description']}"

    result = summarise_context_window(text, memory_manager, client)
    if result.get("status") == "nothing_to_summarize":
        return "No content to summarize."
    return f"Stored as [Summary ID: {result['id']}] {result['description']}"


[markdown] cell 39

<!-- edu-bridge:8315929b -->
### Context Monitor Utility

A monitor function maps usage into `ok`, `warning`, and `critical` states. This closes the helper pipeline with clear operational thresholds.

[code] cell 40

def monitor_context_window(context: str, model: str = "gpt-5-mini") -> dict:
    """
    Monitor the current context window and return capacity utilization.

    Args:
        context: The current context string to measure
        model: The model being used (to determine max tokens)

    Returns:
        dict with:
        - tokens: Estimated token count
        - max: Maximum tokens for the model
        - percent: Percentage of capacity used
        - status: 'ok', 'warning', or 'critical' based on usage
    """
    result = calculate_context_usage(context, model)

    # Add status indicator
    if result['percent'] < 50:
        result['status'] = 'ok'
    elif result['percent'] < 80:
        result['status'] = 'warning'
    else:
        result['status'] = 'critical'

    return result

[markdown] cell 41

**Part 2 Takeaway:** We've built a complete summarization pipeline that monitors context usage, generates structured summaries, and provides tools for the agent to expand summaries when needed.

---

## Part 3: Testing the Memory Pipeline

Now let's verify that our memory consolidation system works end-to-end.

### Test Workflow

| Step | Action | Verification |
|------|--------|--------------|
| 1 | Create test conversation | Messages stored in conversational memory |
| 2 | Monitor context usage | Token count and percentage calculated |
| 3 | Summarize conversation | Summary captures key information |
| 4 | Expand summary | Original messages retrievable |
| 5 | Verify marking | Summarized messages marked as processed |

### Step 1: Create Test Conversation

[markdown] cell 42

<!-- edu-bridge:025b1d47 -->
### Test Thread Creation

A realistic multi-turn conversation is seeded to validate the full summarization lifecycle. The environment and utilities are now exercised end to end.

[code] cell 43

# Step 1: Create a test thread with sample conversations
import time
from helper import SAMPLE_RESEARCH_CONVERSATION

TEST_THREAD_ID = f"test_summary_{int(time.time())}"

# Use the sample conversation from helper.py (30 messages about research papers)
test_messages = SAMPLE_RESEARCH_CONVERSATION

print(f"📝 Creating test thread: {TEST_THREAD_ID}")
print("-" * 50)

for role, content in test_messages:
    memory_manager.write_conversational_memory(content, role, TEST_THREAD_ID)
    print(f"[{role.upper()}] {content[:70]}...")
    time.sleep(0.05)  # Small delay to ensure distinct timestamps

print(f"✅ Added {len(test_messages)} messages to thread")

[markdown] cell 44

### Step 2: Monitor Context Usage

[markdown] cell 45

<!-- edu-bridge:85f1bddd -->
### Pre-Summary Measurement

Baseline context usage is measured before any compression. This creates a reference point for evaluating the effect of summarization.

[code] cell 46

# Step 2: Monitor context usage before summarization
current_context = memory_manager.read_conversational_memory(TEST_THREAD_ID, limit=100)

print("📊 CONTEXT WINDOW MONITOR (Before Summarization)")
print("=" * 50)
usage = monitor_context_window(current_context)
print(f"  Tokens: {usage['tokens']:,}")
print(f"  Max: {usage['max']:,}")
print(f"  Usage: {usage['percent']}%")
print(f"  Status: {usage['status'].upper()}")
print()
print("📄 Current conversation content:")
print("-" * 50)
print(current_context)

[markdown] cell 47

### Step 3: Summarize the Conversation

[markdown] cell 48

<!-- edu-bridge:99c09821 -->
### Summarization Execution

The summarization pipeline runs and produces a durable summary artifact. This demonstrates how verbose history is compacted for continued reasoning.

[code] cell 49

# Step 3: Summarize the conversation
print("🔄 SUMMARIZING CONVERSATION")
print("=" * 50)

summary_result = summarize_conversation(TEST_THREAD_ID)

print(f"\n📋 Summary Result:")
print(f"  ID: {summary_result['id']}")
print(f"  Description: {summary_result['description']}")
print(f"\n📝 Full Summary (for new context window):")
print("-" * 50)
print(summary_result['summary'])

[markdown] cell 50

### Step 4: Expand the Summary

[markdown] cell 51

<!-- edu-bridge:be6ba99c -->
### Summary Expansion Check

The new summary reference is expanded to recover original chronology and detail. It confirms that compact memory remains reversible when precision is needed.

[code] cell 52

# Step 4: Expand the summary to retrieve original conversations
print("🔍 EXPANDING SUMMARY - Retrieving Original Conversations")
print("=" * 50)
print(f"Summary ID: {summary_result['id']}")
print()

# Access the function via toolbox._tools_by_name (since decorator returns ID, not function)
expand_fn = toolbox._tools_by_name['expand_summary']
expanded = expand_fn(summary_result['id'])
print(expanded)

[markdown] cell 53

### Step 5: Verify the Pipeline

[markdown] cell 54

<!-- edu-bridge:d74e0d45 -->
### Post-Summary Verification

API-level and DB-level checks verify that summarized rows are tagged and omitted from unsummarized reads. The consolidation loop is validated with explicit evidence.

[code] cell 55

# Step 5: Verify - After summarization, unsummarized messages should be empty
print("✅ VERIFICATION - Thread After Summarization")
print("=" * 50)

# High-level check via memory API (should show no unsummarized messages)
remaining = memory_manager.read_conversational_memory(TEST_THREAD_ID, limit=100)
print("Unsummarized messages in thread (memory API):")
print(remaining)

# Ground-truth check at DB row level
with memory_manager.conn.cursor() as cur:
    cur.execute(f"""
        SELECT COUNT(*)
        FROM {memory_manager.conversation_table}
        WHERE thread_id = :thread_id AND summary_id IS NULL
    """, {"thread_id": TEST_THREAD_ID})
    unsummarized_count = cur.fetchone()[0]

    cur.execute(f"""
        SELECT COUNT(*)
        FROM {memory_manager.conversation_table}
        WHERE thread_id = :thread_id AND summary_id IS NOT NULL
    """, {"thread_id": TEST_THREAD_ID})
    summarized_count = cur.fetchone()[0]

    cur.execute(f"""
        SELECT DISTINCT summary_id
        FROM {memory_manager.conversation_table}
        WHERE thread_id = :thread_id AND summary_id IS NOT NULL
        ORDER BY summary_id
    """, {"thread_id": TEST_THREAD_ID})
    summary_ids = [row[0] for row in cur.fetchall()]

print(f"\nDB verification:")
print(f"  Unsummarized rows: {unsummarized_count}")
print(f"  Summarized rows: {summarized_count}")
print(f"  Summary IDs applied: {summary_ids}")

if unsummarized_count == 0 and summarized_count > 0:
    print("✅ PASS: conversation units summarized and tagged with summary_id")
else:
    print("⚠️ CHECK: expected 0 unsummarized rows and >0 summarized rows")

print("\n" + "=" * 50)
print("🎉 TEST COMPLETE!")
print("=" * 50)
print("""
Summary of what happened:
1. ✅ Created test conversation with 30 messages
2. ✅ Monitored context window usage
3. ✅ Summarized conversation with a structured LLM prompt
4. ✅ Expanded summary to retrieve original messages with timestamps
5. ✅ Verified source conversation rows are marked with summary_id
""")


[markdown] cell 56

**Part 3 Takeaway:** The test demonstrates the complete memory consolidation cycle: conversations are stored, monitored, summarized when needed, and marked to prevent reprocessing.

---

## Lesson Summary

In this lesson, you learned how to build a self-managing memory system for AI agents:

| Capability | Implementation |
|------------|----------------|
| **Monitor** | `calculate_context_usage()` tracks token consumption |
| **Summarize** | `summarise_context_window()` extracts structured information |
| **Store** | Summaries persist in `SUMMARY_MEMORY` with links to originals |
| **Expand** | `expand_summary()` tool retrieves original conversations |
| **Self-Update** | `mark_as_summarized()` prevents re-processing |

**Key Insight:** Memory consolidation isn't just about compression—it's about *structured extraction* that preserves technical details, emotional context, entities, and action items.

---

## L5/L5.ipynb

[markdown] cell 0

# L5: Memory Aware Agent

[markdown] cell 1

<div style="background-color:#fff6e4; padding:15px; border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"> <p>⏳ <b>Note <code>(Database Starting)</code>:</b> This notebook takes about 30-60 seconds to be ready to use. You may start and watch the video while you wait.</p>
<p>If you see <tt>Admin connection failed</tt> after running the first cell, simply wait and re-run — it is not a credentials issue.</p>
</div>

[markdown] cell 2

This lesson brings together everything from the previous labs to build a complete **Memory Aware Agent**—an AI system that can remember past conversations, learn from interactions, and manage its context window intelligently.

**Lesson Objectives**

By the end of this lesson, you will understand how to:
- Integrate all memory types (conversational, semantic, workflow, entity, summary, tool logs) into a unified agent
- Implement context window management with automatic summarization
- Build an agent loop that retrieves relevant context before each response
- Use Just-In-Time (JIT) retrieval to expand summaries on demand

**Key Concepts**

| Concept | Description |
|---------|-------------|
| **Memory Aware Agent** | An agent that reads from and writes to persistent memory stores during execution |
| **Context Engineering** | Dynamically building the optimal context window for each query |
| **Just-In-Time Retrieval** | Fetching detailed information only when the agent needs it |
| **Automatic Summarization** | Compressing context when usage exceeds thresholds |

[markdown] cell 3

<div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
<p> 💻 &nbsp; <b>Access <code>requirements.txt</code> and <code>helper.py</code> files:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em>.

<p> ⬇ &nbsp; <b>Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>

</div>

[markdown] cell 4

## Part 1: Setup and Infrastructure

This section initializes the complete memory infrastructure needed for our agent. We reuse the components built in previous labs:
- **Database Connection** — Oracle Database for persistent storage
- **Memory Stores** — Vector stores for each memory type
- **MemoryManager** — Unified interface for memory operations
- **Toolbox** — Registry for agent-callable tools

### Database and Embedding Setup

[code] cell 5

from helper import suppress_warnings

# Warning control
suppress_warnings()

from helper import load_env, setup_oracle_database, connect_to_oracle

load_env()

# One-time admin setup: configures tablespace, vector memory, and VECTOR user
setup_oracle_database()

# Connect as the VECTOR user for all subsequent operations
database_connection = connect_to_oracle(
    user="VECTOR",
    password="VectorPwd_2025",
    dsn="127.0.0.1:1521/FREEPDB1",
    program="devrel.deeplearning.course_1",
)

print("Using user:", database_connection.username)

[code] cell 6

from openai import OpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings

client = OpenAI()

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-mpnet-base-v2"
)

[markdown] cell 7

### Memory Stores and Managers

We configure seven memory types that our agent will use:

| Memory Type | Purpose |
|-------------|---------|
| **Conversational** | Chat history for context continuity |
| **Semantic (Knowledge Base)** | Documents and facts retrieved by similarity |
| **Workflow** | Past tool execution patterns |
| **Toolbox** | Available tools with semantic search |
| **Entity** | Extracted people, places, concepts |
| **Summary** | Compressed conversation summaries |
| **Tool Log** | Raw tool-call inputs, outputs, status, and errors for audit/JIT retrieval |

[code] cell 8

# Table names for each memory type
CONVERSATIONAL_TABLE = "CONVERSATIONAL_MEMORY"
KNOWLEDGE_BASE_TABLE = "SEMANTIC_MEMORY"
WORKFLOW_TABLE = "WORKFLOW_MEMORY"
TOOLBOX_TABLE = "TOOLBOX_MEMORY"
ENTITY_TABLE = "ENTITY_MEMORY"
SUMMARY_TABLE = "SUMMARY_MEMORY"
TOOL_LOG_TABLE = "TOOL_LOG_MEMORY"

[markdown] cell 9

### Clean Slate: Drop Existing Tables

<p style="background-color:#ff9a94; padding:15px; border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"> ⏳ <b>Note:</b> To ensure this lesson runs correctly regardless of whether previous lessons have been executed, we drop all memory tables before recreating them by running the cell below. This guarantees a clean starting state with consistent distance strategy and no stale data for the lesson.</p>

[code] cell 10

ALL_TABLES = [
    CONVERSATIONAL_TABLE,
    KNOWLEDGE_BASE_TABLE,
    WORKFLOW_TABLE,
    TOOLBOX_TABLE,
    ENTITY_TABLE,
    SUMMARY_TABLE,
    TOOL_LOG_TABLE]

# Drop existing tables to start fresh
for table in ALL_TABLES:
    try:
        with database_connection.cursor() as cur:
            cur.execute(f"DROP TABLE {table} PURGE")
            print(f"  - {table} (dropped)")
    except Exception as e:
        if "ORA-00942" in str(e):
            print(f"  - {table} (not exists)")
        else:
            print(f"  ✗ {table}: {e}")

database_connection.commit()

[code] cell 11


# Create or retrieve the conversational history table
from helper import create_conversational_history_table, create_tool_log_table
CONVERSATION_HISTORY_TABLE = create_conversational_history_table(database_connection, CONVERSATIONAL_TABLE)
TOOL_LOG_HISTORY_TABLE = create_tool_log_table(database_connection, TOOL_LOG_TABLE)

[code] cell 12

from langchain_oracledb.vectorstores import OracleVS
from langchain_community.vectorstores.utils import DistanceStrategy
from helper import StoreManager

# Create StoreManager instance
store_manager = StoreManager(
    client=database_connection,
    embedding_function=embedding_model,
    table_names={
        'knowledge_base': KNOWLEDGE_BASE_TABLE,
        'workflow': WORKFLOW_TABLE,
        'toolbox': TOOLBOX_TABLE,
        'entity': ENTITY_TABLE,
        'summary': SUMMARY_TABLE,
    },
    distance_strategy=DistanceStrategy.EUCLIDEAN_DISTANCE,
    conversational_table=CONVERSATION_HISTORY_TABLE,
    tool_log_table=TOOL_LOG_HISTORY_TABLE,
)

# Get all stores via the manager
conversation_table = store_manager.get_conversational_table()
knowledge_base_vs = store_manager.get_knowledge_base_store()
workflow_vs = store_manager.get_workflow_store()
toolbox_vs = store_manager.get_toolbox_store()
entity_vs = store_manager.get_entity_store()
summary_vs = store_manager.get_summary_store()
tool_log_table = store_manager.get_tool_log_table()

print("✅ All stores loaded via StoreManager")

[code] cell 13

from helper import MemoryManager, Toolbox, register_common_tools

# Initialize the MemoryManager instance
memory_manager = MemoryManager(
    conn=database_connection,
    conversation_table=conversation_table,
    knowledge_base_vs=knowledge_base_vs,
    workflow_vs=workflow_vs,
    toolbox_vs=toolbox_vs,
    entity_vs=entity_vs,
    summary_vs=summary_vs,
    tool_log_table=TOOL_LOG_HISTORY_TABLE
)

# Initialize Toolbox with embedding function
toolbox = Toolbox(memory_manager, client, embedding_model)

# Register common tools (arxiv search, paper fetch, etc.)
common_tools = register_common_tools(toolbox, memory_manager, KNOWLEDGE_BASE_TABLE)

print("✅ MemoryManager and Toolbox initialized")

[markdown] cell 14

**Part 1 Takeaway:** We now have all memory infrastructure in place. The `MemoryManager` provides read/write access to all memory types, and the `Toolbox` has common tools registered for the agent to use.

---

## Part 2: Context Engineering Techniques

Context engineering is the practice of dynamically constructing the optimal input for an LLM based on the current query. Rather than passing everything to the model, we selectively retrieve and compress information to maximize relevance while staying within token limits.

[markdown] cell 15

### What This Section Covers

| Step | Function | Purpose |
|------|----------|---------|
| **1. Calculate Usage** | `calculate_context_usage()` | Monitor what % of the context window is used |
| **2. Summarize** | `summarise_context_window()` | Compress long content into summaries using LLM |
| **3. Offload** | `offload_to_summary()` | Auto-trigger summarization when usage exceeds threshold |
| **4. Just-in-Time Retrieval** | `expand_summary()` tool | Let agent expand summaries on demand |

**`Just-In-Time (JIT)`** retrieval is the process of fetching only the information needed at the exact moment the agent requires it, based on the current task, query, or reasoning step. Instead of loading pre-computed or pre-cached context upfront, the system dynamically retrieves the minimal, most relevant data on demand, ensuring efficiency and reducing context overload. In the context of agent memory JIT is a retrieval-control strategy where memory access is triggered by the agent’s current goal, query, or reasoning step. Rather than preloading large histories or the full knowledge base, the system dynamically filters, ranks, and injects only the information that materially influences the next token. This reduces context saturation, improves attention allocation, and increases reasoning fidelity.

[code] cell 16

# Import context window management functions from helper
# Summary tools are now loaded through register_common_tools in Part 1.
from helper import (
    calculate_context_usage,
    monitor_context_window,
    summarise_context_window,
    offload_to_summary,
    summarize_conversation,
)

print("✅ Context management functions loaded from helper.py")



[markdown] cell 17

**Part 2 Takeaway:** Context engineering functions are now loaded from `helper.py`. These enable the agent to monitor context usage, summarize when needed, and expand summaries on demand.

---

## Part 3: The Memory-Aware Agent Loop

This is where everything comes together. The agent loop orchestrates memory operations at each step:

```
User Query
    ↓
1. BUILD CONTEXT — Read from all memory stores
    ↓
2. CHECK USAGE — Monitor token count, summarize if >80%
    ↓
3. SELECT TOOLS — Semantic search for relevant tools
    ↓
4. EXECUTE — LLM reasoning + tool calls
    ↓
5. PERSIST — Save conversation, workflow, entities
    ↓
Final Answer
```

### System Prompt and Tool Execution

[code] cell 18

import json as json_lib

AGENT_SYSTEM_PROMPT = """
# Role
You are a memory-aware agentic research assistant with access to tools.

# Context Window Structure (Partitioned Segments)
The user input is a partitioned context window. It contains a `# Question` section followed by memory segments.
Treat each segment as a distinct memory store with a specific purpose:
- `## Conversation Memory`
- `## Knowledge Base Memory`
- `## Workflow Memory`
- `## Entity Memory`
- `## Summary Memory`

# Memory Store Semantics
- Conversation Memory: Recent thread-level dialogue and instructions. Use it for continuity, user preferences, and unresolved requests.
- Knowledge Base Memory: Retrieved documents/passages. Use it to ground factual and technical claims.
- Workflow Memory: Prior execution patterns and step sequences. Use it to plan tool usage; adapt patterns, do not copy blindly.
- Entity Memory: Named people/orgs/systems and descriptors. Use it to disambiguate references and keep naming consistent.
- Summary Memory: Compressed older context represented by summary IDs. When thread-scoped summaries exist, prefer summaries for the active thread_id.

# Summary Expansion Policy
If critical detail is only present in Summary Memory or appears ambiguous, call `expand_summary(summary_id)` before relying on it.

# Operating Rules
1. Start with the provided memory segments before using tools.
2. If segments conflict, prioritize: current `# Question` > latest Conversation Memory > Knowledge Base evidence > older summaries/workflows.
3. Use only the tools provided in this turn and choose the minimum necessary tool calls.
4. If memory is insufficient, state what is missing and then use an appropriate tool.
5. For conversation compaction, use `summarize_and_store` with `thread_id` so source conversation units are marked as summarized.
"""


def execute_tool(tool_name: str, tool_args: dict, current_thread_id: str | None = None) -> str:
    """Execute a tool by looking it up in the toolbox."""

    if tool_name not in toolbox._tools_by_name:
        return f"Error: Tool '{tool_name}' not found"

    args = dict(tool_args or {})

    # Ensure conversation summarization marks source rows in the active thread.
    if tool_name == "summarize_and_store" and "thread_id" not in args and current_thread_id is not None:
        args["thread_id"] = str(current_thread_id)

    return str(toolbox._tools_by_name[tool_name](**args) or "Done")

# ==================== OPENAI CHAT FUNCTION ====================
def call_openai_chat(messages: list, tools: list = None, model: str = "gpt-5-mini"):
    """Call OpenAI Chat Completions API with tools."""
    kwargs = {"model": model, "messages": messages}
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    return client.chat.completions.create(**kwargs)




[markdown] cell 19

### Agent Loop: End-to-End Execution Flow

`call_agent()` is the orchestration layer that turns memory + tools into a reliable multi-step agent run.

1. **Build a partitioned context window**  
   The function pulls memory segments in order: Conversation, Knowledge Base, Workflow, Entity, and Summary.  
   This gives the model a structured, role-specific context instead of one mixed block.

2. **Protect context budget before reasoning**  
   Token usage is measured with `calculate_context_usage()`.  
   If usage is above 80%, `offload_to_summary()` compresses conversation-heavy content into Summary Memory and keeps summary references.

3. **Retrieve only relevant tools**  
   Toolbox memory is searched semantically (`read_toolbox(query, k=5)`), so the model sees a focused toolset for this query.

4. **Run iterative LLM-tool execution**  
   The model can issue tool calls, each tool runs, and the result is returned to the model through `role="tool"` messages.  
   Full raw tool outputs are persisted to `TOOL_LOG_MEMORY` for audit and later retrieval.

5. **Control tool-output bloat in prompt context**  
   The next LLM turn receives only the immediate tool result (truncated when very large), while the complete payload remains in the database.

6. **Persist learning artifacts**  
   At the end, the loop writes conversational turns, workflow steps, and extracted entities so future runs can reuse this execution history.



[code] cell 20

# ==================== MAIN AGENT LOOP ====================
def call_agent(query: str, thread_id: str = "1", max_iterations: int = 10) -> str:
    """Agent loop with context window monitoring and summarization."""
    thread_id = str(thread_id)
    steps = []
    summaries = []  # Track created summaries
    
    # 1. Build context from memory
    print("\n" + "="*50)
    print("🧠 BUILDING CONTEXT...")
    
    # Build memory context (excluding query for now)
    memory_context = ""
    memory_context += memory_manager.read_conversational_memory(thread_id) + "\n\n"
    memory_context += memory_manager.read_knowledge_base(query) + "\n\n"
    memory_context += memory_manager.read_workflow(query) + "\n\n"
    memory_context += memory_manager.read_entity(query) + "\n\n"
    memory_context += memory_manager.read_summary_context(query, thread_id=thread_id) + "\n\n"  # Shows IDs + descriptions (thread-scoped when available)
    
    # 2. Check context usage - summarize if >80%
    usage = calculate_context_usage(memory_context)
    print(f"📊 Context: {usage['percent']}% ({usage['tokens']}/{usage['max']} tokens)")
    
    if usage['percent'] > 80:
        print("⚠️ Context >80% - offloading conversation context to summary memory...")
        memory_context, summaries = offload_to_summary(
            memory_context,
            memory_manager,
            client,
            thread_id=thread_id,
        )
        if summaries:
            print(f"🧾 Created {len(summaries)} summary reference(s): {[s['id'] for s in summaries]}")
        usage = calculate_context_usage(memory_context)
        print(f"📊 After offload: {usage['percent']}% ({usage['tokens']}/{usage['max']} tokens)")
    
    # Now prepend the query (always preserved, never summarized)
    context = f"# Question\n{query}\n\n{memory_context}"

    print("====CONTEXT WINDOW=====\n")
    print(context)
    
    # 3. Get tools
    dynamic_tools = memory_manager.read_toolbox(query, k=5)
    print(f"🔧 Tools: {[t['function']['name'] for t in dynamic_tools]}")
    
    # 4. Store user message & extract entities
    memory_manager.write_conversational_memory(query, "user", thread_id)
    try:
        memory_manager.write_entity("", "", "", llm_client=client, text=query)
    except Exception:
        pass
    
    # 5. Agent loop
    messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}, {"role": "user", "content": context}]
    final_answer = ""
    
    print("\n🤖 AGENT LOOP")
    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")
        
        response = call_openai_chat(messages, tools=dynamic_tools)
        msg = response.choices[0].message
        
        if msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": [
                {"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ]})
            
            for tc in msg.tool_calls:
                tool_name = tc.function.name
                tool_args = json_lib.loads(tc.function.arguments)
                # Format args for display (truncate long values)
                args_display = {k: (v[:50] + '...' if isinstance(v, str) and len(v) > 50 else v) 
                               for k, v in tool_args.items()}
                print(f"🛠️ {tool_name}({args_display})")
                
                try:
                    result = execute_tool(tool_name, tool_args, current_thread_id=thread_id)
                    status = "success"
                    error_message = None
                    steps.append(f"{tool_name}({args_display}) → success")
                except Exception as e:
                    result = f"Error: {e}"
                    status = "failed"
                    error_message = str(e)
                    steps.append(f"{tool_name}({args_display}) → failed")

                # Persist full tool output to TOOL_LOG_MEMORY
                log_id = memory_manager.write_tool_log(
                    thread_id=thread_id,
                    tool_call_id=tc.id,
                    tool_name=tool_name,
                    tool_args=tool_args,
                    result=result,
                    status=status,
                    error_message=error_message,
                    metadata={"iteration": iteration + 1},
                )

                # Next call gets only the immediate tool result (bounded for context control)
                if len(result) > 3000:
                    result_for_llm = result[:3000] + f"\n\n[Truncated for context. Full output saved in TOOL_LOG_MEMORY as log_id: {log_id}]"
                else:
                    result_for_llm = result

                result_display = result_for_llm[:200] + "..." if len(result_for_llm) > 200 else result_for_llm
                print(f"   → {result_display}")
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result_for_llm})
        else:
            final_answer = msg.content or ""
            print(f"\n✅ DONE ({len(steps)} tool calls)")
            break
    else:
        # Max iterations reached without final answer
        print(f"\n⚠️ WARNING: Max iterations ({max_iterations}) reached without final answer")
        final_answer = "I was unable to complete the request within the allowed iterations."
    
    # 6. Save workflow & entities
    if steps:
        memory_manager.write_workflow(query, steps, final_answer)
    try:
        memory_manager.write_entity("", "", "", llm_client=client, text=final_answer)
    except Exception:
        pass
    memory_manager.write_conversational_memory(final_answer, "assistant", thread_id)
    
    print("\n" + "="*50 + f"\n💬 ANSWER:\n{final_answer}\n" + "="*50)
    return final_answer



[markdown] cell 21

### Testing the Agent

Now let's test our memory-aware agent. Notice how it:
- Builds context from memory before responding
- Uses tools to fetch and store information
- Persists the interaction for future context

[code] cell 22

call_agent("Can you get me the paper MemGPT", thread_id="50000")

[code] cell 23

call_agent("Can you save the content of the paper", thread_id="50000")

[code] cell 24

call_agent("What are the main key takeaways from the paper", thread_id="50000")

[code] cell 25

call_agent("Summarize the converstation so far using your tool", thread_id="50000")

[code] cell 26

call_agent("What was my first question?", thread_id="50000")

[markdown] cell 27

**Part 3 Takeaway:** The agent loop demonstrates how memory operations integrate into the execution flow—reading context before reasoning, managing token limits dynamically, and persisting results for future use.

---

## Lesson Summary

In this lesson, you built a complete **Memory Aware Agent** that:

| Capability | Implementation |
|------------|----------------|
| **Reads Memory** | Retrieves from 7 memory types before each response (tool logs remain JIT by default) |
| **Manages Context** | Monitors tokens, summarizes when >80% capacity |
| **Uses Tools** | Semantic search selects relevant tools per query |
| **Persists Learning** | Saves conversations, workflows, entities, and raw tool logs |
| **Expands On-Demand** | JIT retrieval via `expand_summary()` tool |

**Key Insight:** A memory-aware agent doesn't just respond to queries—it *learns* from each interaction. Information discovered, decisions made, and patterns executed are all persisted, making the agent more capable over time.
