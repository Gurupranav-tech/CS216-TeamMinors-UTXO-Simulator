class UTXOManager:
    def __init__(self):
        self.utxo_set = {
             ("genesis", 0) : {"amount": 50.0 , "owner": "Alice"} ,
             ("genesis", 1) : {"amount": 30.0 , "owner": "Bob"},
             ("genesis", 2) : {"amount": 20.0 , "owner": "Charlie"} ,
             ("genesis", 3) : {"amount": 10.0 , "owner": "David"} ,
             ("genesis", 4) : {"amount": 5.0 , "owner": "Eve"}
        }
        
    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
        self.utxo_set[(tx_id, index)] = {
            "amount": amount,
            "owner": owner
        }

        
    def remove_utxo(self, tx_id: str, index: int):
        del self.utxo_set[(tx_id, index)]

    def get_balance(self, owner: str) -> float:
        balance = 0.0
        for utxo in self.utxo_set.values():
            if utxo["owner"] == owner:
                balance += utxo["amount"]
        return balance
        
    def exists(self, tx_id: str, index: int) -> bool:
        return (tx_id,index) in self.utxo_set
        
    def get_utxos_for_owner(self, owner: str) -> list:
        utxos =[]
        for (tx_id,index) in self.utxo_set:
            if(self.utxo_set[(tx_id,index)] ["owner"] ==owner):
                utxos.append( (tx_id,index,self.utxo_set[(tx_id,index)]["amount"]))
        
        return utxos