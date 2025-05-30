with delete_address:= (
    delete Address filter .id = <uuid>$address
)
update Entity filter .id = <uuid>$entity_id set {
    address -= delete_address
}
