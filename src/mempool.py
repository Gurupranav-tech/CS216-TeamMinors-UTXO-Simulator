from src.transaction import Transaction
from src.utxo_manager import UTXOManager
from src.validator import validate_transaction


class Mempool:
    def __init__(self, max_size: int = 50):
        self.transactions: list[Transaction] = []
        self.spent_utxos = set()
        self.max_size = max_size

    def add_transaction(self, tx: Transaction, utxo_manager: UTXOManager) -> (bool, str):
        valid, msg = validate_transaction(tx, utxo_manager, self.spent_utxos)
        if not valid:
            return valid, msg

        if len(self.transactions) > self.max_size:
            return False, "Max size of mempool reached...."

        self.transactions.append(tx)

        for inp in tx.inputs:
            self.spent_utxos.add((inp.prev_tx, inp.index))

        return True, "Transaction Added to mempool"
        
    def remove_transaction(self, tx: str):
        transaction = None

        for trans in self.transactions:
            if trans.tx_id == tx:
                transaction = trans

        if transaction is None:
            return
        
        self.transactions.remove(transaction)
        for inp in transaction.inputs:
            key = (inp.prev_tx, inp.index)
            if key in self.spent_utxos:
                self.spent_utxos.remove(key)
        
    def get_top_transactions(self, n: int=5) -> list[Transaction]:
        return self.transactions[:n]

    def get_transactions(self) -> list[Transaction]:
        return self.transactions
        
    def clear(self):
        self.transactions.clear()
        self.spent_utxos.clear()