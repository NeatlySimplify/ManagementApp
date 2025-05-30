with delete_contact:= (
    delete Contact filter .id = <uuid>$contact
)
update Entity filter .id = <uuid>$entity_id set {
    phone -= delete_contact
}
