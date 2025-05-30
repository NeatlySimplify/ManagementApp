with add_address:= (
    insert Address{
        state:= <str>$state,
        city:= <str>$city,
        district:= <str>$district,
        street:= <str>$street,
        number:= <optional int64>$number,
        complement:= <optional str>$complement,
        postal:= <optional str>$postal
    }
),
update_entity := (
    update Entity filter .id = <uuid>$entity_id set {
        address += add_address
    }
)
select add_address{id}
