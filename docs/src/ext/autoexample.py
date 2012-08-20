
import ast,os
from docutils import nodes, statemachine, utils
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.nodes import fully_normalize_name

def setup(app):
    app.add_directive('autoexample', AutoExampleDirective)

def parse_example(basepath, filename, img_folder):
    path = os.path.join(basepath, filename)
    with open(path) as f:
        content = f.read().strip()
    n = ast.parse(content)
    docstring = ast.get_docstring(n)
    if docstring == None:
        return []

    # Header
    s = [filename, "".ljust(len(filename), '-')]
    
    # Location 
    folder = os.path.basename(basepath)
    s.append("Location: *%s/%s*" % (folder, filename))
    
    # Docstring
    s.append("")
    s.append(docstring)
    s.append("")
    
    # Screenshot
    img_name,_ = os.path.splitext(filename)
    if img_folder != None:
        img_folder = os.path.join(img_folder, img_name + ".png")
        if os.path.isfile(img_folder):
            s.append("")
            s.append(".. image:: " + img_folder)
            s.append("")
            
    s.append("")
    return s
    
def parse_examples(path, img_folder):
    lines = []
    print("autoexample: documenting files in " + path)
    #print os.getcwd()
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file)
            if not os.path.isfile(path):
                continue
            _, ext = os.path.splitext(path)
            if ext != ".py":
                continue
            print("autoexample: documenting " + file)
            lines += parse_example(root, file, img_folder)

    return "\n".join(lines)
    
class AutoExampleDirective(Directive):
    # this enables content in the directive
    #has_content = True
    required_arguments = 1
    option_spec = {'image_folder': str}
    
    def run(self):
        source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
        source_dir = os.path.dirname(os.path.abspath(source))
        path = directives.path(self.arguments[0])
        path = os.path.normpath(os.path.join(source_dir, path))
        
        path = utils.relative_path(None, path)
        path = nodes.reprunicode(path)
        img_folder = None
        if "image_folder" in self.options:
            img_folder = os.path.normpath(os.path.join(source_dir, self.options["image_folder"]))
        
        rawtext = parse_examples(path, img_folder)

        include_lines = statemachine.string2lines(rawtext, self.state.document.settings.tab_width,
                                                  convert_whitespace=True)
        
        self.state_machine.insert_input(include_lines, path)
        return []