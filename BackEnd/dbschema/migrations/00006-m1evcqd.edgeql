CREATE MIGRATION m1evcqd62mjmkidwiltabzl23eeucught7qkozfqajigcvvpmicrta
    ONTO m1i4efgm4v4ssp4n3qo4hhm73amjr7wrp4vrfocb2ourvkbrpxpw5q
{
  CREATE GLOBAL default::current_user -> std::uuid;
  ALTER TYPE default::User {
      CREATE ACCESS POLICY user_access
          ALLOW ALL USING ((__subject__.id ?= GLOBAL default::current_user));
  };
};
