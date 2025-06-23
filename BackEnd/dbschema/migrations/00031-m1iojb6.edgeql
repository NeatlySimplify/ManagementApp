CREATE MIGRATION m1iojb6pgdrpgikehgwvcyhdao23rl4mgbvtxm23qog5slsnjmbjka
    ONTO m1lwgg72ievidb6kb5wqmquwt5iajozt7sj6i6jtsyvgs3aibpmjha
{
  ALTER TYPE default::Payment {
      ALTER TRIGGER insert_event USING (WITH
          new_event := 
              (INSERT
                  default::Scheduler
                  {
                      type_tag := __new__.type_tag,
                      name := __new__.name,
                      status := __new__.status,
                      date := __new__.is_due,
                      owner := __new__.owner
                  })
      UPDATE
          default::Payment
      FILTER
          (.id = __new__.id)
      SET {
          event := new_event
      });
  };
  ALTER TYPE default::Scheduler {
      DROP LINK payment_origin;
  };
};
