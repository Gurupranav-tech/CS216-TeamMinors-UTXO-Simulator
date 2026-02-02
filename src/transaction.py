from pydantic import BaseModel


class TransactionInput(BaseModel):
    prev_tx: str
    index: int
    owner: str


class TransactionOutput(BaseModel):
    amount: float
    address: str


class Transaction(BaseModel):
    tx_id: str
    inputs: list[TransactionInput]
    outputs: list[TransactionOutput]