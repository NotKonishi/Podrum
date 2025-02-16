################################################################################
#                                                                              #
#  ____           _                                                            #
# |  _ \ ___   __| |_ __ _   _ _ __ ___                                        #
# | |_) / _ \ / _` | '__| | | | '_ ` _ \                                       #
# |  __/ (_) | (_| | |  | |_| | | | | | |                                      #
# |_|   \___/ \__,_|_|   \__,_|_| |_| |_|                                      #
#                                                                              #
# Copyright 2021 Podrum Studios                                                #
#                                                                              #
# Permission is hereby granted, free of charge, to any person                  #
# obtaining a copy of this software and associated documentation               #
# files (the "Software"), to deal in the Software without restriction,         #
# including without limitation the rights to use, copy, modify, merge,         #
# publish, distribute, sublicense, and/or sell copies of the Software,         #
# and to permit persons to whom the Software is furnished to do so,            #
# subject to the following conditions:                                         #
#                                                                              #
# The above copyright notice and this permission notice shall be included      #
# in all copies or substantial portions of the Software.                       #
#                                                                              #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS #
# IN THE SOFTWARE.                                                             #
#                                                                              #
################################################################################

from constant.mcbe_packet_ids import mcbe_packet_ids
from packet.mcbe.packet import packet

class start_game_packet(packet):
    def __init__(self, data: bytes = b"", pos: int = 0) -> None:
        super().__init__(data, pos)
        self.packet_id: int = mcbe_packet_ids.start_game_packet

    def decode_payload(self):
        pass
        
    def encode_payload(self):
        self.write_signed_var_long(self.entity_id)
        self.write_var_long(self.entity_runtime_id)
        self.write_signed_var_int(self.player_gamemode)
        self.write_vector_3(self.spawn)
        self.write_vector_2(self.rotation)
        self.write_signed_var_int(self.seed)
        self.write_short_le(self.spawn_biome_type)
        self.write_string(self.custom_biome_name)
        self.write_signed_var_int(self.dimension)
        self.write_signed_var_int(self.generator)
        self.write_signed_var_int(self.world_gamemode)
        self.write_signed_var_int(self.difficulty)
        self.write_block_coordinates(self.world_spawn)
        self.write_byte(self.disable_achivements)
        self.write_signed_var_int(self.time)
        self.write_signed_var_int(self.edu_offer)
        self.write_byte(self.edu_features)
        self.write_string(self.edu_product_id)
        self.write_float_le(self.rain_level)
        self.write_float_le(self.lightning_level)
        self.write_bool(self.confirmed_platform_locked)
        self.write_bool(self.multiplayer_game)
        self.write_bool(self.lan_broadcasting)
        self.write_signed_var_int(self.xbox_live_broadcast_mode)
        self.write_signed_var_int(self.platform_broadcast_mode)
        self.write_bool(self.enable_commands)
        self.write_bool(self.require_texture_pack)
        self.write_game_rules(self.game_rules)
        self.write_int_le(self.experiments)
        self.write_bool(self.has_used_experiments)
        self.write_bool(self.bonus_chest)
        self.write_bool(self.start_map)
        self.write_signed_var_int(self.permission_level)
        self.write_int_le(self.chunk_tick_range)
        self.write_bool(self.locked_behavior_pack)
        self.write_bool(self.locked_texture_pack)
        self.write_bool(self.from_locked_template)
        self.write_bool(self.only_msa_gamer_tags)
        self.write_bool(self.from_world_template)
        self.write_bool(self.world_template_option_locked)
        self.write_bool(self.only_old_villagers)
        self.write_string(self.game_version)
        self.write_int_le(self.limited_world_width)
        self.write_int_le(self.limited_world_height)
        self.write_bool(self.new_nether)
        self.write_bool(self.experimental_gamplay)
        self.write_string(self.level_id)
        self.write_string(self.world_name)
        self.write_string(self.premium_world_template_id)
        self.write_bool(self.trial)
        self.write_var_int(self.movement_type)
        self.write_signed_var_int(self.movement_rewind_size)
        self.write_bool(self.server_authoritative_block_breaking)
        self.write_long_le(self.current_tick)
        self.write_signed_var_int(self.enchantment_seed)
        self.write_var_int(0) # block states length
        self.write_var_int(len(self.item_table)) # item table length
        for string_id, numeric_id in self.item_table.items():
            self.write_string(string_id)
            self.write_short_le(numeric_id)
            self.write_bool(False)
        self.write_string(self.multiplayer_correlation_id)
        self.write_bool(self.server_authoritative_inventories)
