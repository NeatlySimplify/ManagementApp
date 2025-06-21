CREATE MIGRATION m1vwypiuxhu7nodctjrcp74unr2y6ulffjvguq7pugjiinwowktm7q
    ONTO m1taut442c7yrmalkmvo7tlnzbvnw6y5trmyktpjntavzdtgvs274a
{
  ALTER TYPE default::Account {
      ALTER ACCESS POLICY user_access ALLOW SELECT, UPDATE;
  };
  ALTER TYPE default::Administator {
      CREATE ACCESS POLICY admin_only
          ALLOW SELECT, UPDATE, DELETE USING ((__subject__ ?= GLOBAL default::current_user_obj));
  };
  ALTER TYPE default::Auditable {
      CREATE ACCESS POLICY admin_only
          ALLOW SELECT, UPDATE, DELETE USING (((GLOBAL default::current_user_obj).is_admin ?? false));
  };
};
