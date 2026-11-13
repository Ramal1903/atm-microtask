import datetime

# ==========================================
# ATM SİSTEMİ - İLKİN PARAMETRLƏR VƏ DƏYİŞƏnlər
# ==========================================
atm_cash = 10000.00
current_date = datetime.date.today().strftime("%Y-%m-%d")
stored_date = "2026-10-25"

# İstifadəçi 1 Məlumatları
acc1_no = "10010001"
correct_pin = "1234"
balance1 = 3000.00
pin_attempts = 3
card_blocked = False

# İstifadəçi 1 Üçün Limitlər və Tarixçə
deposit_used1 = 0.00
deposit_limit1 = 2000.00
cash_withdrawn1 = 0.00
cash_limit1 = 1000.00
fee_free_limit1 = 100.00  # Nümunə şəkildəki vizual tələb üçün
outgoing_transfers1 = 0
transfer_limit1 = 5
history1 = []

# İstifadəçi 2 Məlumatları (Köçürmə üçün)
acc2_no = "10010002"
balance2 = 1500.00
history2 = []

# ==========================================
# 1. GÜNDƏLİK LİMİTLƏRİN AVTOMATİK SIĞIRLANMASI (Tarix yoxlanışı)
# ==========================================
if current_date != stored_date:
    deposit_used1 = 0.00
    cash_withdrawn1 = 0.00
    outgoing_transfers1 = 0
    stored_date = current_date

print("--- ATM-Ə XOŞ GƏLDİNİZ ---")

# ==========================================
# 2. PIN KODUN YOXLANILMASI (3 Cəhd bloku)
# ==========================================
while pin_attempts > 0 and not card_blocked:
    entered_pin = input("PIN kodunuzu daxil edin: ")
    if entered_pin == correct_pin:
        print("Giriş uğurludur!")
        break
    else:
        pin_attempts -= 1
        print(f"Səhv PIN! Qalan cəhd sayı: {pin_attempts}")
        if pin_attempts == 0:
            card_blocked = True
            print("Çoxsaylı səhv cəhd! Kartınız bloklandı.")

