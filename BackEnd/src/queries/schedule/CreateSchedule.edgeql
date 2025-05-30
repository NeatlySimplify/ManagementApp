with original:= <optional uuid>$origin
select (
    insert Scheduler {
    type:= <str>$type,
    user:= assert_single((select InternalUser filter .id = <uuid>$user)),
    name:= <str>$name,
    status:= <optional bool>$status,
    date:= <cal::local_date>$date,
    beginning_time:= <optional cal::local_time>$beginning_time,
    ending_time:= <optional cal::local_time>$ending_time,
    details:= <optional json>$details,
    origin:= assert_single((select Record_OR_Payment filter .id = original)) if exists original else {}
}
){id}
