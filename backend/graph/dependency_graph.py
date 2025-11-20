GRAPH = {
    "utils/crypto.py": ["services/billing/charge.py", "lib/logger.py"],
    "services/billing/charge.py": ["services/payments/pay_client.py"],
    "services/payments/pay_client.py": ["lib/network.py"],
    "lib/logger.py": [],
    "lib/network.py": []
}

FILE_TO_MODULE = {
    "utils/crypto.py": "lib:utils",
    "services/billing/charge.py": "service:billing",
    "services/payments/pay_client.py": "service:payments",
    "lib/logger.py": "lib:logger",
    "lib/network.py": "lib:network"
}

MODULE_METADATA = {
    "lib:utils": {"coverage": 65, "criticality": 0.3, "churn": 2},
    "service:billing": {"coverage": 45, "criticality": 0.9, "churn": 6},
    "service:payments": {"coverage": 80, "criticality": 0.7, "churn": 1},
    "lib:logger": {"coverage": 90, "criticality": 0.4, "churn": 0},
    "lib:network": {"coverage": 70, "criticality": 0.5, "churn": 1}
}
