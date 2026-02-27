from cognimem import CogniMem

cm = CogniMem()
cm.start()  # Brain is alive

# ═══════════════════════════════════════════════════
# THE SQL DBA
# Gets SQL power + living brain enrichment
# ═══════════════════════════════════════════════════

result = cm.sql("""
    SELECT c.name, c.type, 
           o.total_revenue,
           COUNT(o.id) as order_count
    FROM customers c
    JOIN orders o ON o.customer_id = c.id  
    WHERE o.date >= '2025-01-01'
    GROUP BY c.name, c.type
    HAVING total_revenue > 100000
    ORDER BY total_revenue DESC
""")

# They get familiar SQL rows PLUS:
print(result.data)              # Normal SQL rows
print(result.confidence)        # "0.92 — 3 customer records have low confidence"
print(result.contradictions)    # "Customer X has conflicting addresses in 2 orders"
print(result.connections)       # "Customer Y also appears in supplier database"

# ═══════════════════════════════════════════════════
# THE BUSINESS ANALYST  
# Gets natural language + deep insights
# ═══════════════════════════════════════════════════

result = cm.ask("Which customers are buying less this quarter "
                "compared to last quarter, and why might that be?")

# Gets a human-readable answer with reasoning:
# "5 customers show declining orders:
#   1. Acme Corp: -32% (Note: they had a supply chain disruption - 
#      I found this in your support tickets)
#   2. GlobalTech: -18% (Confidence: 0.7 — incomplete order data)
#      ⚠️ Contradiction: Your CRM shows them as 'satisfied' but
#      order pattern suggests possible churn risk
#   3. ..."

# ═══════════════════════════════════════════════════
# THE DATA SCIENTIST
# Gets Python fluent API + ML features
# ═══════════════════════════════════════════════════

# Fluent Python API
df = cm.concepts.where(type="customer").filter(
    region="APAC", revenue__gt=50000
).with_relations("purchased").to_dataframe()

# In-DB ML (already built!)
clusters = cm.ml().cluster("customers", features=["revenue", "frequency"], k=5)
predictions = cm.ml().predict_confidence("materials", target="tensile_strength")
anomalies = cm.ml().detect_anomalies("orders", method="zscore")

# ═══════════════════════════════════════════════════
# THE GRAPH PERSON
# Gets Cypher-style + concept connections
# ═══════════════════════════════════════════════════

result = cm.match("""
    MATCH (m:material)-[:used_in]->(p:product)-[:sold_to]->(c:customer)
    WHERE m.type = 'steel' AND c.region = 'Europe'
    RETURN m.name, p.name, c.name, c.satisfaction
""")
# Gets graph traversal results + CogniMem discovers paths nobody asked about

# ═══════════════════════════════════════════════════
# THE ENTERPRISE DEVELOPER
# Gets stored procedures + triggers + rules + transactions
# ═══════════════════════════════════════════════════

@cm.procedure("process_return")
def process_return(order_id: str, reason: str):
    """Process a product return with full business logic."""
    order = cm.get(order_id)
    customer = cm.related(order_id, "placed_by")[0]
    
    # Check return policy (stored as a business rule concept)
    policy = cm.ask(f"What is the return policy for {order.properties['product_type']}?")
    
    if policy.data["eligible"]:
        with cm.transaction() as tx:
            tx.update(order_id, status="returned", return_reason=reason)
            tx.update(customer.id, returns_count="+1")
            # Trigger fires: check if customer has too many returns
            # Brain watches: is this part of a fraud pattern?
            tx.commit()
        return {"status": "approved", "refund": order.properties["total"]}
    else:
        return {"status": "denied", "reason": policy.data["reason"]}

# Call it via code
result = cm.call("process_return", order_id="ORD-001", reason="defective")

# OR via SQL
cm.sql("CALL process_return('ORD-001', 'defective')")

# OR via natural language  
cm.ask("Process a return for order ORD-001, the product was defective")

# ALL THREE do the SAME THING, through the SAME brain

# ═══════════════════════════════════════════════════
# THE AI/ML ENGINEER
# Gets the memory layer for LLMs
# ═══════════════════════════════════════════════════

# CogniMem as the RAG replacement for any LLM
context = cm.retrieve_for_llm(
    query="What materials should I use for a marine heat exchanger?",
    max_concepts=10,
    include_relations=True,
    include_contradictions=True,
    min_confidence=0.7
)
# Returns structured context with confidence, sources, and contradictions
# — infinitely better than dumb vector similarity search

# ═══════════════════════════════════════════════════
# THE PERSON WHO DOESN'T KNOW ANYTHING ABOUT DATABASES
# Just talks to CogniMem like a person
# ═══════════════════════════════════════════════════

with cm.dialogue(user_id="new_employee") as chat:
    chat.say("I'm new here. What does our company sell?")
    # CogniMem: "Based on 1,247 product concepts, you sell industrial 
    #            materials (primarily steel and aluminum alloys) to 
    #            342 customers across 12 regions. Your top product 
    #            is SS316L. Want me to walk you through the product lines?"
    
    chat.say("Yes please")
    # CogniMem: "Here are your 5 product categories: ..."
    # (CogniMem also proactively pushes: "By the way, I noticed 
    #  3 products have price inconsistencies you might want to 
    #  check with the pricing team.")