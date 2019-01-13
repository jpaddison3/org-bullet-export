import click
import re

BULLET_PATTERN = r'^(\*+) (.*)'


def read_bullet(line):
    '''
    :param line:
    :return: is_bullet, indent_level, non_bullet_text
    '''
    match = re.match(BULLET_PATTERN, line)
    if not match:
        return False, -1, line.strip()
    else:
        asterisks = match.group(1)
        return True, len(asterisks), match.group(2)


def adjust_indent(current_indent_level, new_indent_level, output_fd):
    while current_indent_level < new_indent_level:
        output_fd.write('  ' * current_indent_level + '<ul>\n')
        current_indent_level += 1

    while current_indent_level > new_indent_level:
        output_fd.write('  ' * (current_indent_level - 1) + '</ul>\n')
        current_indent_level -= 1


def org_export(input_fd, output_fd):
    lines = input_fd.readlines()
    current_indent_level = 0
    for line in lines:
        is_bullet, indent_level, text = read_bullet(line)
        if not is_bullet:
            indent_level = current_indent_level
        adjust_indent(current_indent_level, indent_level, output_fd)
        current_indent_level = indent_level
        if is_bullet:
            output_fd.write('  ' * current_indent_level + '<li>' + text + '</li>\n')
        else:
            output_fd.write('  ' * current_indent_level + '<p>' + text + '</p>\n')
    adjust_indent(current_indent_level, 0, output_fd)


@click.command()
@click.option('--input-file', '-i')
@click.option('--output-file', '-o')
def run(input_file, output_file):
    if not input_file or not output_file:
        raise ValueError('Must specify input and output files')
    with open(input_file, 'r') as input_fd, open(output_file, 'w') as output_fd:
        org_export(input_fd, output_fd)


if __name__ == '__main__':
    run()
