CREATE MIGRATION m13kyg2w7at3x5s4zhgovdeubel3pu3qfyc4tufjpxtiivmp6vztnq
    ONTO m1nwdy5o5j2yifoy3vuqftx2scp42b5tvinawsbnasm76bwpruwqla
{
  ALTER TYPE default::Scheduler {
      DROP PROPERTY beginning_time;
  };
  ALTER TYPE default::Scheduler {
      CREATE PROPERTY date_ending: std::cal::local_datetime {
          SET default := ((__source__.date_beggining + <std::duration>'12 hours'));
      };
  };
  ALTER TYPE default::Scheduler {
      DROP PROPERTY ending_time;
  };
};
