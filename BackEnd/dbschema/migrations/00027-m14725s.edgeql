CREATE MIGRATION m14725ssc75lme2tnfxgykoyyylxy46q3dkvtzi3wpor2ephc7kvfq
    ONTO m1qztj47ktz4e23evk2237dejccat2hjww6ratclcht5q5xclgybpa
{
  ALTER TYPE default::BankAccount {
      ALTER ACCESS POLICY user_access USING ((__subject__.owner ?= GLOBAL default::current_user_obj));
  };
};
