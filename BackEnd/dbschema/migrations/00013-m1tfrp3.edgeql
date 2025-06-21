CREATE MIGRATION m1tfrp3l73aark3urxyqounnwj5ealfilc4hobdb3g422ls3ykwh7a
    ONTO m1vwypiuxhu7nodctjrcp74unr2y6ulffjvguq7pugjiinwowktm7q
{
  ALTER TYPE default::User {
      CREATE PROPERTY tag_type: std::str;
  };
  ALTER TYPE default::Account {
      ALTER PROPERTY tag_type {
          SET default := 'is_account';
          SET OWNED;
          SET TYPE std::str;
      };
  };
  ALTER TYPE default::Administator {
      ALTER PROPERTY tag_type {
          SET default := 'is_admin';
          SET OWNED;
          SET TYPE std::str;
      };
  };
  ALTER TYPE default::Individual {
      ALTER PROPERTY tag_type {
          SET default := 'is_individual';
          SET OWNED;
          SET TYPE std::str;
      };
  };
};
