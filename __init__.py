from binaryninja import *

def list_symbols(bv,function):
    fmt_xrefs = "- `{}`, **xrefs:** {}"
    fmt_xref_el = "[{}+{:X}](binaryninja://?expr=0x{:x})"
    md_text = "# Symbols\n\n"

    def parse_symbol(refs, symbol):
        xrefs = bv.get_code_refs(symbol.address)
        if len(xrefs) == 0:
            return ""
        for r in xrefs:
            refs.append(fmt_xref_el.format(
                r.function.name, 
                r.address - r.function.start,
                r.address))
        return fmt_xrefs.format(symbol.full_name, ", ".join(refs))
    
    md = []
    for name in bv.symbols:    
        symbol = bv.symbols[name]
        refs = []
        if isinstance(symbol, list):
            for s in symbol:
                p = parse_symbol(refs, s)
                if p not in md:
                    md.append(p)
        else:
            md.append(parse_symbol(refs, symbol))
    
    md.sort()
    md_text += "\n".join(md)
    bv.show_markdown_report("Symbols Listing", md_text)


PluginCommand.register_for_address("List External Symbols", "List detected symbols", list_symbols)
