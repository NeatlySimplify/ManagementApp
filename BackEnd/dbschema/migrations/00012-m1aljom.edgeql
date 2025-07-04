CREATE MIGRATION m1aljomffl6sdnahdu7wfki6hqsuraodryg6apr5rxmhfbn7zurtuq
    ONTO m13kyg2w7at3x5s4zhgovdeubel3pu3qfyc4tufjpxtiivmp6vztnq
{
  ALTER TYPE default::Scheduler {
      ALTER PROPERTY date_beggining {
          RENAME TO date_beginning;
      };
      ALTER PROPERTY date_ending {
          SET default := ((__source__.date_beginning + <std::duration>'12 hours'));
      };
  };
  ALTER TYPE default::Payment {
      ALTER TRIGGER update_event USING (WITH
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
          date_beginning := <std::cal::local_datetime>new_date
      });
  };
};
