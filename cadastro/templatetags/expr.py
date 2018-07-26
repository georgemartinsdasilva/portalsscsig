from django import template
from django.utils.translation import gettext_lazy as _
import re

register = template.Library()

class ExprNode(template.Node):
    def __init__(self, expr_string, var_name):
        self.expr_string = expr_string
        self.var_name = var_name
        
    
    def render(self, context):
        try:
            clist = list(context)
            clist.reverse()
            d = {}
            d['_'] = _
            for c in clist:
                for item in c:
                    if isinstance(item, dict): 
                        d.update(item)
            if self.var_name:
                context[self.var_name] = eval(self.expr_string, d)
                return ''
            else:
                return str(eval(self.expr_string, d))
        except:
            raise

r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)    
def do_expr(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        print("ERROR")
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
             print("ERROR2")
            
        expr_string, var_name = arg, None
    return ExprNode(expr_string, var_name)
do_expr = register.tag('expr', do_expr)