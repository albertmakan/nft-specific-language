from textx import get_location, TextXSemanticError
            
from .model import Construct
from .model_utils import find_root


class SemanticError(TextXSemanticError):
    def __init__(self, message, construct: Construct):            
        super().__init__(message, **get_location(construct))
        
        self.construct = construct


def errorHandlerWrapper():
    def decorate(f):
        def aplicator(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except SemanticError as semanticError:
                handle_custom_error(semanticError)
            except Exception:
                if should_skip_error(args):
                    return
                raise
        return aplicator
    return decorate


def handle_custom_error(exception: SemanticError):
    root = find_root(exception.construct)
    if "errors" not in dir(root):
        root.errors = []
    root.errors.append(exception)
    return


def should_skip_error(function_args):
    for arg in function_args:
        if not isinstance(arg, Construct):
            continue

        if "skip_errors" in dir(arg._tx_metamodel) and arg._tx_metamodel.skip_errors:
            return True
    
    return False


def raise_error(message: str, construct: Construct):
    if "skip_errors" in dir(construct._tx_metamodel) and construct._tx_metamodel.skip_errors:
        raise SemanticError(message, construct)

    raise Exception(message)