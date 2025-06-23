CREATE MIGRATION m1f52gg5wdyuqzpdqzervx3gpkbhpz37cgizxtwifm5z6fzqp7maxa
    ONTO m1xefmvao3w5wrvd7jlkauzz4gv6tpui6hjgrsw6kzvbdoshqsq66a
{
  ALTER TYPE default::Payment {
      CREATE LINK owner: default::User;
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
};
