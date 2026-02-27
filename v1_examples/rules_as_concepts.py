# Rules aren't code — they're CONCEPTS
# That means CogniMem's 6 processes work on them:
# - Sentinel detects conflicting rules
# - Gardener removes expired rules  
# - Prophet anticipates which rules will fire
# - Skeptic challenges rules that seem wrong
# - Connector finds rules from other domains that might apply
# - Librarian indexes rules for instant lookup

cm.store_concept(Concept(
    name="bulk_discount_rule",
    concept_type="business_rule",
    domains=["sales", "pricing"],
    properties=[
        ConceptProperty(key="condition", value="order.quantity > 100"),
        ConceptProperty(key="action", value="apply_discount(10%)"),
        ConceptProperty(key="effective_from", value="2026-01-01"),
        ConceptProperty(key="effective_until", value="2026-12-31"),
        ConceptProperty(key="approved_by", value="finance_team"),
        ConceptProperty(key="priority", value="100"),
    ],
    relations=[
        ConceptRelation(
            relation_type="overrides",
            target_concept_id="standard_pricing_rule",
            confidence=1.0,
            evidence="Approved in Q4 2025 pricing review"
        )
    ],
    confidence=1.0,
    sources=["finance_team_approval_2025_q4"]
))