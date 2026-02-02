class UTXOManager:
    def __init__(self):
        self.utxo_set = {}
        
    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
        ...
        
    def remove_utxo(self, tx_id: str, index: int):
        ...

    def get_balance(self, owner: str) -> float:
        ...
        
    def exists(self, tx_id: str, index: int) -> bool:
        ...
        
    def get_utxos_for_owner(self, owner: str) -> list:
        ...