# Əgər kart bloklanmayıbsa, əsas əməliyyatlara keçirik
if not card_blocked:
    print("\n==========================================")
    print(f" Hesab nömrəniz: {acc1_no}")
    print(f" Cari balansınız: {balance1:.2f} AZN")
    print("==========================================")

    # ==========================================
    # 3. NAĞD DEPOZİT QOYMA ƏMƏLİYYATI
    # ==========================================
    print("\n--- NAĞD DEPOZİT QOYMA ---")
    deposit_amount = float(input("Hesaba yatırmaq istədiyiniz məbləğ (AZN): "))

    if deposit_amount > 0 and (deposit_used1 + deposit_amount) <= deposit_limit1:
        b_before = balance1
        balance1 += deposit_amount
        atm_cash += deposit_amount
        deposit_used1 += deposit_amount
        b_after = balance1

        # Unikal ID və Tarix yaradılması
        txn_id = f"TXN000{len(history1) + 1}"
        txn_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        history1.append({
            "id": txn_id,
            "date": txn_date,
            "type": "Deposit",
            "amount": deposit_amount,
            "before": b_before,
            "after": b_after,
            "recipient": "N/A"
        })
        print(f"Depozit uğurludur! Yeni balans: {balance1:.2f} AZN")
    else:
        print("Xəta: Limit aşımı və ya səhv məbləğ daxil edildi!")

    # ==========================================
    # 4. ATM-DƏN PUL ÇIXARMA ƏMƏLİYYATI
    # ==========================================
    print("\n--- ATM-DƏN PUL ÇIXARMA ---")
    withdraw_amount = float(input("Çıxarmaq istədiyiniz məbləği daxil edin (AZN): "))

    if withdraw_amount > 0 and withdraw_amount <= balance1 and withdraw_amount <= atm_cash and (cash_withdrawn1 + withdraw_amount) <= cash_limit1:
        b_before = balance1
        balance1 -= withdraw_amount
        atm_cash -= withdraw_amount
        cash_withdrawn1 += withdraw_amount
        b_after = balance1

        txn_id = f"TXN000{len(history1) + 1}"
        txn_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        history1.append({
            "id": txn_id,
            "date": txn_date,
            "type": "Withdrawal",
            "amount": -withdraw_amount,
            "before": b_before,
            "after": b_after,
            "recipient": "N/A"
        })
        print(f"Pul çıxarıldı! Yeni balans: {balance1:.2f} AZN")
    else:
        print("Xəta: Kifayət qədər balans, ATM nağd pulu yoxdur və ya limit aşımı!")

    # ==========================================
    # 5. İSTİFADƏÇİLƏR ARASINDA KÖÇÜRMƏ ƏMƏLİYYATI
    # ==========================================
    print("\n--- İSTİFADƏÇİLƏR ARASINDA KÖÇÜRMƏ ---")
    recipient_acc = input("Alıcının hesab nömrəsini daxil edin: ")
    
    if recipient_acc == acc2_no:
        transfer_amount = float(input("Köçürmək istədiyiniz məbləğ (AZN): "))
        
        if transfer_amount > 0 and transfer_amount <= balance1 and outgoing_transfers1 < transfer_limit1:
            print(f"Sender: user01")
            print(f"Recipient account: {recipient_acc}")
            print(f"Recipient: user02")
            print(f"Amount: {transfer_amount:.2f} AZN")
            confirm = input("Confirm transfer (Y/N): ").strip().upper()

            if confirm == 'Y':
                # Göndərənin məlumatları
                b_before_sender = balance1
                balance1 -= transfer_amount
                b_after_sender = balance1
                outgoing_transfers1 += 1

                txn_id_s = f"TXN000{len(history1) + 1}"
                txn_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                history1.append({
                    "id": txn_id_s,
                    "date": txn_date,
                    "type": "Transfer Sent",
                    "amount": -transfer_amount,
                    "before": b_before_sender,
                    "after": b_after_sender,
                    "recipient": recipient_acc
                })

                # Alıcının məlumatları
                b_before_rec = balance2
                balance2 += transfer_amount
                b_after_rec = balance2

                txn_id_r = f"TXN000{len(history2) + 1}"
                history2.append({
                    "id": txn_id_r,
                    "date": txn_date,
                    "type": "Transfer Received",
                    "amount": transfer_amount,
                    "before": b_before_rec,
                    "after": b_after_rec,
                    "recipient": acc1_no
                })

                print("Transfer successful.")
                print(f"Sender new balance: {balance1:.2f} AZN")
            else:
                print("Transfer ləğv edildi.")
        else:
            print("Xəta: Balans kifayət deyil və ya köçürmə limiti dolub!")
    else:
        print("Xəta: Belə hesab nömrəsi tapılmadı!")

    # ==========================================
    # 6. GÜNDƏLİK LİMİTLƏR EKRANI
    # ==========================================
    print("\n--- GÜNDƏLİK LİMİTLƏR EKRANI ---")
    print("=========== DAILY LIMITS ===========")
    print(f"Deposit used:          {deposit_used1:.2f} / {deposit_limit1:.2f} AZN")
    print(f"Deposit remaining:     {deposit_limit1 - deposit_used1:.2f} AZN")
    print(f"Cash withdrawn:        {cash_withdrawn1:.2f} / {cash_limit1:.2f} AZN")
    print(f"Cash withdrawal remaining: {cash_limit1 - cash_withdrawn1:.2f} AZN")
    print(f"Fee-free cash remaining: {fee_free_limit1:.2f} AZN")
    print(f"Outgoing transfers:    {outgoing_transfers1} / {transfer_limit1}")
    print("====================================")

    # ==========================================
    # 7. ƏMƏLİYYAT TARİXÇƏSİ EKRANI
    # ==========================================
    print("\n--- ƏMƏLİYYAT TARİXÇƏSİ ---")
    print("User01 Tarixçəsi:")
    for txn in history1:
        print(f"ID: {txn['id']}")
        print(f"Date: {txn['date']}")
        print(f"Type: {txn['type']}")
        print(f"Amount: {txn['amount']:.2f} AZN")
        print(f"Balance before: {txn['before']:.2f} AZN")
        print(f"Balance after: {txn['after']:.2f} AZN")
        if txn['recipient'] != "N/A":
            print(f"Recipient account: {txn['recipient']}")
        print("-" * 30)