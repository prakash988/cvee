**One concept, infinite views — zero data duplication.**

A single stored concept can be viewed as SQL row, JSON document, graph node, 
vector, time-series point, or key-value pair. Views are computed on-the-fly 
or materialized for performance.

**Available Views:**
- **SQL Row**: Relational table row with typed columns
- **JSON Document**: Nested MongoDB-style document
- **Graph Node**: Neo4j-style node with labels and edges
- **Vector**: Dense embedding with metadata
- **Time-Series Point**: Timestamp + value
- **Key-Value**: Simple (id → data) pair