with entity:=assert_single((select Entity filter .id = <uuid>$entity)),
add_contact:= (
    insert Contact{
        type_tag:= <str>$type_tag,
        extra_email:= <optional str>$extra_email,
        notes:=<optional json>$notes,
        number:= <str>$number,
    }
) if exists entity else <Contact>{},
update_entity:= (update entity set {
    phone += add_contact
}),
select {
    contact := add_contact { id },
    updated := update_entity { id }
}
