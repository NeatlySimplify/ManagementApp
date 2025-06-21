CREATE MIGRATION m17kiyx5wry4alow5xfdyucjzw5rnlvxi5insrgnixbbfdys5rlxcq
    ONTO m1wri6u6sxa2wvge7d7pepg6tspcymtykyx4lvjjiqmc6gciyfbbza
{
  ALTER TYPE default::User {
      CREATE MULTI LINK account := (SELECT
          DETACHED default::Movement
      FILTER
          (.owner = __source__)
      );
  };
  ALTER TYPE default::Scheduler {
      ALTER LINK onwer {
          RENAME TO owner;
      };
  };
  ALTER TYPE default::User {
      CREATE MULTI LINK event := (SELECT
          DETACHED default::Scheduler
      FILTER
          (.owner = __source__)
      );
  };
};
