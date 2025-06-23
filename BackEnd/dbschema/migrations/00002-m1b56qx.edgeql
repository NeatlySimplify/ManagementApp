CREATE MIGRATION m1b56qxlqsvvbyh2x2dlyulzrdb3iifm2quodpkahctphzcbfyb4oa
    ONTO m1ewy335uiavcvrm2z7swivimluhmanxwio75diher4ihz6j6nnb2q
{
  ALTER TYPE default::Administator {
      CREATE ACCESS POLICY admin_only
          ALLOW ALL USING ((__subject__ ?= GLOBAL default::current_user_obj));
  };
};
