import yaml
import json

from util import util


# existing TRExFitter config blocks
BLOCKS = ["Job", "Fit", "Region", "Sample",
          "NormFactor", "Systematic"]


class ConfigFile():
    def __init__(self, path):
        """some preprocessing of the config file"""
        with open(path) as f:
            lines = f.readlines()
        self.config = []
        for i in range(len(lines)):
            current_line = lines[i].rstrip()        # drop newlines
            # skip empty lines and comments
            if (len(current_line) > 0) and\
               (current_line.lstrip()[0] != "%"):
                self.config.append(current_line)

        # find where all blocks are
        self.block_positions = self._find_blocks()

    def __repr__(self):
        """for printing a class instance"""
        output = ""
        for line in self.config:
            output += line + "\n"
        return output

    def _identify_block_start(self, line):
        """check whether a new block starts on a given line"""
        start_pos = [line.find(b + ":") for b in BLOCKS]
        num_zeros = sum(p == 0 for p in start_pos)
        # zero means this kind of block starts here, can at most have one
        assert num_zeros <= 1
        if num_zeros == 1:
            block_type = BLOCKS[start_pos.index(0)]
            return block_type
        else:
            return None

    def _count_blocks(self, block_type):
        """count the amount of blocks of certain type"""
        is_in_line = [self._identify_block_start(l) == block_type
                      for l in self.config]
        return sum(is_in_line)

    def _split_setting_line(self, line):
        """split a setting of type 'Setting: Value' into setting and value"""
        parts = [part.replace("\"", "").strip() for part in line.split(":")]
        # translate value to int or float if applicable
        parts[1] = util.translate_value(parts[1])
        return parts[0], parts[1]

    def _find_blocks(self):
        """find where all blocks are"""
        block_positions = {}
        for block in BLOCKS:
            nBlocks_in_file = self._count_blocks(block)
            block_positions.update({block: [{} for _ in range(nBlocks_in_file)]})
            inside_block = False  # are we inside a block of type block
            number_of_blocks = 0  # how many blocks of this type exist
            for i, line in enumerate(self.config):
                block_start = self._identify_block_start(line)
                if (block_start is not None) and (inside_block):
                    # print(" ", block, "ends at line", i)
                    inside_block = False
                    block_positions[block][number_of_blocks].update({"end": i-1})
                    number_of_blocks += 1
                if (block_start == block) and (not inside_block):
                    inside_block = True
                    _, block_name = self._split_setting_line(line)
                    block_positions[block][number_of_blocks].update({"start": i})
                    block_positions[block][number_of_blocks].update({"name": block_name})
                    # print(" ", block, "starts at line", i)
            if inside_block:
                # should have reached the end of file, close last block
                block_positions[block][number_of_blocks].update({"end": i})

        return block_positions

    def _get_translated_blocks(self, block_type):
        """translate the TRExFitter block into a list of dictionaries"""
        nBlocks = len(self.block_positions[block_type])
        out_dict_list = [{} for _ in range(nBlocks)]
        for i, block in enumerate(self.block_positions[block_type]):
            out_dict_list[i].update({"Name": block["name"]})
            # get the rest of the info from the original config
            # +1 in lower index to skip block start, +1 to include last line
            for j in range(block["start"]+1, block["end"]+1):
                setting, value = self._split_setting_line(self.config[j])
                out_dict_list[i].update({setting: value})
        return out_dict_list

    def produce_dict(self, output_path, file_type="YAML"):
        full_dict = {}
        for block in BLOCKS:
            translated = self._get_translated_blocks(block)
            # for some block types, only a single instance is expected
            if block in ["Job", "Fit"]:
                assert len(translated) == 1
                translated = translated[0]
            full_dict.update({block: translated})
        self.full_dict = full_dict
        if file_type == "YAML":
            with open(output_path, "w") as f:
                yaml.dump(full_dict, f, default_flow_style=False)
        elif file_type == "JSON":
            with open(output_path, "w") as f:
                json.dump(full_dict, f, sort_keys=True, indent=4)
        else:
            raise NotImplementedError


def from_file(path, file_type="YAML"):
    """
    read and return a YAML/JSON config from a file via provided path
    """
    with open(path, "r") as f:
        if file_type == "YAML":
            config = yaml.safe_load(f)
        elif file_type == "JSON":
            config = json.load(f)
        else:
            raise NotImplementedError
    return config


if __name__ == "__main__":
    config_path = "input/minimal_example.config"
    output_path_yml = "out.yml"
    output_path_json = "out.json"

    # create a config object
    config = ConfigFile(config_path)

    # write the config to a file in YAML format
    config.produce_dict(output_path_yml, file_type="YAML")

    # write the config to a file in JSON format
    config.produce_dict(output_path_json, file_type="JSON")

    # check that they are consistent
    assert from_file(output_path_yml, file_type="YAML") == config.full_dict
    assert from_file(output_path_json, file_type="JSON") == config.full_dict
