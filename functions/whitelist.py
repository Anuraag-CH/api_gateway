from typing import List, Dict

def load_whitelist() -> Dict[str, List[str]]:
    # In a real-world scenario, this would load from a database or configuration file
    return {
        "service1": ["GET", "POST"],
        "service2": ["GET", "PUT", "DELETE"],
    }

def is_whitelisted(service_name: str, method: str) -> bool:
    whitelist = load_whitelist()
    return service_name in whitelist and method in whitelist[service_name]
