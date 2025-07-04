insert Scheduler {
    type_tag:= <str>$type_tag,
    name:= <str>$name,
    status:= <optional bool>$status,
    date_beginning:= <cal::local_datetime>$date,
    date_ending:= <optional cal::local_datetime>$ending_time,
    notes:=<optional json>$notes,
}
