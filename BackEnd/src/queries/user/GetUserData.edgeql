with user_id:= (<uuid>$id),
select InternalUser {
    name,
    email,
    settings: {
        id,
        account_types,
        default_bank_account: { id, bank_name, account_name, balance },
        record_title,
        movement_title,
        entity_title,
        entity_types,
        entity_id_types,
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
        type,
        value,
        installment,
    },
    entity: {
        id,
        name,
        email,
        govt_id,
        type,
        id_type,
        status,
        address: {
            state,
            city,
        },
        phone: {
            id,
            number,
        }
    },
    paymente_income:{
        id,
        name,
        type,
        value,
        payment_date,
        status,
        movement:{id}
    },
    paymente_expense:{
        id,
        name,
        type,
        value,
        payment_date,
        status,
        movement:{id}
    },
    record: {
        id,
        name,
        id_service,
        active,
        status,
        type,
    },
    event:{
        id,
        type,
        name,
        status,
        date,
    },
    account: {
        id,
        bank_name,
        account_name,
        balance,
    },
    entityNUM:= (select EntityNum(user_id)),
    recordNUM:= (select RecordNum(user_id)),
    balanceTOTAL:= (select balanceTotal(user_id))
} filter .id = user_id
