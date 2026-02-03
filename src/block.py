from src.mempool import Mempool
from src.utxo_manager import UTXOManager
from src.transaction import Transaction


def mine_block(miner_address: str, mempool: Mempool, utxo_manager: UTXOManager):
    transactions: list[Transaction] = mempool.get_top_transactions()
    
    if not transactions:
        print("No Transactions to mine")
        return False
    
    total_fee = 0.0
    mined_tx_ids = []
    
    for tx in transactions:
        input_sum = 0
        clear_inputs = []
        
        for inp in tx.inputs:
            utxo = utxo_manager.get_utxo(inp.prev_tx, inp.index)
            input_sum += utxo.get("amount")
            clear_inputs.append((inp.prev_tx, inp.index))

        output_sum = sum(out.amount for out in tx.outputs)

        total_fee += input_sum - output_sum

        for inp in clear_inputs:
            utxo_manager.remove_utxo(*inp)

        for i, out in enumerate(tx.outputs):
            utxo_manager.add_utxo(tx.tx_id, i, out.amount, out.address)

        mined_tx_ids.append(tx.tx_id)

    if total_fee > 0 or len(mined_tx_ids) > 0:
        coinbase_tx_id = f"coinbase-{Transaction.generate_tx_id()}"
        utxo_manager.add_utxo(coinbase_tx_id, 0, total_fee, miner_address)
        print(f"Miner received fee of {total_fee}")

    for tx_id in mined_tx_ids:
        mempool.remove_transaction(tx_id)

    return True