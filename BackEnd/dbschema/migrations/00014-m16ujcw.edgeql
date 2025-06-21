CREATE MIGRATION m16ujcwxp6h56imcklfkonar6bis2jmeifdbxu5bav5ul5qjfvj4ha
    ONTO m1tfrp3l73aark3urxyqounnwj5ealfilc4hobdb3g422ls3ykwh7a
{
  ALTER TYPE default::Administator {
      DROP ACCESS POLICY admin_only;
  };
};
