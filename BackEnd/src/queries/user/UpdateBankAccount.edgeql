update BankAccount filter .id = <uuid>$bank_account set {
    bank_name:= <optional str>$bank_name ?? .bank_name,
    account_name:= <optional str>$account_name ?? .account_name,
    ignore_on_totals:= <optional bool>$ignore_on_totals ?? .ignore_on_totals,
    category_tag:= <optional str>$category ?? .category_tag,
    type_tag:= <optional str>$type ?? .type_tag,
    notes:=<optional json>$notes ?? .notes,
}
