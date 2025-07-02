CREATE MIGRATION m1zuycqz2cfjdmxbeirxm3rabz3p5xlteb42iidug7t5ucoqv32fwq
    ONTO m1s4vkmx4qzlnpmka2keg5lguwx5lz5qbefqs6cdcq5aeido5m53gq
{
  ALTER TYPE default::Administator {
      ALTER ACCESS POLICY admin_only USING (SELECT
          ((GLOBAL default::current_user_obj).is_admin ?? false)
      );
  };
};
