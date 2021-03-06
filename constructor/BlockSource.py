import os, sys
import yaml

class BlockSource(object):
    def __init__(self, path):
        blocks = []
        roots = []
        for entry in os.listdir(path):
            if os.path.isdir(os.path.join(path,entry)) and entry[0] != '.':
                roots.append(entry)
        for root in roots:
            processes = []
            for entry in os.listdir(os.path.join(path,root)):
                if os.path.splitext(entry)[1] == '.occ' and entry[0] != '.':
                    block_file = open(os.path.join(path,root,entry), 'r').read()
                    if block_file.find('--- Code') is -1:
                        metadata = block_file
                        code = None
                    else:
                        metadata, code = block_file.split('--- Code')
                    block = yaml.load(metadata)
                    block['code'] = code
                    processes.append(block)
            if processes:
                blocks.append((root, processes))
        self.blocks = blocks

    def get_roots (self):
        return [root for root, processes in self.blocks]

    def get_blocks (self, reqRoot):
        for root, processes in self.blocks:
            if root == reqRoot:
                return processes

if __name__ == '__main__':
    from pprint import pprint
    path = os.path.abspath(sys.argv[0])
    path = os.path.split(path)[0]
    bs = BlockSource(os.path.join(path, 'blocks'))
    pprint(bs.blocks)
