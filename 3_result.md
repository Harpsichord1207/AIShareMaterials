# Real-time Collaborative Editor Architecture

## 1. Conflict Resolution: CRDT (Conflict-free Replicated Data Types)

### Why CRDT over OT?

| Criterion | CRDT | OT |
|-----------|------|-----|
| Server dependency | ❌ Serverless possible | ✅ Requires central server |
| Offline support | ✅ Excellent | ⚠️ Complex |
| Complexity | ⚠️ Higher initial | ✅ Simpler concepts |
| Scalability | ✅ Highly scalable | ⚠️ Server bottleneck |

**Recommendation**: Use **Yjs CRDT** library for document sync.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User A    │     │   User B    │     │   User C    │
│  (Offline)  │     │   (Online)  │     │   (Online)  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │    CRDT Merge     │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │  WebSocket  │
                    │   Server    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Document   │
                    │   State     │
                    └─────────────┘
```

---

## 2. Backend Architecture

```
┌────────────────────────────────────────────────────────────┐
│                      Load Balancer                         │
└─────────────────────────┬──────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌─────▼─────┐     ┌────▼────┐
   │  API    │      │ WebSocket │     │  REST   │
   │ Gateway │      │  Cluster  │     │  API    │
   └────┬────┘      └─────┬─────┘     └────┬────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
┌───▼───┐           ┌─────▼─────┐        ┌─────▼─────┐
│ Auth  │           │ Document  │        │   User    │
│Service│           │  Service  │        │  Service  │
└───────┘           └─────┬─────┘        └───────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
         ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
         │ Redis   │ │  Doc    │ │  User   │
         │ (Cache) │ │   DB    │ │   DB    │
         └─────────┘ └─────────┘ └─────────┘
```

### Services Breakdown

| Service | Responsibility |
|---------|---------------|
| **API Gateway** | Rate limiting, auth validation, routing |
| **WebSocket Cluster** | Real-time message broadcasting |
| **Document Service** | CRUD operations, versioning |
| **Auth Service** | JWT validation, user sessions |

---

## 3. Offline Editing & Sync Strategy

### Implementation Flow

```
┌─────────────────────────────────────────────────────┐
│                   Client Side                        │
├─────────────────────────────────────────────────────┤
│  1. Store all edits in local IndexedDB              │
│  2. Maintain local CRDT document state              │
│  3. Queue operations when offline                   │
│  4. On reconnect: sync queued operations            │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                   Sync Protocol                      │
├─────────────────────────────────────────────────────┤
│  1. Client sends: last_sync_version + operations    │
│  2. Server responds: missed_operations + new_state  │
│  3. Client merges using CRDT merge algorithm        │
│  4. Update local state, continue editing            │
└─────────────────────────────────────────────────────┘
```

### Local Storage Schema

```javascript
// IndexedDB Structure
{
  documents: {
    id: "doc_123",
    content: Y.Doc,           // CRDT document
    lastSyncVersion: 42,
    pendingOps: [             // Queued when offline
      { type: "insert", pos: 10, text: "hello" },
      { type: "delete", pos: 5, length: 3 }
    ]
  }
}
```

---

## 4. Database Technology

### Recommended Stack

| Use Case | Technology | Reason |
|----------|------------|--------|
| **Document Storage** | PostgreSQL + JSONB | ACID, JSON queries, mature ecosystem |
| **Real-time State** | Redis | Pub/Sub, fast, in-memory |
| **Binary CRDT State** | S3 / MinIO | Cost-effective blob storage |
| **Search** | Elasticsearch | Full-text search in documents |

### Schema Design

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    owner_id UUID REFERENCES users(id),
    crdt_state BYTEA,           -- Compressed CRDT state
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE document_operations (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id),
    user_id UUID,
    operation JSONB,            -- CRDT operation
    version INTEGER,
    created_at TIMESTAMP
);
```

---

## 5. Global Low Latency Strategy

### Multi-Region Architecture

```
                    ┌─────────────┐
                    │   Global    │
                    │   Router    │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐      ┌────▼────┐
   │ US-East │       │ EU-West   │      │ Asia    │
   │ Region  │       │ Region    │      │ Region  │
   └────┬────┘       └─────┬─────┘      └────┬────┘
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐      ┌────▼────┐
   │WebSocket│       │ WebSocket │      │WebSocket│
   │ Cluster │       │  Cluster  │      │ Cluster │
   └────┬────┘       └─────┬─────┘      └────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Redis     │
                    │   Cluster   │
                    │ (Cross-DC)  │
                    └─────────────┘
```

### Latency Optimization Techniques

| Technique | Implementation |
|-----------|---------------|
| **Edge WebSocket** | User connects to nearest regional server |
| **Redis Pub/Sub** | Cross-region message propagation |
| **Binary Protocol** | Use protobuf instead of JSON |
| **Delta Compression** | Send only changes, not full state |
| **Optimistic Updates** | Apply locally before server confirm |

### Expected Latency

| Region | Local User | Cross-Region |
|--------|------------|--------------|
| US-East | ~20ms | ~100ms |
| EU-West | ~25ms | ~120ms |
| Asia | ~30ms | ~150ms |
