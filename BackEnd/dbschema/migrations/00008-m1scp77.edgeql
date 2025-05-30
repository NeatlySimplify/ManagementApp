CREATE MIGRATION m1scp772tpy5ac44yihjbeiyh3x2n2mtcv2ojrxswe656ytz3ak4oq
    ONTO m1tan7ugi3ff4nb6dnuvdjsjdm5gmtjn5hx2lksam4zpnflgy3dv2q
{
  ALTER TYPE default::InternalUser {
      DROP LINK payment;
  };
};
