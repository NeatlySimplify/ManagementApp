with recorded := <optional uuid>$record_id,
user:= (select global current_user_obj)
select (insert Movement {
    owner := user,
    type_tag:= <str>$type_tag,
    notes:=<optional json>$notes,
    record := assert_single((select Record filter .id = recorded)) if exists recorded else {}
    }
){id}
