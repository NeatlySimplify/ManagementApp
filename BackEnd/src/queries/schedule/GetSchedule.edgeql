select Scheduler{
    type_tag,
    name,
    status,
    date,
    beginning_time,
    ending_time,
    notes,
}filter .id = <uuid>$id
