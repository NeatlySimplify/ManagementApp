CREATE MIGRATION m1pmnziznpkbpqjpdcvyd4a2q75bb77fedvjacp2yjgbhgywsgmoha
    ONTO m16ujcwxp6h56imcklfkonar6bis2jmeifdbxu5bav5ul5qjfvj4ha
{
  ALTER TYPE default::Administator {
      CREATE ACCESS POLICY admin_only
          ALLOW SELECT, UPDATE, DELETE USING ((__subject__ ?= GLOBAL default::current_user_obj));
  };
};
