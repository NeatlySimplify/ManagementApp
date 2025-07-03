with selected_user:= (select global current_user),
converted := (select Account filter .id = selected_user.id),
select converted{
    name,
    email,
    auth:= true,
    total_balance:= to_str(sum((select converted.account.balance))),
    settings: {
        id,
        account_types,
        default_bank_account: {id},
        record_title,
        movement_title,
        entity_title,
        entity_types,
        entity_document_types,
        contact_number_types,
        record_types,
        record_status,
        movement_income_types,
        movement_expense_types,
        scheduler_types,
        movement_cycle_types
    },
    movement: {
        id,
        type_tag,
        value_str:= to_str(.value),
        installment,
        payment: {
            id,
            status,
            payment_date,
        }
    },
    entity: {
        id,
        name,
        email,
        document,
        type_tag,
        document_type,
        status,
        address: {
            state,
            city,
        },
        phone: {number}
    },
    payment:{
        id,
        name,
        type_tag,
        value_str:=to_str(.value),
        payment_date,
        status,
        movement:{id}
    },
    record: {
        id,
        name,
        service_id,
        status,
        optional_status,
        type_tag,
    },
    event:{
        id,
        type_tag,
        name,
        status,
        date,
    },
    account: {
        id,
        bank_name,
        account_name,
        balance_str:=to_str(.balance),
    },
    grouping: {
        id,
        name,
    },
    collaborator_pool: {
        id,
        name,
        email
    }
}
