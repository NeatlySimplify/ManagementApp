with add_contact:= (
    insert Contact{
        name:= <str>$name,
        email:= <optional str>$email,
        number:= <json>$number,
        details:= <optional json>$details
    }
),
update_entity:= (
    update Entity filter .id = <uuid>$entity set {
        phone += add_contact
    }
)
select add_contact{id}
