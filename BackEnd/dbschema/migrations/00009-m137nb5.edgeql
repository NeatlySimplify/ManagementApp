CREATE MIGRATION m137nb55j7nd7l2rmhquu6j6f7hmk7oju4kgetoxf4awiucwswlxta
    ONTO m1scp772tpy5ac44yihjbeiyh3x2n2mtcv2ojrxswe656ytz3ak4oq
{
  ALTER TYPE default::InternalUser {
      ALTER LINK settings {
          ON SOURCE DELETE DELETE TARGET;
      };
  };
  ALTER TYPE default::Payment {
      DROP TRIGGER update_any;
      DROP TRIGGER update_balance_on_delete;
  };
};
