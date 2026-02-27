    """
    The replacement for vector databases.
    Stores CONCEPTS, not text chunks.
    Supports REASONING, not just similarity search.

    Usage:
        memory = ConceptMemory("data/")
        memory.store_concept(steel_concept)
        results = memory.query(type="material", domain_includes="marine",
                               property_gt=("tensile_strength", 400))
    """