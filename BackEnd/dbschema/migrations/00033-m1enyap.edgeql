CREATE MIGRATION m1enyapmtnl5kzle6m4kk4lc7kdjziz7jq3r3grb55uyavsj3vdyaa
    ONTO m17ph6wxgp6eywz3afckvtmrzm4l5lxnhqwkwlz7qrqeah7hwrpkma
{
  ALTER TYPE default::Payment {
      DROP ACCESS POLICY user_access;
  };
};
