from src.transaction import Transaction
from src.utxo_manager import UTXOManager


def validate_transaction(tx: Transaction, utxo_manager: UTXOManager, spent_utxos: set[(str, int)]):
    inputs = tx.inputs
    outputs = tx.outputs
    
    for out in outputs:
        if out.amount < 0:
            return False, "Negative output amount"

    input_sum = 0
    input_keys = []
    
    for inp in inputs:
        key = (inp.prev_tx, inp.index)
        
        if not utxo_manager.exists(*key):
            return False, f"Input {key} UTXO does not exist"

        utxo = utxo_manager.get_utxo(*key)
        
        if utxo.get("owner") != inp.owner:
            return False, f"UTXO not owned by the owner {inp.owner}. It belongs to {utxo.get("owner")}"

        if key in spent_utxos:
            return False, f"UTXO has already been spent and waiting in the mempool"

        if key in input_keys:
            return False, "Same UTXO repeated twice"

        input_keys.append(key)
        input_sum += utxo.get("amount")

    output_sum = sum(out.amount for out in outputs)

    if input_sum < output_sum:
        return False, f"Can't create new UTXO from void. Input {input_sum}, Output {output_sum}"

    return True, "ok"