select Scheduler{
    type_tag,
    name,
    status,
    date_beginning,
    date_ending,
    notes,
}filter .id = <uuid>$id
