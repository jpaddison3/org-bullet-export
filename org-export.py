'''
TODO; docstrings
'''
# TODO; maybe could be more OO rather than passing around output_fd
# TODO; or functional
from bs4 import BeautifulSoup
import click
import io
import pyperclip
import re

BULLET_PATTERN = r'^(\*+) (.*)'


def print_test():
    with open('example.html', 'r') as f:
        soup = BeautifulSoup(f.read())

    for tag in soup():
        for attribute in ['style', 'class']:
            del tag[attribute]

    print(str(soup).replace('\n', ''))


def read_bullet(line):
    '''

    :param line:
    :return: is_bullet, indent_level, non_bullet_text
    '''
    print('line', line.strip())
    match = re.match(BULLET_PATTERN, line)
    if not match:
        print('no match')
        return False, -1, line.strip()
    else:
        asterisks = match.group(1)
        print('asterisks', asterisks)
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
    # print('lines', lines)
    for line in lines:
        is_bullet, indent_level, text = read_bullet(line)
        if not is_bullet:
            indent_level = current_indent_level
        print('is_bullet', is_bullet)
        print('indent', indent_level)
        print('text', text)
        adjust_indent(current_indent_level, indent_level, output_fd)
        current_indent_level = indent_level
        if is_bullet:
            output_fd.write('  ' * current_indent_level + '<li>' + text + '</li>\n')
        else:
            output_fd.write('  ' * current_indent_level + '<p>' + text + '</p>\n')
        print('----\n')
    adjust_indent(current_indent_level, 0, output_fd)


@click.command()
@click.option('--input-file', '-i', default=None)
@click.option('--output', '-o', default='clipboard')
def run(input_file, output):
    # print('input', input_file)
    # print('input bool', bool(input_file))
    # print('input type', type(input_file))
    if not input_file:
        raise ValueError('Must specify input org file')
    if output != 'clipboard':
        raise NotImplementedError
    # print('input', input_file)
    # print('output', output)
    with open(input_file, 'r') as input_fd:
        output_fd = io.StringIO()
        org_export(input_fd, output_fd)
        output_str = output_fd.getvalue()
        print('output_str\n', output_str)
        pyperclip.copy(output_str)
        # print('pyperclip paste', pyperclip.paste())
        output_fd.close()
    # get fd_in, fd_out
    # org_export_file(fd_in, fd_out)
    pass


if __name__ == '__main__':
    run()
