CREATE MIGRATION m1z6w5oqdcm3d2uyo3zerlz5euvk7t3f6zb73fc27zdmpmeeywvicq
    ONTO m14725ssc75lme2tnfxgykoyyylxy46q3dkvtzi3wpor2ephc7kvfq
{
  ALTER TYPE default::BankAccount {
      DROP ACCESS POLICY user_access;
  };
};
