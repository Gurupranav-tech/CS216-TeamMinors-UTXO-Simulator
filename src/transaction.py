from dataclasses import dataclass
import time
import random


@dataclass
class TransactionInput:
    prev_tx: str
    index: int
    owner: str


@dataclass
class TransactionOutput:
    amount: float
    address: str


@dataclass
class Transaction:
    tx_id: str
    inputs: list[TransactionInput]
    outputs: list[TransactionOutput]

    @staticmethod
    def generate_tx_id():
        return f"tx_{int(time.time())}_{random.randint(1000, 9999)}"