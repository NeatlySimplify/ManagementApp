CREATE MIGRATION m1qztj47ktz4e23evk2237dejccat2hjww6ratclcht5q5xclgybpa
    ONTO m155vedxdh4vfbgi3iznowul3cmmattaeaxdfvgatnrloucrhko3jq
{
  ALTER TYPE default::Payment {
      ALTER ACCESS POLICY user_access USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
};
