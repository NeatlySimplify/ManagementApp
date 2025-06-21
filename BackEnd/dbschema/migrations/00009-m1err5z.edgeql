CREATE MIGRATION m1err5zxcui2fsdi5x3mhhhkuw75cv6zxwrk4kikip3qzqurgnizzq
    ONTO m15liljng5z3dfzigb27z2kunawgltsfocuuqdidxqmr7dmgua5jya
{
  ALTER TYPE default::Account {
      CREATE ACCESS POLICY admin_only
          ALLOW DELETE, INSERT USING (((GLOBAL default::current_user_obj).is_admin ?? false));
      ALTER ACCESS POLICY user_access ALLOW SELECT, UPDATE, DELETE;
  };
  ALTER TYPE default::Individual {
      CREATE ACCESS POLICY admin_only
          ALLOW DELETE, INSERT USING (((GLOBAL default::current_user_obj).is_admin ?? false));
      ALTER ACCESS POLICY user_access ALLOW SELECT, UPDATE, DELETE;
  };
};
