class EngineType(Enum):
    """Available storage engine types"""
    MASE = "mase"           # Default - high-performance Rust engine
    CAM = "cam"             # Content-Addressable Memory
    STORAGE = "storage"     # Original file-based engine