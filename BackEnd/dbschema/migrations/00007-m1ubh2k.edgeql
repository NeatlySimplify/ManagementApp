CREATE MIGRATION m1ubh2kr63qmj42pfblwzussvp37tzgvbdmbwhhsnif7r3u4f54zxq
    ONTO m1evcqd62mjmkidwiltabzl23eeucught7qkozfqajigcvvpmicrta
{
  CREATE GLOBAL default::current_user_obj := (SELECT
      default::User
  FILTER
      (.id = GLOBAL default::current_user)
  );
  ALTER TYPE default::User {
      DROP ACCESS POLICY user_access;
  };
  ALTER TYPE default::Account {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__ ?= GLOBAL default::current_user_obj));
  };
  ALTER TYPE default::Auditable {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__ ?= GLOBAL default::current_user_obj));
  };
  ALTER TYPE default::BankAccount {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
  ALTER TYPE default::Entity {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
  ALTER TYPE default::Individual {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__ ?= GLOBAL default::current_user_obj));
  };
  ALTER TYPE default::Movement {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
  ALTER TYPE default::Project {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
  ALTER TYPE default::Record {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
  ALTER TYPE default::Scheduler {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
};
