import json
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "data.json")

DEFAULT_ATM = 5000.0   # ATM-dəki pul (AZN)
ACC_KEY = "ID"         # data.json-da hesab nömrəsinin açarı

# data.json-da bütün pul məbləğləri AZN ilə saxlanır (məs. 2500.00).
# Əsas kod isə qəpiklə işləyir, ona görə burada çevrilir.


def _load():
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def _save(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def _q(azn):
    return int(round(float(azn) * 100))


def _azn(q):
    return round(q / 100, 2)


def _users(data):
    u = data["users"]
    return list(u.values()) if isinstance(u, dict) else u


def _find_user(data, current_user):
    name = current_user["username"] if isinstance(current_user, dict) else current_user
    for u in _users(data):
        if u["username"] == name:
            return u
    raise KeyError(f"User not found: {name}")


def _find_by_account(data, acc):
    for u in _users(data):
        if str(u.get(ACC_KEY)) == str(acc):
            return u
    return None


def _prepare(data, user):
    # Çatışmayan sahələri doldurur, yeni gün başlayıbsa limitləri sıfırlayır
    user.setdefault("balance", 0.0)
    user.setdefault("deposit_used", 0)
    user.setdefault("withdraw_used", 0)
    user.setdefault("transfers_used", 0)
    user.setdefault("history", [])
    today = str(date.today())
    if user.get("deposit_date") != today:
        user["deposit_date"] = today
        user["deposit_used"] = 0
        user["withdraw_used"] = 0
        user["transfers_used"] = 0
    data.setdefault("atm", DEFAULT_ATM)


def load_state(current_user):
    data = _load()
    user = _find_user(data, current_user)
    _prepare(data, user)
    _save(data)
    return {
        "balance": _q(user["balance"]),
        "atm": _q(data["atm"]),
        "deposit_used": _q(user["deposit_used"]),
        "withdraw_used": _q(user["withdraw_used"]),
        "transfers_used": user["transfers_used"],
    }


def save_operation(current_user, op_name, amount, fee,
                   balance_before, balance_after, atm, kind, used_today):
    # bütün məbləğlər qəpiklə gəlir, fayla AZN ilə yazılır
    data = _load()
    user = _find_user(data, current_user)
    _prepare(data, user)

    user["balance"] = _azn(balance_after)
    data["atm"] = _azn(atm)
    if kind == "deposit":
        user["deposit_used"] = _azn(used_today)
    elif kind == "withdraw":
        user["withdraw_used"] = _azn(used_today)

    user["history"].append({
        "type": op_name,
        "amount": _azn(amount),
        "fee": _azn(fee),
        "balance_before": _azn(balance_before),
        "balance_after": _azn(balance_after),
        "date": str(date.today()),
    })
    _save(data)


# ---------------- transfer ----------------

def load_transfer_state(current_user, recipient_acc):
    data = _load()
    sender = _find_user(data, current_user)
    _prepare(data, sender)
    rec = _find_by_account(data, recipient_acc)
    if rec is sender:      # özünə köçürmə olmaz
        rec = None
    if rec is not None:
        _prepare(data, rec)
    _save(data)
    return {
        "username1": sender["username"],
        "acc1_no": sender.get(ACC_KEY),
        "balance1": _q(sender["balance"]),                # qəpik
        "outgoing_transfers1": sender["transfers_used"],
        "history1": sender["history"],
        "username2": rec["username"] if rec else None,
        "acc2_no": rec.get(ACC_KEY) if rec else None,
        "balance2": _q(rec["balance"]) if rec else 0,     # qəpik
        "history2": rec["history"] if rec else [],
    }


def _to_record(e):
    # köçürmə kodundakı yazını data.json formatına çevirir (AZN)
    return {
        "id": e["id"],
        "date": e["date"],
        "type": e["type"],
        "amount": round(abs(e["amount"]), 2),
        "fee": 0,
        "balance_before": round(e["before"], 2),
        "balance_after": round(e["after"], 2),
        "recipient": e["recipient"],
    }


def save_transfer_state(current_user, recipient_acc, balance1, balance2,
                        outgoing_transfers1, entry1, entry2):
    # balance1, balance2 AZN ilə gəlir
    data = _load()
    sender = _find_user(data, current_user)
    rec = _find_by_account(data, recipient_acc)
    _prepare(data, sender)
    _prepare(data, rec)
    sender["balance"] = round(balance1, 2)
    rec["balance"] = round(balance2, 2)
    sender["transfers_used"] = outgoing_transfers1
    sender["history"].append(_to_record(entry1))
    rec["history"].append(_to_record(entry2))
    _save(data)
def load_history(username):
    data = load_data()

    for user in data["users"]:
        if user["username"] == username:
            return user.get("history", [])

    return []