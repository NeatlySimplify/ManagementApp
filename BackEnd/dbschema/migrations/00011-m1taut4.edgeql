CREATE MIGRATION m1taut442c7yrmalkmvo7tlnzbvnw6y5trmyktpjntavzdtgvs274a
    ONTO m14rkvedugw5fm7pto5nbitkhit3mh32o2gtt5yqv4ij24xj4ithoq
{
  ALTER TYPE default::Auditable {
      DROP ACCESS POLICY admin_only;
  };
};
