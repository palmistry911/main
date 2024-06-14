account = {"fio": "", "password_saved": "", "transactions": [], "balance": 0, "max": 0}


def save(account, file_name):
    with open(file_name, "w") as fout:
        fout.write(account["fio"] + "\n")
        fout.write(account["password_saved"] + "\n")
        fout.write(str(account["balance"]) + "\n")
        fout.write(str(account["max"]) + "\n")
        fout.write(str(len(account["transactions"])) + "\n")
        for transaction in account["transactions"]:
            fout.write(transaction["comment"] + "\n")
            fout.write(str(transaction["amount"]) + "\n")


def load(account, file_name):
    if not path.exists(file_name):
        print("Файл {file_name} не найден. Программа завершена.")
        exit()
    with open(file_name) as fin:
        account["fio"] = fin.readline().strip()
        account["password_saved"] = fin.readline().strip()
        account["balance"] = int(fin.readline().strip())
        account["max"] = int(fin.readline().strip())
        account["transactions"] = []
        transactions_cnt = int(fin.readline().strip())
    for i in range(transactions_cnt):
        comment = fin.readline().strip()
        amount = int(fin.readline().strip())
        transaction = {"comment": comment, "amount": amount}
        account["transactions"].append(transaction)


def input_password():
    password = input("Введите пароль: ")
    if password == account["password_saved"]:
        return False
    else:
        print("пароль неверный")
        return True


def create_transaction(account):
    while True:
        try:
            amount = int(input("Введите сумму транзакции: "))
            break
        except ValueError:
            print("Пожалуйста, введите числовое значение.")
    comment = input("Введите название транзакции: ")
    transaction = {"comment": comment, "amount": amount}
    account["transactions"].append(transaction)
    print("Транзакция создана: " + "\n" + "Название транзакции: " + str(comment) + "\n" + "Сумма транзакции: " + str(
        amount))


def apply_transaction(account):
    rejected_transactions = []
    for transaction in account["transactions"]:
        if transaction["amount"] + account["balance"] >= account["limit"]:
            account["balance"] += transaction["amount"]
            print("Транзакция успешно применена:" + transaction["comment"])
        else:
            print("Транзакция отклонена:" + transaction["comment"])
            rejected_transactions.append(transaction)
    account["transactions"] = rejected_transactions


def get_expected_payments_statistics(transactions):
    payment_stats = {}
    for transaction in account["transactions"]:
        payment_stats[transaction["amount"]] = (payment_stats.get(transaction["amount"], 0) + 1)
    for amount, count in payment_stats.items():
        print(str(amount), "руб:" + str(count), "платеж(а)")


def filter_transactions(transactions, threshold):
    for transaction in transactions:
        if transaction["amount"] >= threshold:
            yield transaction


file_name = "account_data.txt"

restore_data = input("Хотите восстановить данные из файла? (да/нет): ")
if restore_data.lower() == "да":
    load(account, file_name)
else:
    print("Аккаунт не найден.Создайте новый аккаунт")

while True:
    print("\n1.Создать новый аккаунт")
    print("2.Положить деньги на счет")
    print("3.Снять деньги")
    print("4.Вывести баланс на экран")
    print("5.Создание транзакции")
    print("6.Установить лимит")
    print("7.Применить транзакции")
    print("8.Статистика по ожидаемым пополениям")
    print("9.Фильтрация пополнений")
    print("10.Выйти из программы")

    if operation == 1:
        fio = input("Введите ФИО")
        birth_date = int(input("Введите дату рождения"))
        print("Аккаунт создан: " + fio + "(" + str(2024 - birth_date) + "лет)")
        password_saved = input("Создайте пароль")
        balance = 0
        save(account, file_name)

    elif operation == 2:
        increase_balance = int(input("Введите сумму пополнения"))
        balance += increase_balance
        print("Счет пополнен")
        save(account, file_name)

    elif operation == 3:
        if input_password():
            decrease_balance = int(input("Введите сумму снятия: "))
            if account["balance"] >= decrease_balance:
                account["balance"] -= decrease_balance
                print("Снятие прошло успешно.")
            else:
                print("На счете недостаточно средств.")


    elif operation == 4:
        if input_password():
            print("Ваш баланс: " + str(balance))
            save(account, file_name)

    elif operation == 5:
        create_transaction(account)
        save(account, file_name)

    elif operation == 6:
        limit = int(input("Введите сумму лимита"))
        print("Лимит измененен на сумму" + str(limit))
        save(account, file_name)

    elif operation == 7:
        apply_transaction(account)
        save(account, file_name)

    elif operation == 8:
        get_expected_payments_statistics(account)
        save(account, file_name)

    elif operation == 9:
        threshold = float(input("Введите сумму для фильтрации: "))
        if threshold < 0:
            print("Сумма не может быть отрицательной.")
        else:
            filtered_transactions = filter_transactions(transactions, threshold)
            print("Транзакции не меньше введенного числа:")
            for transactions in filtered_transactions:
                print(transactions["comment"])

    elif operation == 10:
        print("Всего доброго!")
        save(account, file_name)
        break
    else:
        print("Неверная операция")
