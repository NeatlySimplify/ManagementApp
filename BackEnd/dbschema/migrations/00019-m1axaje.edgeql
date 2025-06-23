CREATE MIGRATION m1axaje5evzw22zlmc67u3usxbymrbahu3hdfhzoqexjal5x6p5nfa
    ONTO m163nnx6r5nob5tnmo7dj5ncakf27b3el4qpkkcwn5cvdkdxd6pzma
{
  ALTER TYPE default::Auditable {
      CREATE ACCESS POLICY allow_all_inserts
          ALLOW INSERT USING (true);
  };
};
