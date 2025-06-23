CREATE MIGRATION m17ny36z53m2k4pacpprsamjsdfd7j2wa5v3bvfw7wf4ifebmdtc6q
    ONTO m1enyapmtnl5kzle6m4kk4lc7kdjziz7jq3r3grb55uyavsj3vdyaa
{
  ALTER TYPE default::Payment {
      ALTER LINK event {
          DROP REWRITE
              INSERT ;
          };
      };
};
