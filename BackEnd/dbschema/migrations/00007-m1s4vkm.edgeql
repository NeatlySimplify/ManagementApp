CREATE MIGRATION m1s4vkmx4qzlnpmka2keg5lguwx5lz5qbefqs6cdcq5aeido5m53gq
    ONTO m1cf3iwyndjivuugqag36iyzhcbwzukcknlxdntfmlkgmrqeh3s7dq
{
  ALTER TYPE default::Administator {
      CREATE ACCESS POLICY bootstrap_admin
          ALLOW INSERT USING ((std::count(DETACHED default::User FILTER
              .is_admin
          ) = 0));
  };
};
