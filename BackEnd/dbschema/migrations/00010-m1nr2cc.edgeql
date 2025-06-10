CREATE MIGRATION m1nr2cc6ujtnp2oq2fwnh43jjeykf6g6kvqut7kghhhtg24kxf5cra
    ONTO m1ubfbu2zbnw7kbvrk6ceebtn72h5ssmpmks2yax6ooybbhgn4boca
{
  ALTER TYPE default::Entity {
      ALTER TRIGGER log_update USING (INSERT
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
  ALTER TYPE default::Movement {
      ALTER TRIGGER log_update USING (INSERT
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
