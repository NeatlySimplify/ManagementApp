update Scheduler filter .id = <uuid>$id set {
    name:= <optional str>$name ?? .name,
    type:= <optional str>$type ?? .type,
    status:= <optional bool>$status ?? .status,
    date:= <optional cal::local_date>$date ?? .date,
    beginning_time:= <optional cal::local_time>$beginning_time ?? .beginning_time,
    ending_time:= <optional cal::local_time>$ending_time ?? .ending_time,
}
