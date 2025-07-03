with add_bank:=(
    insert BankAccount {
        bank_name:= <str>$bank_name,
        account_name:= <str>$account_name,
        balance:= to_decimal(<str>$balance, 'FM999999999999.99'),
        category_tag:= <optional str>$category,
        ignore_on_totals:= <bool>$ignore_on_totals,
        type_tag:= <optional str>$type,
        notes:= <optional json>$notes,
    }
),
select (add_bank){id};
