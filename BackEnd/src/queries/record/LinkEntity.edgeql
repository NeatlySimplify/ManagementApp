update Record filter .id = <uuid>$record_id set {
    entity+= (select Entity filter .id = <uuid>$entity_id)
}
