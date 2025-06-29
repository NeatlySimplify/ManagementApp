CREATE MIGRATION m1g7xw4pv56kg2u7ax2g2x2nkve2gbdhjqxb4appmkhnannqjkrzxq
    ONTO m1elyqterhm5mzc4bchgrw6svzse64eb4s5hskapsndxijphafuuiq
{
  ALTER TYPE default::Account {
      DROP ACCESS POLICY admin_only;
  };
  ALTER TYPE default::Account {
      CREATE ACCESS POLICY allow_insert
          ALLOW INSERT USING (true);
  };
  ALTER TYPE default::Individual {
      DROP ACCESS POLICY admin_only;
  };
  ALTER TYPE default::Individual {
      CREATE ACCESS POLICY allow_insert
          ALLOW INSERT USING (true);
  };
};
