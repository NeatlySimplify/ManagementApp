select Record {
    name,
    service_id,
    status,
    optional_status,
    type_tag,
    str_value:=to_str(.value),
    notes,
    entity: {
        id,
        name,
    },
    event: {
        id,
        name,
        type_tag,
        status,
        date_beginning,
        date_ending
    },
    movement: {
        id,
        type_tag,
        value,
        installment,
    }
} filter .id = <uuid>$id
