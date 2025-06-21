CREATE MIGRATION m14rkvedugw5fm7pto5nbitkhit3mh32o2gtt5yqv4ij24xj4ithoq
    ONTO m1err5zxcui2fsdi5x3mhhhkuw75cv6zxwrk4kikip3qzqurgnizzq
{
  ALTER TYPE default::Auditable {
      ALTER ACCESS POLICY admin_only ALLOW SELECT, UPDATE, DELETE;
  };
};
