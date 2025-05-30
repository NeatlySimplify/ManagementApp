with user:= <uuid>$user,
add_bank:=(
    insert BankAccount {
        bank_name:= <str>$bank_name,
        account_name:= <str>$account_name,
        balance:= <decimal>$balance,
        details:= <optional json>$details,
        category:= <optional str>$category,
        ignore_on_totals:= <bool>$ignore_on_totals,
        type:= <optional str>$type
    }
),
update_user:= (
    update InternalUser filter .id = <uuid>$user set {
        account += add_bank
    }
)
select add_bank{id};
