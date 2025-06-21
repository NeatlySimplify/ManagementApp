with user:= (select global current_user_obj),
setup:=(
    insert UserSettings {
        default_bank_account:= assert_single((select BankAccount filter .id = <uuid>$bank_account)),
        record_title := <str>$record_title,
        movement_title := <str>$movement_title,
        entity_title := <str>$entity_title,
    }
)
update user set {
    settings:= setup
}
