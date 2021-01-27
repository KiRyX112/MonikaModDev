
init python in mas_sprite_decoder:
    import store

    EYEBROW_MAP = {
        "f": "furrowed",
        "u": "up",
        "k": "knit",
        "s": "mid",
        "t": "think",
    }

    EYE_MAP = {
        "e": "normal",
        "w": "wide",
        "s": "sparkle",
        "t": "smug",
        "c": "crazy",
        "r": "right",
        "l": "left",
        "f": "soft",
        "h": "closedhappy",
        "d": "closedsad",
        "k": "winkleft",
        "n": "winkright",
    }

    MOUTH_MAP = {
        "a": "smile",
        "b": "big",
        "c": "smirk",
        "d": "small",
        "o": "gasp",
        "u": "smug",
        "w": "wide",
        "x": "angry",
        "p": "pout",
        "t": "triangle",
    }

    ARM_MAP = {
        "1": "steepling",
        "2": "crossed",
        "3": "restleftpointright",
        "4": "pointright",
        "5": ("def", "def"),
        "6": "down",
        "7": "downleftpointright",
    }


    HEAD_MAP = {
        
        "eua": "a",
        "eub": "b",
        "euc": "c",
        "eud": "d",
        "eka": "e",
        "ekc": "f",
        "ekd": "g",
        "esc": "h",
        "esd": "i",
        "hua": "j",
        "hub": "k",
        "hkb": "l", 
        "lka": "m", 
        "lkb": "n", 
        "lkc": "o", 
        "lkd": "p", 
        "dsc": "q",
        "dsd": "r",
    }

    SIDES_MAP = {
        "1": ("1l", "1r"),
        "2": ("1l", "2r"),
        "3": ("2l", "2r"),
        "4": ("2l", "2r"),
        "5": ("", ""),
        "6": ("1l", "1r"),
        "7": ("1l", "2r"),
    }


    SINGLE_MAP = {
        "a": "3a",
        "u": "3a",
    }

    BLUSH_MAP = {
        "bl": "lines",
        "bs": "shade",
        "bf": "full"
    }

    TEAR_MAP = {
        "ts": "streaming",
        "td": "dried",
        "tp": "pooled",
        "tu": "up",
    }

    SWEAT_MAP = {
        "sdl": "def",
        "sdr": "right"
    }

    def _m1_sprite0x2ddecoder__process_blush(spcode, index, export_dict, *prefixes):
        """
        Processes a blush off the given sprite code at the given index

        IN:
            spcode the spcode to check
            index the next index to check
            export_dict - dict to add the sprite data to
            prefixes letters to prefix the code with

        OUT:
            Tuple of the following format:
                [0] - True if the blush was valid, False if not
                [1] - the number of spots to increase the index by
        """
        
        fullcode = list(prefixes)
        fullcode.append(spcode[index])
        
        blush = BLUSH_MAP.get("".join(fullcode), None)
        
        if blush is None:
            return False, 0
        
        
        export_dict["blush"] = blush
        return True, 1

    def _m1_sprite0x2ddecoder__process_s(spcode, index, export_dict, *prefixes):
        """
        Processes the s-prefixed spcodes at the given index

        IN:
            spcode the spcode to check
            index the next index to check
            export_dict - dict to add the sprite data to
            prefixes letters to prefix the code with

        OUT:
            Tuple of the following format:
                [0] - True if the processes were valid, False if not
                [1] - the number of spots to increase the index by
        """
        midfix = spcode[index]
        index += 1
        sprite_added = False
        
        processor = SUB_PROCESS_MAP["s"].get(midfix, None)
        
        if processor is not None:
            fullcode = list(prefixes)
            fullcode.append(midfix)
            
            sprite_added, increaseby = processor(
                spcode,
                index,
                export_dict,
                *fullcode
            )
        
        
        if not sprite_added:
            return False, 0
        
        
        return True, 1 + increaseby

    def _m1_sprite0x2ddecoder__process_sweatdrop(spcode, index, export_dict, *prefixes):
        """
        Processes a sweatdrop off the given spcode at the given index

        IN:
            spcode the spcode to check
            index the next index to check
            export_dict - dict to add the sprite data to
            prefixes letters to prefix the code with

        OUT:
            Tuple of the following format:
                [0] - True if the sweatdrops were valid, False if not
                [1] - the number of spots to increase the index by
        """
        
        fullcode = list(prefixes)
        fullcode.append(spcode[index])
        
        sweatdrop = SWEAT_MAP.get("".join(fullcode), None)
        
        if sweatdrop is None:
            return False, 0
        
        
        export_dict["sweat"] = sweatdrop
        return True, 1

    def _m1_sprite0x2ddecoder__process_tears(spcode, index, export_dict, *prefixes):
        """
        Processes a tear off the given spcode at the given index

        IN:
            spcode the spcode to check
            index the next index to check
            export_dict - dict to add the sprite data to
            prefixes letters to prefix the code with

        OUT:
            Tuple of the following format:
                [0] - True if the tears were valid, False if not
                [1] - the number of spots to increase the index by
        """
        
        fullcode = list(prefixes)
        fullcode.append(spcode[index])
        
        tears = TEAR_MAP.get("".join(fullcode), None)
        
        if tears is None:
            return False, 0
        
        
        export_dict["tears"] = tears
        return True, 1

    PROCESS_MAP = {
        "b": _m1_sprite0x2ddecoder__process_blush,
        "s": _m1_sprite0x2ddecoder__process_s,
        "t": _m1_sprite0x2ddecoder__process_tears,
    }

    SUB_PROCESS_MAP = {
        "s": {
            "d": _m1_sprite0x2ddecoder__process_sweatdrop,
        },
    }

    def parse_exp_to_kwargs(exp):
        """
        Converts exp codes to kwargs to pass into mas_drawmonika_rk

        IN:
            exp - spritecode to convert

        OUT:
            dict representing the exp as kwargs for mas_drawmonika_rk

        ASSUMES:
            exp is not in the staticsprite format (not exp_static)

        RAISES:
            - KeyError if pose, eyes, eyebrows, or mouth is invalid
            - Exception if optional sprite is invalid
        """
        full_code = exp
        kwargs = dict()
        
        
        arms = ARM_MAP[exp[0]]
        
        
        if isinstance(arms, tuple):
            
            kwargs["lean"], arms = arms
            
            
            kwargs["single"] = SINGLE_MAP.get(exp[-1], "3b")
        
        else:
            
            kwargs["left"], kwargs["right"] = SIDES_MAP[exp[0]]
        
        
        kwargs["arms"] = arms
        
        
        kwargs["head"] = HEAD_MAP.get("".join((exp[1], exp[2], exp[-1])), "")
        
        
        kwargs["eyes"] = EYE_MAP[exp[1]]
        
        
        kwargs["eyebrows"] = EYEBROW_MAP[exp[2]]
        
        
        kwargs["mouth"] = MOUTH_MAP[exp[-1]]
        
        
        exp = exp[3:-1]
        
        
        kwargs["nose"] = "def"
        
        index = 0
        while index < len(exp):
            prefix = exp[index]
            index += 1
            sprite_added = False
            
            
            processor = PROCESS_MAP.get(prefix, None)
            if processor is not None:
                sprite_added, increaseby = processor(
                    exp,
                    index,
                    kwargs,
                    prefix
                )
            
            
            if not sprite_added:
                raise Exception("Invalid sprite used: {0}".format(full_code))
            
            
            index += increaseby
        
        return kwargs

    def isValidSpritecode(exp):
        """
        Spritecode validity tester

        IN:
            exp - exp to check validity

        OUT:
            boolean:
                - True if code is valid
                - False otherwise
        """
        
        exp = exp.replace("_static", "")
        
        
        try:
            parse_exp_to_kwargs(exp)
            
            
            return True
        
        
        except:
            return False
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
