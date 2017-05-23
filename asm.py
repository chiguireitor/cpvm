import re
import ops

line_regex = re.compile("((\w*):){0,1}\W*(\w*)\W*([\w,\"=><\.\-\+]*)\W*(;.*){0,1}")
bops = ops.get_byte_ops()

def load_asm(fname):
    lines = []
    labels = {}

    with open(fname, 'r') as f:
        line_no = 0
        for line in f:
            line = line.strip().split(";")[0]
            if len(line) > 0:
                parsed = line_regex.match(line).groups()
                lop = None
                if parsed[1] != None:
                    labels[parsed[1]] = line_no

                if (parsed[2] != None) and (len(parsed[2]) > 0):
                    lop = bops[parsed[2]](parsed[3])
                lines.append(lop)
            else:
                lines.append(None)

            line_no += 1

    return {
        "lines": lines,
        "labels": labels
        }
