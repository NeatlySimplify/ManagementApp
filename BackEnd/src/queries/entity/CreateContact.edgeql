with entity:=assert_single((select Entity filter .id = <uuid>$entity)),
add_contact:= (
    insert Contact{
        name:= <str>$name,
        email:= <optional str>$email,
        notes:=<optional json>$notes,
        number:= <json>$number,
    }
) if exists entity else <Contact>{},
update_entity:= (update entity set {
    phone += add_contact
}),
select {
    contact := add_contact { id },
    updated := update_entity { id }
}
