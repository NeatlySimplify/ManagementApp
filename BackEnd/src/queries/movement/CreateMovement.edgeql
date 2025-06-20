with recorded := <optional uuid>$record_id,
select (insert Movement {
    user := assert_single((select InternalUser filter .id = <uuid>$user)),
    type:= <str>$type,
    notes:=<optional json>$notes,
    record := assert_single((select Record filter .id = recorded)) if exists recorded else {}
    }
){id}
