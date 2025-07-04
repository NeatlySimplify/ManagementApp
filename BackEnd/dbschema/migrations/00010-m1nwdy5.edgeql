CREATE MIGRATION m1nwdy5o5j2yifoy3vuqftx2scp42b5tvinawsbnasm76bwpruwqla
    ONTO m1uvkwjlvo3jdrorxzks4utftrvhnluqvlz3wa6eor7rx4upo3moaa
{
  ALTER TYPE default::Scheduler {
      CREATE PROPERTY date_beggining: std::cal::local_datetime;
      ALTER PROPERTY beginning_time {
          SET default := (<std::cal::local_time>'08:00:00');
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
          date_beggining := <std::cal::local_datetime>new_date
      });
  };
  ALTER TYPE default::Scheduler {
      DROP PROPERTY date;
      ALTER PROPERTY ending_time {
          SET default := (<std::cal::local_time>'18:00:00');
      };
  };
};
