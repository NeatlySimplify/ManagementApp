update Record filter .id = <uuid>$record set {
    event -= (select Scheduler filter .id = <uuid>$schedule_id)
}
