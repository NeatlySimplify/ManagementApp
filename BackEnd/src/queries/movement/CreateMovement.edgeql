with recorded := <optional uuid>$record_id,
select (insert Movement {
    type_tag:= <str>$type_tag,
    notes:=<optional json>$notes,
    record := assert_single((select Record filter .id = recorded)) if exists recorded else {}
    }
){id}
