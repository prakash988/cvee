# ═══════════════════════════════════════════════════════════
# BUSINESS LOGIC IN COGNIMEM
# Not just stored procedures — INTELLIGENT business rules
# ═══════════════════════════════════════════════════════════

from cognimem import CogniMem

cm = CogniMem()

# ─────────────────────────────────────────────────────
# 1. STORED PROCEDURES (like traditional DBs, but smarter)
# ─────────────────────────────────────────────────────

# Register a business procedure — but CogniMem UNDERSTANDS what it does
@cm.procedure("calculate_order_total")
def calculate_order_total(order_id: str):
    """Calculate total for an order including tax and discounts."""
    order = cm.get(order_id)
    items = cm.related(order_id, "contains")
    
    subtotal = sum(item.properties["price"] * item.properties["quantity"] 
                   for item in items)
    
    # CogniMem knows the customer's region → applies correct tax
    customer = cm.related(order_id, "placed_by")[0]
    tax_rate = cm.ask(f"What is the tax rate for {customer.properties['region']}?")
    
    # CogniMem checks for applicable discounts automatically
    discounts = cm.find_applicable_rules(order, "discount")
    
    total = subtotal * (1 + tax_rate) - sum(d.value for d in discounts)
    return {"subtotal": subtotal, "tax": tax_rate, "discounts": discounts, "total": total}

# Call it
result = cm.call("calculate_order_total", order_id="ORD-2026-001")

# But ALSO — you can just ask in natural language:
result = cm.ask("What's the total for order ORD-2026-001 including tax?")
# CogniMem finds the stored procedure, runs it, explains the result


# ─────────────────────────────────────────────────────
# 2. TRIGGERS THAT THINK (not just fire-and-forget)
# ─────────────────────────────────────────────────────

@cm.trigger("on_new_order", when="AFTER_INSERT", concept_type="order")
def on_new_order(order):
    """When a new order comes in."""
    # Check inventory (CogniMem knows stock levels as concepts)
    for item in cm.related(order.id, "contains"):
        stock = cm.get_property(item.id, "stock_quantity")
        if stock < item.properties["quantity"]:
            cm.alert(
                priority="HIGH",
                message=f"⚠️ Insufficient stock for {item.name}: "
                        f"need {item.properties['quantity']}, have {stock}",
                action="notify_purchasing"
            )
    
    # Check customer credit (CogniMem reasons about it)
    customer = cm.related(order.id, "placed_by")[0]
    credit_check = cm.think_about(
        f"Should we approve credit for {customer.name} "
        f"for order value {order.properties['total']}?"
    )
    # CogniMem considers: payment history, outstanding balance,
    # credit limit, recent patterns — all from concept memory
    
    if credit_check["recommendation"] == "decline":
        cm.flag(order.id, reason=credit_check["reasoning"])


# ─────────────────────────────────────────────────────
# 3. BUSINESS RULES AS CONCEPTS (not code!)
# ───────────────────────���─────────────────────────────

# Instead of hardcoding business rules, STORE them as concepts:
cm.store_rule(
    name="discount_rule_bulk_order",
    condition="order.quantity > 100 AND customer.tier = 'gold'",
    action="apply_discount(10%)",
    domain="sales",
    effective_from="2026-01-01",
    effective_until="2026-12-31",
    approved_by="finance_team",
    confidence=1.0
)

# Rules are concepts too! CogniMem can:
# - Track which rules are used most
# - Detect conflicting rules automatically (Sentinel!)
# - Suggest new rules based on patterns (Prophet!)
# - Expire stale rules (Gardener!)
# - Challenge rules that seem wrong (Skeptic!)

# Ask CogniMem about rules naturally:
cm.ask("What discounts apply to gold tier customers ordering 200 units?")
# → "Based on rule 'discount_rule_bulk_order' (approved by finance_team, 
#    effective Jan 2026-Dec 2026): 10% discount applies.
#    Note: I also found rule 'seasonal_discount_q1' that gives an 
#    additional 5%. These rules don't conflict."


# ─────────────────────────────────────────────────────
# 4. TRANSACTIONS THAT UNDERSTAND TRUST
# ─────────────────────────────────────────────────────

with cm.transaction() as tx:
    # Traditional ACID — but with CogniMem intelligence
    tx.update("inventory_widget_a", stock=-50)
    tx.update("order_12345", status="shipped")
    tx.create_relation("order_12345", "fulfilled_by", "warehouse_east")
    
    # CogniMem adds its own checks during transaction:
    # - Sentinel: "Stock for widget_a will drop below reorder point"
    # - Prophet: "Based on sales patterns, you'll need 200 more in 2 weeks"
    # - Skeptic: "Are you sure? Last time we shipped from warehouse_east,
    #             delivery was delayed by 3 days"
    
    tx.commit()  
    # Commits AND stores the experience for learning


# ─────────────────────────────────────────────────────
# 5. COMPLEX JOINS & AGGREGATIONS (SQL power + concept intelligence)
# ─────────────────────────────────────────────────────

# SQL-style complex query — CogniMem handles it
result = cm.query("""
    SELECT 
        c.name AS customer,
        COUNT(o.id) AS total_orders,
        SUM(o.total) AS total_revenue,
        AVG(o.satisfaction_score) AS avg_satisfaction
    FROM customers c
    JOIN orders o ON o.customer_id = c.id
    WHERE o.date >= '2025-01-01'
    GROUP BY c.name
    HAVING total_revenue > 100000
    ORDER BY total_revenue DESC
""")

# But CogniMem also adds what SQL CAN'T:
# - Confidence scores for each aggregation
# - Contradictions found (e.g., same order in two different statuses)
# - Insights ("Customer X's satisfaction dropped 20% last quarter")
# - Predictions ("Customer Y is likely to churn based on declining orders")


# ─────────────────────────────────────────────────────
# 6. VIEWS THAT THINK
# ─────────────────────────────────────────────────────

@cm.view("at_risk_customers", refresh="1h")
def at_risk_customers():
    """Customers likely to churn — CogniMem figures out who."""
    all_customers = cm.find(type="customer")
    at_risk = []
    for customer in all_customers:
        # CogniMem REASONS about churn risk using:
        # - Order frequency trends
        # - Satisfaction scores
        # - Support ticket patterns
        # - Industry benchmarks (from its knowledge)
        risk = cm.think_about(f"Is {customer.name} at risk of churning?")
        if risk["probability"] > 0.7:
            at_risk.append({
                "customer": customer,
                "risk_score": risk["probability"],
                "reasons": risk["evidence"],
                "suggested_action": risk["recommendation"]
            })
    return at_risk

# Access it like any view
risky = cm.view("at_risk_customers")

# Or just ask:
cm.ask("Which customers are we likely to lose?")
# → Uses the view, explains the reasoning