CREATE MIGRATION m1vv7xnr2fxsm5e6bziynmoomdp366jdr3hkpsy5jgrn37kdptohpq
    ONTO m1axaje5evzw22zlmc67u3usxbymrbahu3hdfhzoqexjal5x6p5nfa
{
  ALTER TYPE default::Account {
      ALTER ACCESS POLICY admin_only ALLOW SELECT, DELETE, INSERT;
  };
  ALTER TYPE default::Administator {
      ALTER ACCESS POLICY admin_only ALLOW ALL;
  };
  ALTER TYPE default::Individual {
      ALTER ACCESS POLICY admin_only ALLOW SELECT, DELETE, INSERT;
  };
};
