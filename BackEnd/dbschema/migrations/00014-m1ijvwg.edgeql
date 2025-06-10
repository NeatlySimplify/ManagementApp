CREATE MIGRATION m1ijvwgi6wkmuvvnjvzrus456egkn7wimnvtace5hjus5msqhuumxq
    ONTO m1nbx3rckbcjulg2xv6mtx6lsxhm6dzysfphumxcvkvge57vnx7aoq
{
  ALTER TYPE default::Payment {
      ALTER TRIGGER create_event USING (INSERT
          default::Scheduler
          {
              user := __new__.user,
              name := __new__.name,
              type := __new__.type,
              status := __new__.status,
              date := __new__.is_due,
              origin := <default::Record_OR_Payment>__new__.id
          });
  };
  ALTER TYPE default::Payment {
      DROP TRIGGER update_event;
  };
  ALTER TYPE default::Payment {
      DROP LINK event;
  };
  ALTER TYPE default::Payment {
      CREATE LINK event := (SELECT
          default::Scheduler
      FILTER
          (.origin = __source__)
      );
  };
  ALTER TYPE default::Payment {
      CREATE TRIGGER update_event
          AFTER UPDATE 
          FOR EACH 
              WHEN (((__new__.status = true) OR (__old__.is_due != __new__.is_due)))
          DO (WITH
              new_status := 
                  __new__.status
              ,
              old_status := 
                  __old__.status
              ,
              new_isDue := 
                  __new__.is_due
              ,
              payment_date := 
                  __new__.payment_date
              ,
              new_date := 
                  (SELECT
                      (payment_date IF (new_status AND (new_status != old_status)) ELSE new_isDue)
                  )
          UPDATE
              __old__.event
          SET {
              name := __new__.name,
              status := __new__.status,
              date := new_date
          });
  };
};
