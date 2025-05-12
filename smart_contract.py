import json
import os
from typing import Dict

def load_json(path: str) -> dict:
    """Load JSON data from file, create if doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return {}
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_json(path: str, data: dict) -> None:
    """Save data to JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

class SmartContract:
    """Base structure for smart contract simulation."""
    def __init__(self, tokens_file: str, proposals_file: str, signers_file: str):
        self.tokens_file = tokens_file
        self.proposals_file = proposals_file
        self.signers_file = signers_file

        self.tokens = load_json(tokens_file)
        self.proposals = load_json(proposals_file)
        self.signers = load_json(signers_file)
