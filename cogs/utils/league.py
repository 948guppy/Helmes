import discord


class CreateLeague:
    @staticmethod
    def create_index(total: int):
        participates_index = []
        index = 1
        while index <= total:
            participates_index.append(index)
            index += 1
        return participates_index

    @staticmethod
    def total_matches(participates_index):
        teams = len(participates_index)
        match_count = teams * (teams - 1) / 2
        print(f"{int(match_count)}試合")
        return int(match_count)

    @staticmethod
    def nth_league_match(participates, nthMatch: int):
        def check_swap_list(indexMe, indexOpponent):
            if indexMe == indexOpponent:
                return True

        if len(participates) % 2 == 1:
            index_me = 0
            index_opponent = -1
            match_number = 1
            while True:
                if check_swap_list(participates[index_me], participates[index_opponent]):
                    index_me = 0
                    index_opponent = -1
                    for i in range(len(participates) - 1):
                        participates0 = participates[0]
                        participates.remove(participates0)
                        participates.append(participates0)

                else:
                    if match_number == nthMatch:
                        print(participates[index_me], participates[index_opponent])
                        return participates[index_me], participates[index_opponent]
                    else:
                        match_number += 1
                        index_me += 1
                        index_opponent += -1
        else:
            index_me = 0
            index_opponent = -1
            match_number = 1
            remainder = participates[-1]
            participates.remove(remainder)
            while True:
                # print(f"{participates[index_me]}, {participates[index_opponent]}")
                if check_swap_list(participates[index_me], participates[index_opponent]):
                    if match_number == nthMatch:
                        print(f"第{match_number}試合{participates[index_me]} vs {remainder}")
                        return participates[index_me], remainder
                    index_me = 0
                    index_opponent = -1
                    for i in range(len(participates) - 1):
                        participates0 = participates[0]
                        participates.remove(participates0)
                        participates.append(participates0)
                    match_number += 1

                else:
                    if match_number == nthMatch:
                        print(f"第{match_number}試合{participates[index_me]} vs {participates[index_opponent]}")
                        return participates[index_me], participates[index_opponent]
                    else:
                        match_number += 1
                        index_me += 1
                        index_opponent += -1

    @staticmethod
    def initial_setting(participates: int):
        index = league.create_index(participates)
        e = discord.Embed()
        e.add_field(name="参加人数", value=f"{participates}人")


league = CreateLeague()
league.initial_setting(6)
