CREATE MIGRATION m163nnx6r5nob5tnmo7dj5ncakf27b3el4qpkkcwn5cvdkdxd6pzma
    ONTO m1ozop7me2abpig7zjttecderb3ubpdvifnznhkmtoucme7twr5fsa
{
  ALTER TYPE default::User {
      ALTER LINK account {
          USING (SELECT
              DETACHED default::BankAccount
          FILTER
              (.owner = __source__)
          );
      };
  };
};
