# Prompt 3: System Architecture Question

## Scenario

You are designing a **real-time collaborative document editing system** (similar to Google Docs).

## Requirements

1. **Real-time Collaboration**
   - Multiple users editing the same document simultaneously
   - Changes visible to all users instantly
   - Cursor positions visible to collaborators

2. **Data Consistency**
   - No data loss during concurrent edits
   - Conflict resolution when edits overlap
   - Offline support with sync when reconnected

3. **Scalability**
   - Support for large documents (1000+ pages)
   - Support for many concurrent users per document
   - Low latency across different geographic regions

## Questions to Answer

1. What **conflict resolution algorithm** would you use? (OT, CRDT, or other)
2. How would you architect the **backend services**?
3. How would you handle **offline editing and sync**?
4. What **database technology** would you choose and why?
5. How would you ensure **low latency** for users globally?
