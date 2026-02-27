# ═══════════════════════════════════════════════════════════
# THE SAME QUESTION, SEVEN DIFFERENT LANGUAGES
# CogniMem understands ALL of them
# ═══════════════════════════════════════════════════════════

from cognimem import CogniMem

cm = CogniMem()

# ──── SQL Person ────
cm.query("""
    SELECT name, tensile_strength, cost_per_kg
    FROM materials
    WHERE corrosion_resistance = 'excellent'
      AND tensile_strength > 400
    ORDER BY cost_per_kg ASC
    LIMIT 5
""")
# Returns: familiar SQL-style rows with columns
# ┌──────────┬──────────────────┬─────────────┐
# │ name     │ tensile_strength │ cost_per_kg │
# ├──────────┼──────────────────┼─────────────┤
# │ SS316L   │ 515 MPa          │ 4.50        │
# │ SS304    │ 505 MPa          │ 3.80        │
# └──────────┴──────────────────┴─────────────┘

# ──── MongoDB Person ────
cm.query({
    "collection": "materials",
    "filter": {
        "properties.corrosion_resistance": "excellent",
        "properties.tensile_strength": {"$gt": 400}
    },
    "sort": {"properties.cost_per_kg": 1},
    "limit": 5
})
# Returns: JSON documents like MongoDB

# ──── Graph Person (Cypher-style) ────
cm.query("""
    MATCH (m:material)-[:resists]->(c:corrosion)
    WHERE m.tensile_strength > 400
    RETURN m.name, m.tensile_strength
    ORDER BY m.cost_per_kg
""")
# Returns: nodes and relationships

# ──── Natural Language Person ────
cm.ask("What are the cheapest materials that resist corrosion "
       "and have tensile strength above 400 MPa?")
# Returns: "Based on 23 concepts in the engineering domain,
#           the most cost-effective corrosion-resistant materials are:
#           1. SS304 ($3.80/kg, 505 MPa) — confidence: 0.95
#           2. SS316L ($4.50/kg, 515 MPa) — confidence: 0.97
#           Note: SS316L has better marine corrosion resistance
#           despite higher cost. Consider your environment."

# ──── GraphQL Person ────
cm.query("""
    {
        materials(
            where: { corrosion_resistance: "excellent", tensile_strength_gt: 400 }
            orderBy: cost_per_kg_ASC
            first: 5
        ) {
            name
            tensile_strength
            cost_per_kg
            relations { type target { name } }
        }
    }
""")
# Returns: GraphQL-shaped response

# ──── Python Person (Pandas-style) ────
df = cm.concepts.where(
    type="material",
    corrosion_resistance="excellent"
).filter(
    tensile_strength__gt=400
).sort("cost_per_kg").limit(5).to_dataframe()

# ──── CQL Person (CogniMem native) ────
cm.cql("FIND materials WITH corrosion_resistance = 'excellent' "
       "AND tensile_strength > 400 "
       "SORTED BY cost_per_kg "
       "EXPLAIN WHY "          # <── CogniMem-only: explains reasoning
       "CHECK CONTRADICTIONS")  # <── CogniMem-only: flags issues
# Returns: results + WHY these are the best + any contradictions found