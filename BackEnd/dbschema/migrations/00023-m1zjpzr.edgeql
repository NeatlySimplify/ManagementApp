CREATE MIGRATION m1zjpzrlxn3s54znhrvemyeg5giida6siiop2s3acrstqgytt73xta
    ONTO m1f52gg5wdyuqzpdqzervx3gpkbhpz37cgizxtwifm5z6fzqp7maxa
{
  ALTER TYPE default::Payment {
      ALTER ACCESS POLICY user_access USING (true);
  };
};
