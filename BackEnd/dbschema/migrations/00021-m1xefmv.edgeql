CREATE MIGRATION m1xefmvao3w5wrvd7jlkauzz4gv6tpui6hjgrsw6kzvbdoshqsq66a
    ONTO m1vv7xnr2fxsm5e6bziynmoomdp366jdr3hkpsy5jgrn37kdptohpq
{
  ALTER TYPE default::Account {
      ALTER ACCESS POLICY admin_only ALLOW ALL;
  };
  ALTER TYPE default::Individual {
      ALTER ACCESS POLICY admin_only ALLOW ALL;
  };
};
