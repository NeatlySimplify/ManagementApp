select Scheduler{
    type,
    name,
    status,
    date,
    beginning_time,
    ending_time,
    details,
    origin: {id}
}filter .id = <uuid>$id
