import sys

def main():
    lines = sys.stdin.read().strip().splitlines()
    idx = 0

    # 1. Non-fraudulent codes (read but not used)
    non_fraud_codes = set(lines[idx].split(","))
    idx += 1

    # 2. Fraudulent codes
    fraud_codes = set(lines[idx].split(","))
    idx += 1

    # 3. MCC thresholds
    mcc_count = int(lines[idx].strip())
    idx += 1
    mcc_threshold = {}
    for _ in range(mcc_count):
        mcc, val = lines[idx].split(",")
        mcc_threshold[mcc] = int(val)
        idx += 1

    # 4. Merchants table (account_id → mcc)
    merchant_count = int(lines[idx].strip())
    idx += 1
    merchant_mcc = {}
    for _ in range(merchant_count):
        account_id, mcc = lines[idx].split(",")
        merchant_mcc[account_id] = mcc
        idx += 1

    # 5. Minimum total transactions
    min_transactions = int(lines[idx].strip())
    idx += 1

    # 6. Charges
    charge_count = int(lines[idx].strip())
    idx += 1

    total_tx = {}
    fraud_tx = {}

    for _ in range(charge_count):
        parts = lines[idx].split(",")
        idx += 1

        # Format: CHARGE,charge_id,account_id,amount,code
        account_id = parts[2]
        code = parts[4]

        total_tx[account_id] = total_tx.get(account_id, 0) + 1

        if code in fraud_codes:
            fraud_tx[account_id] = fraud_tx.get(account_id, 0) + 1

    # Determine fraudulent merchants
    fraudulent_merchants = []

    for account_id, total in total_tx.items():
        if total < min_transactions:
            continue

        fraud_count = fraud_tx.get(account_id, 0)
        mcc = merchant_mcc.get(account_id)

        # Skip if merchant has no MCC mapping
        if mcc not in mcc_threshold:
            continue

        threshold = mcc_threshold[mcc]

        if fraud_count > threshold:
            fraudulent_merchants.append(account_id)

    # Sort & output
    fraudulent_merchants.sort()
    print(",".join(fraudulent_merchants))


if __name__ == "__main__":
    main()
