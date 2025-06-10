with entity:=assert_single((select Entity filter .id = <uuid>$entity_id)),
add_address:= (
    insert Address{
        state:= <str>$state,
        city:= <str>$city,
        district:= <str>$district,
        street:= <str>$street,
        number:= <optional int64>$number,
        complement:= <optional str>$complement,
        postal:= <optional str>$postal
    }
) if exists entity else <Address>{},
update_entity := (
    update entity  set {
        address += add_address
    }
),
select {
    address := add_address { id },
    updated := update_entity { id }
}
