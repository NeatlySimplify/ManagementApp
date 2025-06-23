CREATE MIGRATION m1xaelupfehqootidycvhnnrjgsrscgekxinfnsdo2hhdxecwdkz4a
    ONTO m1z6w5oqdcm3d2uyo3zerlz5euvk7t3f6zb73fc27zdmpmeeywvicq
{
  ALTER TYPE default::Scheduler {
      DROP ACCESS POLICY user_access;
  };
};
