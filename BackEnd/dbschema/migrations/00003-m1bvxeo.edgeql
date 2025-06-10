CREATE MIGRATION m1bvxeo53okdnprlkvb6oqgvvfqbf3y7tmfdf5j3caxab6e6jszu5a
    ONTO m1e2r4dhcbnnjm23sxfqhzwcb4mehbj7ezyrqurnlgyfyllu2hx5dq
{
  ALTER TYPE default::Payment {
      ALTER LINK event {
          RESET ON SOURCE DELETE;
      };
  };
};
