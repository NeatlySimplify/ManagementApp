update Scheduler filter .id = <uuid>$id set {
    name:= <optional str>$name ?? .name,
    type_tag:= <optional str>$type_tag ?? .type_tag,
    status:= <optional bool>$status ?? .status,
    date_beginning:= <optional cal::local_datetime>$date ?? .date_beginning,
    date_ending:= <optional cal::local_datetime>$ending_time ?? .date_ending,
    notes:=<optional json>$notes ?? .notes,
}
