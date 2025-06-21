CREATE MIGRATION m1ozop7me2abpig7zjttecderb3ubpdvifnznhkmtoucme7twr5fsa
    ONTO m1vyhzmixxegrlvtghpln6v56pshsqzh5dxkuhelg2tq7bfdb3irtq
{
  ALTER TYPE default::Record {
      ALTER PROPERTY optitional_status {
          RENAME TO optional_status;
      };
  };
};
