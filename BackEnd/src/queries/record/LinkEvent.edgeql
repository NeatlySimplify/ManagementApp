update Record filter .id = <uuid>$record_id set {
    event += (select Scheduler filter .id = <uuid>$schedule_id)
}
