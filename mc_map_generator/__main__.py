from .app import Mapper
import sys


if __name__ == "__main__":
    if sys.argv[1] == 'std_map':
        Mapper.standard_map()

    elif sys.argv[1] == 'heatmap':
        Mapper.heatmap()
