CREATE MIGRATION m1lwgg72ievidb6kb5wqmquwt5iajozt7sj6i6jtsyvgs3aibpmjha
    ONTO m1xaelupfehqootidycvhnnrjgsrscgekxinfnsdo2hhdxecwdkz4a
{
  ALTER TYPE default::Payment {
      ALTER LINK event {
          CREATE REWRITE
              INSERT 
              USING (__subject__.event);
      };
  };
  ALTER TYPE default::Scheduler {
      CREATE LINK payment_origin: default::Payment;
  };
  ALTER TYPE default::Payment {
      CREATE TRIGGER insert_event
          AFTER INSERT 
          FOR EACH DO (WITH
              status_ := 
                  __new__.status
              ,
              isDue := 
                  __new__.is_due
              ,
              type_ := 
                  __new__.type_tag
              ,
              name_ := 
                  __new__.name
              ,
              owner_ := 
                  __new__.owner
              ,
              origin := 
                  __new__
          INSERT
              default::Scheduler
              {
                  type_tag := type_,
                  name := name_,
                  status := status_,
                  date := isDue,
                  owner := owner_,
                  payment_origin := origin
              });
  };
};
