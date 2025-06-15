select Scheduler{
    type_entry := .type,
    name,
    status,
    date,
    beginning_time,
    ending_time,
    notes,
    origin: {id}
}filter .id = <uuid>$id
