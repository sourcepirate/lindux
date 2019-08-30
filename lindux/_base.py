"""

contains code for indexer implementation

"""
import os
import struct
import io

# This is for supporting address space for large files
# 2 ^ 64 address space which supports over a GB
NBYTEARCH = b"<Q"
NBYTE = 8


def _refine_index_filename(filename):
    """ get the current file name for CSV index
    """
    return f"{filename}.index"


def _get_index_filename(filepath):
    """ get index file """
    _file = os.path.basename(filepath)
    filename = _refine_index_filename(_file)
    return filename


def create_index(filepath):
    """ create new index if not exists """
    filename = _get_index_filename(filepath)
    if os.path.exists(filepath) and not os.path.isdir(filepath):
        _create_index(filepath, filename)


def _create_index(filepath, filename):
    buffer = io.BytesIO()
    reader = open(filepath, "rb")
    bytes_read = 0
    for line in reader.readlines():
        buffer.write(struct.pack(NBYTEARCH, bytes_read))
        bytes_read += len(line)
    index_file_path = os.path.join(os.path.dirname(filepath), filename)
    index_file = open(index_file_path, "wb")
    index_file.write(buffer.getvalue())
    index_file.close()
    return bytes_read


def read_line(filepath, n, num_lines=1):

    index_filename = _get_index_filename(filepath)
    try:
        index_file_path = os.path.join(
            os.path.dirname(filepath), index_filename
        )
        index_file = open(index_file_path, "rb")
        actual_file = open(filepath, "r")

        seek_pos = (n - 1) * NBYTE
        index_file.seek(seek_pos)

        # Read the start position of the line
        current_line_pos = struct.unpack(NBYTEARCH, index_file.read(NBYTE))

        seek_pos = (n - 1 + num_lines) * NBYTE
        index_file.seek(seek_pos)

        next_line_pos = struct.unpack(NBYTEARCH, index_file.read(NBYTE))

        actual_file.seek(current_line_pos[0])

        data = actual_file.read(next_line_pos[0] - current_line_pos[0])

        return data
    except FileNotFoundError:
        raise Error("No index found")


if __name__ == "__main__":

    print(read_line("pmsm_temperature_data.csv", 900000, num_lines=2))
