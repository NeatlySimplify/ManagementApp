select Entity {
    email,
    type_tag,
    document_type,
    status,
    document,
    name,
    sex,
    relationship_status,
    notes,
    birth,
    phone: {*},
    address: {*}
} filter .id = <uuid>$entity
