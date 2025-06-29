CREATE MIGRATION m1aazte4657gqylbgj3g5c6daaegblkj24mr4nsnatqkllpnkpddva
    ONTO m1g7xw4pv56kg2u7ax2g2x2nkve2gbdhjqxb4appmkhnannqjkrzxq
{
  ALTER TYPE default::Account {
      CREATE ACCESS POLICY admin_only
          ALLOW ALL USING (((GLOBAL default::current_user_obj).is_admin ?? false));
  };
  ALTER TYPE default::Account {
      DROP ACCESS POLICY allow_insert;
  };
  ALTER TYPE default::Individual {
      CREATE ACCESS POLICY admin_only
          ALLOW ALL USING (((GLOBAL default::current_user_obj).is_admin ?? false));
  };
  ALTER TYPE default::Individual {
      DROP ACCESS POLICY allow_insert;
  };
};
