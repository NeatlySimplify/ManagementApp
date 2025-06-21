CREATE MIGRATION m15liljng5z3dfzigb27z2kunawgltsfocuuqdidxqmr7dmgua5jya
    ONTO m1ubh2kr63qmj42pfblwzussvp37tzgvbdmbwhhsnif7r3u4f54zxq
{
  ALTER TYPE default::User {
      CREATE PROPERTY is_admin: std::bool {
          SET default := (<std::bool>false);
      };
  };
  CREATE TYPE default::Administator EXTENDING default::User {
      ALTER PROPERTY is_admin {
          SET default := (<std::bool>true);
          SET OWNED;
          SET TYPE std::bool;
      };
  };
  ALTER TYPE default::Auditable {
      ALTER ACCESS POLICY user_access RENAME TO admin_only;
  };
  ALTER TYPE default::Auditable {
      ALTER ACCESS POLICY admin_only USING (((GLOBAL default::current_user_obj).is_admin ?? false));
  };
};
