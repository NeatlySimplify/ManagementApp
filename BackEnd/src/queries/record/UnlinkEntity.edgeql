update Record filter .id = <uuid>$id_record set {
    entity-= (select Entity filter .id = <uuid>$entity_id)
}
