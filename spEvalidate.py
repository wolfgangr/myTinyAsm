# sanity checking of user provided code
# see https://github.com/yaroslaff/evalidate/
# assume it lives beneath ourselves in Macro/dev
# .../FreeCAD/Macro/dev$ git clone https://github.com/yaroslaff/evalidate.git

import dev.evalidate.evalidate as evalidate

# anything is forbidden if not explicitly allowed:
# start by generic math formulae and test what is missing
# sPyMod_model = evalidate.mult_eval_model.clone()
sPyMod_model = evalidate.base_eval_model.clone()
sPyMod_model.nodes.extend(['Mult', 'Call', 'Attribute'] )
