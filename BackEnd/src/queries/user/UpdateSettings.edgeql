with user:=assert_single((select InternalUser filter .id = <uuid>$user)).settings,
bank_account:= <optional uuid>$bank_account,
update user set {
    default_bank_account:= assert_single((select BankAccount filter .id = bank_account)) if exists bank_account else .default_bank_account,
    record_title := <optional str>$record_title ?? .record_title,
    movement_title := <optional str>$movement_title ?? .movement_title,
    entity_title := <optional str>$entity_title ?? .entity_title,
    account_types:= <optional array<str>>$account_types ?? .account_types,
    entity_types:= <optional array<str>>$entity_types ?? .entity_types,
    entity_id_types:=<optional array<str>>$entity_id_types ?? .entity_id_types,
    contact_number_types:= <optional array<str>>$contact_number_types ?? .contact_number_types,
    record_types:= <optional array<str>>$record_types ?? .record_types,
    record_status:= <optional array<str>>$record_status ?? .record_status,
    movement_income_types:= <optional array<str>>$movement_income_types ?? .movement_income_types,
    movement_expense_types:= <optional array<str>>$movement_expense_types ?? .movement_expense_types,
    scheduler_types:= <optional array<str>>$scheduler_types ?? .scheduler_types,
    movement_cycle_types:= <optional array<str>>$movement_cycle_types ?? .movement_cycle_types
}
