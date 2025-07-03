insert Scheduler {
    type_tag:= <str>$type_tag,
    name:= <str>$name,
    status:= <optional bool>$status,
    date:= <cal::local_date>$date,
    beginning_time:= <optional cal::local_time>$beginning_time,
    ending_time:= <optional cal::local_time>$ending_time,
    notes:=<optional json>$notes,
}
