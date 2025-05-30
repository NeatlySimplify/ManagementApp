CREATE MIGRATION m1fihnrqkufai2744uxkgpgpwiognnr4iqnhafzytzwxj4enrsffda
    ONTO m1emt4t7zkt46np2dohzfat3suulmvilcviqggcyzdszzeca4k6deq
{
  ALTER TYPE default::Movement {
      CREATE PROPERTY charges: std::float64 {
          SET default := 0;
      };
  };
  ALTER TYPE default::Payment {
      DROP PROPERTY charges;
  };
};
