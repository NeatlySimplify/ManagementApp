CREATE MIGRATION m1otfifqvctr43v3lqjdy4sttp6ecvf5t4tevonasocckfichsx2ka
    ONTO m1zjpzrlxn3s54znhrvemyeg5giida6siiop2s3acrstqgytt73xta
{
  ALTER TYPE default::BankAccount {
      ALTER ACCESS POLICY user_access USING (true);
  };
  ALTER TYPE default::Scheduler {
      ALTER ACCESS POLICY user_access USING (true);
  };
};
