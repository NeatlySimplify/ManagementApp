select Record {
    name,
    id_service,
    active,
    status,
    type,
    value,
    details,
    entity: {
        id,
        name,
    },
    event: {
        id,
        name,
        type,
        status,
        date
    },
    movement: {
        id,
        type,
        value,
        installment,
    }
} filter .id = <uuid>$id
