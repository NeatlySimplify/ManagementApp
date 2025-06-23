CREATE MIGRATION m155vedxdh4vfbgi3iznowul3cmmattaeaxdfvgatnrloucrhko3jq
    ONTO m1otfifqvctr43v3lqjdy4sttp6ecvf5t4tevonasocckfichsx2ka
{
  ALTER TYPE default::Scheduler {
      ALTER ACCESS POLICY user_access USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
};
