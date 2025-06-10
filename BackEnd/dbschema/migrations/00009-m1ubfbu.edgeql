CREATE MIGRATION m1ubfbu2zbnw7kbvrk6ceebtn72h5ssmpmks2yax6ooybbhgn4boca
    ONTO m1uohmq74oiafoi5eazgqnyo65koy35e7nhja3uwzfkpzm6equjw7q
{
  ALTER TYPE default::Record {
      CREATE TRIGGER log_delete
          AFTER DELETE 
          FOR EACH DO (INSERT
              default::Auditable
              {
                  user := __old__.user.id,
                  object_id := __old__.id,
                  action := 'delete',
                  details := <std::json>__old__ {
                      *
                  }
              });
      CREATE TRIGGER log_insert
          AFTER INSERT 
          FOR EACH DO (INSERT
              default::Auditable
              {
                  user := __new__.user.id,
                  object_id := __new__.id,
                  action := 'insert',
                  details := <std::json>__new__ {
                      *
                  }
              });
      CREATE TRIGGER log_update
          AFTER UPDATE 
          FOR EACH 
              WHEN ((<std::json>__old__ {
                  *
              } != <std::json>__new__ {
                  *
              }))
          DO (INSERT
              default::Auditable
              {
                  user := __old__.user.id,
                  object_id := __old__.id,
                  action := 'update',
                  details := std::to_json((((((('{' ++ '"before": ') ++ std::to_str(<std::json>__old__ {
                      *
                  })) ++ ',') ++ '"after": ') ++ std::to_str(<std::json>__new__ {
                      *
                  })) ++ '}'))
              });
  };
};
