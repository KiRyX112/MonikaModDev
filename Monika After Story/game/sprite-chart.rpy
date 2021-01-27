




































































































define is_sitting = True


default persistent._mas_acs_pre_list = []
default persistent._mas_acs_bbh_list = []
default persistent._mas_acs_bse_list = []
default persistent._mas_acs_bba_list = []
default persistent._mas_acs_ase_list = []
default persistent._mas_acs_bat_list = []
default persistent._mas_acs_mat_list = []
default persistent._mas_acs_mab_list = []
default persistent._mas_acs_bfh_list = []
default persistent._mas_acs_afh_list = []
default persistent._mas_acs_mid_list = []
default persistent._mas_acs_pst_list = []


default persistent._mas_zoom_zoom_level = None

default persistent._mas_force_clothes = False


default persistent._mas_force_hair = False


# image monika g1:
#     "monika/g1.png"
#     xoffset 35 yoffset 55
#     parallel:
#         zoom 1.00
#         linear 0.10 zoom 1.03
#         repeat
#     parallel:
#         xoffset 35
#         0.20
#         xoffset 0
#         0.05
#         xoffset -10
#         0.05
#         xoffset 0
#         0.05
#         xoffset -80
#         0.05
#         repeat
#     time 1.25
#     xoffset 0 yoffset 0 zoom 1.00
#     "monika 3"

# image monika g2:
#     block:
#         choice:
#             "monika/g2.png"
#         choice:
#             "monika/g3.png"
#         choice:
#             "monika/g4.png"
#     block:
#         choice:
#             pause 0.05
#         choice:
#             pause 0.1
#         choice:
#             pause 0.15
#         choice:
#             pause 0.2
#     repeat

define m = DynamicCharacter('monika_name', image='monika', what_prefix='', what_suffix='', ctc="ctc", ctc_position="fixed")


image mas_bday_banners = ConditionSwitch(
    "morning_flag",
    "mod_assets/location/spaceroom/bday/birthday_decorations_rus.png",
    "not morning_flag",
    "mod_assets/location/spaceroom/bday/birthday_decorations-n_rus.png"
)


image mas_finalnote_idle = "mod_assets/poem_finalfarewell_desk.png"


image mas_piano = MASFilterSwitch("mod_assets/other/mas_piano.png")






init -101 python in mas_sprites:

    class ACSTemplate(renpy.store.object):
        """
        ACS template object
        Establishes guidelines for defauling properties for an ACS

        PROPERTIES:
            acs_type - the acs type associated with this template
            mux_type - the default mux type list for this template
            ex_props - default exprops dict for this template
            keep_on_desk - default keep on desk flag for this templat
        """
        
        def __init__(self,
                acs_type,
                mux_type=None,
                ex_props=None,
                keep_on_desk=None
        ):
            """
            Constructor

            IN:
                acs_type - acs type this template should be associated with
                mux_type - the mux_type we want to use as default. Ignored if
                    None.
                    (Default: None)
                ex_props - the ex_props we want to use as default. Ignored if
                    None.
                    (Default: None)
                keep_on_desk - the keep_on_desk flag we want to use as default.
                    Ignored if None.
                    (Default: None)
            """
            self.acs_type = acs_type
            self.mux_type = mux_type
            self.ex_props = ex_props
            self.keep_on_desk = keep_on_desk
        
        def _apply_ex_props(self, acs):
            """
            Applies ex prop defaults to the given ACS.

            acs_type is NOT checked.

            IN:
                acs - acs to modify
            """
            if self.ex_props is None:
                return
            
            if acs.ex_props is None:
                acs.ex_props = dict(self.ex_props)
            
            else:
                acs.ex_props.update(self.ex_props)
        
        def _apply_keep_on_desk(self, acs):
            """
            Applies keep_on_desk defaults to the given ACS.

            acs_type is NOT checked.

            IN:
                acs- acs to modify
            """
            if self.keep_on_desk is None:
                return
            
            acs.keep_on_desk = self.keep_on_desk
        
        def _apply_mux_type(self, acs):
            """
            Applies mux type defaults to the given ACS. 
            
            acs_type is NOT checked.

            IN:
                acs - acs to modify.
            """
            if self.mux_type is None:
                return
            
            if acs.mux_type is None:
                acs.mux_type = list(self.mux_type)
            
            else:
                for mux_type in self.mux_type:
                    if mux_type not in acs.mux_type:
                        acs.mux_type.append(mux_type)
        
        def apply(self, acs):
            """
            Applies the defaults to the given ACS. (NOTE: acs type is checked)
            """
            if self.acs_type == acs.acs_type:
                self._apply_ex_props(acs)
                self._apply_keep_on_desk(acs)
                self._apply_mux_type(acs)


init -100 python in mas_sprites:





    EXP_A_EXCLHP = "excluded-hair-props"




    EXP_A_LHSEL = "left-hair-strand-eye-level"



    EXP_A_RQHP = "required-hair-prop"



    EXP_A_LD = "left-desk-acs"



    EXP_A_RBL = "ribbon-like"



    EXP_A_TWRB = "twin-ribbon"



    EXP_A_FOOD = "food"



    EXP_A_DRINK = "drink"





    EXP_H_TT = "twintails"



    EXP_H_RQCP = "required-clothes-prop"



    EXP_H_EXCLCP = "excluded-clothes-props"




    EXP_H_TS = "tiedstrand"



    EXP_H_NT = "no-tails"


    EXP_H_TB = "twinbraid"



    EXP_C_BRS = "bare-right-shoulder"



    EXP_C_COST = "costume"



    EXP_C_COSP = "cosplay"



    EXP_C_LING = "lingerie"





    DEF_EXP_TT_EXCL = [EXP_H_TT]




    DEF_MUX_RB = [
        "ribbon",
        "bow",
        "bunny-scrunchie",
        "hat",
        "s-type-ribbon",
        "twin-ribbons",
    ]


    DEF_MUX_HS = [
        "headset",
        "earphones",
        "hat",
        "headband",
        "headphones",
        "left-hair-flower-ear",
    ]


    DEF_MUX_HB = [
        "headband",
        "hat",
        "headphones",
        "headset",
    ]


    DEF_MUX_LHC = ["left-hair-clip"]


    DEF_MUX_LHFE = [
        "left-hair-flower-ear",
        "earphones",
        "front-hair-flower-crown",
        "hat",
        "headset",
        "headphones",
        "left-hair-flower",
    ]


    DEF_MUX_LD = [
        "plush_q",
        "chocs",
        "plate"
    ]


    DEF_MUX_HAT = [
        "hat",
        "bow",
        "bunny-scrunchie",
        "earphones",
        "front-hair-flower-crown",
        "headband",
        "headphones",
        "headset",
        "left-hair-flower",
        "ribbon",
        "s-type-ribbon",
        "twin-ribbons",
    ]



    ACS_DEFS = {
        "bow": ACSTemplate(
            "bow",
            mux_type=DEF_MUX_RB,
            ex_props={
                EXP_A_RBL: True,
                EXP_A_EXCLHP: DEF_EXP_TT_EXCL,
            }
        ),
        "bunny-scrunchie": ACSTemplate(
            "bunny-scrunchie",
            mux_type=DEF_MUX_RB,
            ex_props={
                EXP_A_RBL: True,
                EXP_A_EXCLHP: DEF_EXP_TT_EXCL,
            }
        ),
        "choker": ACSTemplate(
            "choker",
            mux_type=["choker"],
            ex_props={
                "bare neck": True
            }
        ),
        "front-hair-flower-crown": ACSTemplate(
            "front-hair-flower-crown",
            mux_type=DEF_MUX_LHFE,
            ex_props={
                "front-hair-crown": True,
            },
        ),
        "hat": ACSTemplate(
            "hat",
            mux_type=DEF_MUX_HAT
        ),
        "headband": ACSTemplate(
            "headband",
            mux_type=DEF_MUX_HB
        ),
        "headset": ACSTemplate(
            "headset",
            mux_type=DEF_MUX_HS
        ),
        "left-hair-clip": ACSTemplate(
            "left-hair-clip",
            mux_type=DEF_MUX_LHC,
            ex_props={
                EXP_A_LHSEL: True
            }
        ),
        "left-hair-flower": ACSTemplate(
            "left-hair-flower",
            mux_type=[
                "left-hair-flower",
                "left-hair-flower-ear",
                "front-hair-flower-crown"
            ],
            ex_props={
                EXP_A_LHSEL: True
            }
        ),
        "left-hair-flower-ear": ACSTemplate(
            "left-hair-flower-ear",
            mux_type=DEF_MUX_LHFE,
            ex_props={
                EXP_A_LHSEL: True
            }
        ),
        "mug": ACSTemplate(
            "mug",
            mux_type=["mug", "thermos-mug"],
            keep_on_desk=True,
            ex_props={
                EXP_A_DRINK: True
            }
        ),
        "necklace": ACSTemplate(
            "necklace",
            mux_type=["necklace"],
            ex_props={
                "bare collar": True,
            }
        ),
        "plate": ACSTemplate(
            "plate",
            mux_type=DEF_MUX_LD,
            keep_on_desk=True,
            ex_props={
                EXP_A_LD: True,
                EXP_A_FOOD: True
            }
        ),
        
        "ribbon": ACSTemplate(
            "ribbon",
            mux_type=DEF_MUX_RB
        ),
        "s-type-ribbon": ACSTemplate(
            "s-type-ribbon",
            mux_type=DEF_MUX_RB,
            ex_props={
                EXP_A_RBL: True,
            }
        ),
        "thermos-mug": ACSTemplate(
            "thermos-mug",
            mux_type=["mug", "thermos-mug"],
            keep_on_desk=False
        ),
        "twin-ribbons": ACSTemplate(
            "twin-ribbons",
            mux_type=DEF_MUX_RB,
            ex_props={
                EXP_A_TWRB: True,
                EXP_A_RBL: True,
                EXP_A_RQHP: EXP_H_TT,
            }
        ),
        "wrist-bracelet": ACSTemplate(
            "wrist-bracelet",
            mux_type=["wrist-bracelet"],
            ex_props={
                "bare wrist": True,
            }
        ),
    }


    def apply_ACSTemplate(acs):
        """
        Applies ACS template to the given ACS

        IN:
            acs - acs to apply defaults to
        """
        template = get_ACSTemplate(acs)
        if template is not None:
            template.apply(acs)


    def apply_ACSTemplates():
        """RUNTIME ONLY
        Applies all templates to the available ACS.
        """
        for acs_name in ACS_MAP:
            apply_ACSTemplate(ACS_MAP[acs_name])


    def get_ACSTemplate(acs):
        """
        Gets the template for an ACS given the ACS.

        IN:
            acs - acs to get template for

        RETURNS: ACSTemplate associated with the acs, or None if not found
        """
        if acs is None:
            return None
        return get_ACSTemplate_by_type(acs.acs_type)


    def get_ACSTemplate_by_type(acs_type):
        """
        Gets the template for an ACS given the ACS type

        IN:
            acs_type - acs type to get template for

        RETURNS: ACSTemplate associated with the acs_type or Nonr if not ound
        """
        return ACS_DEFS.get(acs_type, None)


init -5 python in mas_sprites:

    import store


    MOD_ART_PATH = "mod_assets/monika/"
    STOCK_ART_PATH = "monika/"


    ART_DLM = "-"


    KW_STOCK_ART = "def"









    H_MAIN = MOD_ART_PATH + "h/"
    C_MAIN = MOD_ART_PATH + "c/"
    B_MAIN = MOD_ART_PATH + "b/"
    F_MAIN = MOD_ART_PATH + "f/"
    A_MAIN = MOD_ART_PATH + "a/"
    S_MAIN = MOD_ART_PATH + "s/"
    T_MAIN = MOD_ART_PATH + "t/"





    F_T_MAIN = F_MAIN



    A_T_MAIN = A_MAIN




    LOC_REG = "(1280, 850)"
    LOC_LEAN = "(1280, 850)"
    LOC_Z = "(0, 0)"
    LOC_STAND = "(960, 960)"

    LOC_W = 1280
    LOC_H = 850
    LOC_WH = (1280, 850)


    I_COMP = "LiveComposite"
    L_COMP = "LiveComposite"
    TRAN = "Transform"


    ZOOM = "zoom="

    default_zoom_level = 3

    if store.persistent._mas_zoom_zoom_level is None:
        store.persistent._mas_zoom_zoom_level = default_zoom_level
        zoom_level = default_zoom_level

    else:
        zoom_level = store.persistent._mas_zoom_zoom_level

    zoom_step = 0.05
    default_value_zoom = 1.25
    value_zoom = default_value_zoom
    max_zoom = 20


    default_x = 0
    default_y = 0
    adjust_x = default_x
    adjust_y = default_y

    y_step = 20


    PRE_SPRITE_STR = TRAN + "(" + L_COMP + "("


    PREFIX_TORSO = "torso" + ART_DLM
    PREFIX_TORSO_LEAN = "torso-leaning" + ART_DLM
    PREFIX_BODY = "body" + ART_DLM
    PREFIX_BODY_LEAN = "body-leaning" + ART_DLM
    PREFIX_HAIR = "hair" + ART_DLM
    PREFIX_HAIR_LEAN = "hair-leaning" + ART_DLM
    PREFIX_ARMS = "arms" + ART_DLM
    PREFIX_ARMS_LEAN = "arms-leaning" + ART_DLM
    PREFIX_ARMS_LEFT = "left" + ART_DLM
    PREFIX_ARMS_RIGHT = "right" + ART_DLM
    PREFIX_FACE = "face" + ART_DLM
    PREFIX_FACE_LEAN = "face-leaning" + ART_DLM
    PREFIX_ACS = "acs" + ART_DLM
    PREFIX_ACS_LEAN = "acs-leaning" + ART_DLM
    PREFIX_EYEB = "eyebrows" + ART_DLM
    PREFIX_EYES = "eyes" + ART_DLM
    PREFIX_NOSE = "nose" + ART_DLM
    PREFIX_MOUTH = "mouth" + ART_DLM
    PREFIX_SWEAT = "sweatdrop" + ART_DLM
    PREFIX_EMOTE = "emote" + ART_DLM
    PREFIX_TEARS = "tears" + ART_DLM
    PREFIX_EYEG = "eyebags" + ART_DLM
    PREFIX_BLUSH = "blush" + ART_DLM
    PREFIX_TABLE = "table" + ART_DLM
    PREFIX_CHAIR = "chair" + ART_DLM


    FHAIR = "front"
    BHAIR = "back"


    NIGHT_SUFFIX = ART_DLM + "n"
    SHADOW_SUFFIX = ART_DLM + "s"
    FHAIR_SUFFIX  = ART_DLM + FHAIR
    BHAIR_SUFFIX = ART_DLM + BHAIR
    HLITE_SUFFIX = ART_DLM + "h"
    FILE_EXT = ".png"


    DEF_BODY = "def"
    NEW_BODY_STR = PREFIX_BODY + DEF_BODY


    BASE_BODY_STR = PREFIX_BODY + DEF_BODY + ART_DLM
    BASE_BODY_STR_LEAN = PREFIX_BODY_LEAN + DEF_BODY + ART_DLM


    TC_GEN = "".join((
        T_MAIN,
        "{0}", 
        "{1}", 
        "{2}", 
        "{3}", 
        FILE_EXT
    ))


    def alt_bcode(v_list, prefix, inc_night):
        """
        Adds bcode 0 and bcode 1 versions of the given prefix to the given
        list.

        IN:
            prefix - string to add bcode to
            inc_night - if True, then we also do night variants of each bcode
                version, otherwise, just day versions

        OUT:
            v_list - list to add strings to
        """
        if inc_night:
            alt_night(v_list, prefix + ART_DLM + "0")
            alt_night(v_list, prefix + ART_DLM + "1")
        
        else:
            v_list.append(prefix + ART_DLM + "0" + FILE_EXT)
            v_list.append(prefix + ART_DLM + "1" + FILE_EXT)


    def alt_hsplit(v_list, prefix, inc_night):
        """
        Adds backhair/front hair versionsof the given prefix to the given list

        IN:
            prefix - string to add bhair/front hair to
            inc_night - if Ture, then we also do night varaints of each bhair
                fhair version, otherwise just day versions

        OUT:
            v_list - list to add strings to
        """
        if inc_night:
            alt_night(v_list, prefix + FHAIR_SUFFIX)
            alt_night(v_list, prefix + BHAIR_SUFFIX)
        
        else:
            v_list.append(prefix + FHAIR_SUFFIX + FILE_EXT)
            v_list.append(prefix + BHAIR_SUFFIX + FILE_EXT)




    lean_acs_blacklist = [
        "test"
    ]


    HAIRS = [
        "def", 
        "down" 
    ]


    CLOTHES = [
        "def" 
    ]


    def adjust_zoom():
        """
        Sets the value zoom to an appropraite amoutn based on the current
        zoom level.
        NOTE: also sets the persistent save for zoom
        """
        global value_zoom, adjust_y
        if zoom_level > default_zoom_level:
            value_zoom = default_value_zoom + (
                (zoom_level-default_zoom_level) * zoom_step
            )
            adjust_y = default_y + ((zoom_level-default_zoom_level) * y_step)
        
        elif zoom_level < default_zoom_level:
            value_zoom = default_value_zoom - (
                (default_zoom_level-zoom_level) * zoom_step
            )
            adjust_y = default_y
        else:
            
            value_zoom = default_value_zoom
            adjust_y = default_y
        
        store.persistent._mas_zoom_zoom_level = zoom_level


    def reset_zoom():
        """
        Resets the zoom to the default value
        NOTE: also set sthe persistent save for zoom
        """
        global zoom_level
        zoom_level = default_zoom_level
        adjust_zoom()


    def zoom_out():
        """
        zooms out to the farthest zoom level
        NOTE: also sets the persistent save for zoom
        """
        global zoom_level
        zoom_level = 0
        adjust_zoom()




    def tryparsehair(_hair, default="def"):
        """
        Returns the given hair if it exists, or the default if not exist

        IN:
            _hair - hair to check for existence
            default - default if hair dont exist

        RETURNS:
            the hair if it exists, or default if not
        """
        if _hair in HAIRS:
            return _hair
        
        return default



    def tryparseclothes(_clothes, default="def"):
        """
        Returns the given clothes if it exists, or the default if not exist

        IN:
            _clothes - clothes to check for existence
            default - default if clothes dont exist

        RETURNS:
            the clothes if it exists, or default if not
        """
        if _clothes in CLOTHES:
            return _clothes
        
        return default



    ACS_MAP = dict()


    HAIR_MAP = dict()


    CLOTH_MAP = dict()


    SP_ACS = store.mas_sprites_json.SP_ACS
    SP_HAIR = store.mas_sprites_json.SP_HAIR
    SP_CLOTHES = store.mas_sprites_json.SP_CLOTHES

    SP_MAP = {
        SP_ACS: ACS_MAP,
        SP_HAIR: HAIR_MAP,
        SP_CLOTHES: CLOTH_MAP
    }


    LEAN_TYPES = [
        "def"
    ]


    NUM_POSE = {
        1: "steepling",
        2: "crossed",
        3: "restleftpointright",
        4: "pointright",
        5: "def|def",
        6: "down",
        7: "downleftpointright",
    }



    POSES = [
        NUM_POSE[1],
        NUM_POSE[2],
        NUM_POSE[3],
        NUM_POSE[4],
        NUM_POSE[6],
        NUM_POSE[7],
    ]





    L_POSES = [
        NUM_POSE[5],
    ]



    ALL_POSES = []
    ALL_POSES.extend(POSES)
    ALL_POSES.extend(L_POSES)


    NUM_ARMS = {
        1: "crossed",
        2: "left-down",
        3: "left-rest",
        4: "right-down",
        5: "right-point",
        6: "right-restpoint",
        7: "steepling",
        8: "def|left-def",
        9: "def|right-def",
    }


    ARMS = list(NUM_ARMS.values())



    LEAN_ARMS = {
        LEAN_TYPES[0]: (8, 9),
    }


    ARMS_LEAN = {}
    for lean, values in LEAN_ARMS.iteritems():
        for value in values:
            ARMS_LEAN[value] = lean


    EXPROP_TOPIC_MAP = {
        EXP_A_LHSEL: [
            "monika_hairclip_select"
        ],
    }


    ACSTYPE_TOPIC_MAP = {
        "ribbon": "monika_ribbon_select"
    }

    def _genLK(keys):
        """
        generates a tuple of keys + leanables using the given kens

        Leanable Keys are keys prefixed with a lean type like: <lean>|<key>

        IN:
            keys - iterable of keys to use

        RETURNS: tuple of keys + leanable keys
        """
        key_list = list(keys)
        for lean in LEAN_TYPES:
            key_list.extend([lean + "|" + key for key in keys])
        
        return tuple(key_list)


    def _verify_uprightpose(val):
        return val in POSES


    def _verify_lean(val):
        return val in LEAN_TYPES


    def _verify_leaningpose(val):
        return val in L_POSES


    def _verify_pose(val, allow_none=True):
        if val is None:
            return allow_none
        return _verify_uprightpose(val) or _verify_leaningpose(val)


    def acs_lean_mode(sprite_list, lean):
        """
        NOTE: DEPRECATED

        Adds the appropriate accessory prefix dpenedong on lean

        IN:
            sprite_list - list to add sprites to
            lean - type of lean
        """
        if lean:
            sprite_list.extend((
                PREFIX_ACS_LEAN,
                lean,
                ART_DLM
            ))
        
        else:
            sprite_list.append(PREFIX_ACS)


    def face_lean_mode(lean):
        """
        Returns the appropriate face prefix depending on lean

        IN:
            lean - type of lean

        RETURNS:
            appropriat eface prefix string
        """
        if lean:
            return "".join((
                PREFIX_FACE_LEAN,
                lean,
                ART_DLM
            ))
        
        return PREFIX_FACE


    def create_remover(acs_type, group, mux_types):
        """
        Creates a remover ACS

        IN:
            acs_type - acs type for the remover. This is also used in mux_type
            group - group of selectables this ACS remover should be linked to
                This is used in the naming of the ACS.
            mux_types - list of types to use for mux_type

        RETURNS: remover ACS object
        """
        remover_acs = store.MASAccessory(
            group + "-remover",
            "ribbon_blank",
            store.MASPoseMap(
                default="0",
                use_reg_for_l=True
            ),
            stay_on_start=False,
            acs_type=acs_type,
            mux_type=mux_types
        )
        init_acs(remover_acs)
        return remover_acs

    def init_acs(mas_acs):
        """
        Initlializes the given MAS accessory into a dictionary map setting

        IN:
            mas_acs - MASAccessory to initialize
        """
        if mas_acs.name in ACS_MAP:
            raise Exception(
                "MASAccessory name '{0}' already exists.".format(mas_acs.name)
            )
        
        
        ACS_MAP[mas_acs.name] = mas_acs


    def init_hair(mas_hair):
        """
        Initlializes the given MAS hairstyle into a dictionary map setting

        IN:
            mas_hair - MASHair to initialize
        """
        if mas_hair.name in HAIR_MAP:
            raise Exception(
                "MASHair name '{0}' already exists.".format(mas_hair.name)
            )
        
        
        HAIR_MAP[mas_hair.name] = mas_hair


    def init_clothes(mas_cloth):
        """
        Initlializes the given MAS clothes into a dictionary map setting

        IN:
            mas_clothes - MASClothes to initialize
        """
        if mas_cloth.name in CLOTH_MAP:
            raise Exception(
                "MASClothes name '{0}' already exists.".format(mas_cloth.name)
            )
        
        
        CLOTH_MAP[mas_cloth.name] = mas_cloth


    def rm_acs(acs):
        """
        Deletes an ACS by removing it from the map

        IN:
            acs - ACS to remove
        """
        if acs.name in ACS_MAP:
            ACS_MAP.pop(acs.name)


    def lock_exprop_topics(exprop):
        """
        Locks topics with the given exprop

        IN:
            exprop - extended property to lock associated topics wtih
        """
        topic_list = EXPROP_TOPIC_MAP.get(exprop, None)
        if topic_list is not None:
            for topic in topic_list:
                store.mas_lockEVL(topic, "EVE")


    def lock_acstype_topics(acs_type):
        """
        Locks topics with the given acs type

        IN:
            acstype - acs type to lock assicated topics with
        """
        topic_label = ACSTYPE_TOPIC_MAP.get(acs_type, None)
        if topic_label is not None:
            store.mas_lockEVL(topic_label, "EVE")


    def unlock_exprop_topics(exprop):
        """
        Unlocks topics with the given exprop

        IN:
            exprop - extended property to unlock associated topics with
        """
        topic_list = EXPROP_TOPIC_MAP.get(exprop, None)
        if topic_list is not None:
            for topic in topic_list:
                store.mas_unlockEVL(topic, "EVE")


    def unlock_acstype_topics(acs_type):
        """
        Unlocks topics with the given acs type

        IN:
            acstype - acs type to unlock associated topics with
        """
        topic_label = ACSTYPE_TOPIC_MAP.get(acs_type, None)
        if topic_label is not None:
            store.mas_unlockEVL(topic, "EVE")


    def should_disable_lean(lean, arms, character):
        """
        Figures out if we need to disable the lean or not based on current
        character settings

        IN:
            lean - lean type we want to do
            arms - arms type involved with lean
            character - MASMonika object

        RETURNS:
            True if we should disable lean, False otherwise
        """
        if lean is None:
            return False
        
        
        if len(character.lean_acs_blacklist) > 0:
            
            return True
        
        larms = lean + "|" + arms
        
        if not character.hair.pose_map.l_map.get(larms, False):
            return True
        
        if not character.clothes.pose_map.l_map.get(larms, False):
            return True
        
        
        return False


    def build_loc():
        """
        RETURNS location string for the sprite
        """
        return "".join(("(", str(adjust_x), ",", str(adjust_y), ")"))


    def build_loc_val():
        """
        RETURNS location tuple for a sprite
        """
        return (adjust_x, adjust_y)


    def get_sprite(sprite_type, sprite_name):
        """
        Returns the sprite object with the given sprite name and sprite type.
        Or None if we couldn't find one.
        """
        
        sprite_map = SP_MAP.get(sprite_type, None)
        if sprite_map is None:
            return None
        
        
        return sprite_map.get(sprite_name, None)
























    def acs_rm_exit_pre_change(temp_space, moni_chr, rm_acs, acs_loc):
        """
        Runs before exit point runs for acs

        IN:
            temp_space - temp space
            moni_chr - MASMonika object
            rm_acs - acs we are removing
            acs_loc - acs location to rm this acs from
        """
        pass


    def acs_rm_exit_pst_change(temp_space, moni_chr, rm_acs, acs_loc):
        """
        Runs after exit point runs runs for acs

        IN:
            temp_space - temp space
            moni_chr - MASMonika object
            rm_acs - acs we are removing
            acs_loc -  acs location to rm this acs from
        """
        if store.mas_selspr.in_prompt_map(rm_acs.acs_type):
            store.mas_selspr.set_prompt(rm_acs.acs_type, "wear")


    def acs_wear_mux_pre_change(temp_space, moni_chr, new_acs, acs_loc):
        """
        Runs before mux type acs are removed

        IN:
            temp_space - temp space
            moni_chr - MASMonika object
            new_acs - acs we are adding
            acs_loc - acs location to wear this acs
        """
        
        if not is_hairacs_compatible(moni_chr.hair, new_acs):
            temp_space["abort"] = True


    def acs_wear_mux_pst_change(temp_space, moni_chr, new_acs, acs_loc):
        """
        Runs after mux type acs removed, before insertion

        IN:
            temp space - temp space
            moni_chr - MASMonika object
            new_acs - acs we are adding
            acs_loc - acs location to wear this acs
        """
        pass


    def acs_wear_entry_pre_change(temp_space, moni_chr, new_acs, acs_loc):
        """
        Runs after insertion, before entry pooint

        IN:
            temp_space - temp space
            moni_chr - MASmonika object
            new_acs - acs we are adding
            acs_loc - acs location to wear this acs
        """
        pass


    def acs_wear_entry_pst_change(temp_space, moni_chr, new_acs, acs_loc):
        """
        Runs after entry point

        IN:
            temp_space - temp space
            moni_chr - MASMonika object
            new_acs - acs we are adding
            acs_loc - acs location to wear this acs
        """
        if store.mas_selspr.in_prompt_map(new_acs.acs_type):
            store.mas_selspr.set_prompt(new_acs.acs_type, "change")


    def clothes_exit_pre_change(temp_space, moni_chr, prev_cloth, new_cloth):
        """
        Runs pre clothes change code. This code is ran prior to clothes being
        changed and prior to exit prog point

        IN:
            temp_space - temporary dictionary space
            moni_chr - MASMonika object
            prev_cloth - current clothes
            new_cloth - clothes we are changing to
        """
        pass


    def clothes_exit_pst_change(temp_space, moni_chr, prev_cloth, new_cloth):
        """
        Runs after exit prog point is ran, before the actual change.

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_cloth - current clothes
            new_cloth - clothes we are changing to
        """
        
        
        desired_ribbon = prev_cloth.getprop("desired-ribbon")
        if (
                desired_ribbon is not None
                and desired_ribbon in ACS_MAP
                and moni_chr.is_wearing_hair_with_exprop("ribbon")
        ):
            temp_ribbon = temp_storage.get("hair.ribbon", None)
            if temp_ribbon is None:
                moni_chr.remove_acs(ACS_MAP[desired_ribbon])
            
            else:
                moni_chr.wear_acs(temp_ribbon)


    def clothes_entry_pre_change(temp_space, moni_chr, prev_cloth, new_cloth):
        """
        Runs after change, before entry prog point.

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_cloth - current clothes
            new_cloth - clothes we are changing to
        """
        if prev_cloth.hasprop("baked outfit"):
            
            
            _hair_unlock_select_if_needed()
            store.mas_selspr._validate_group_topics()


    def clothes_entry_pst_change(temp_space, moni_chr, prev_cloth, new_cloth):
        """
        Runs after entry prog point

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_cloth - current clothes
            new_cloth - clothes we are changing to
        """
        outfit_mode = temp_space.get("outfit_mode", False)
        
        
        desired_ribbon = new_cloth.getprop("desired-ribbon")
        if (
                outfit_mode
                and desired_ribbon is not None
                and desired_ribbon in ACS_MAP
                and moni_chr.is_wearing_hair_with_exprop("ribbon")
        ):
            prev_ribbon = moni_chr.get_acs_of_type("ribbon")
            if prev_ribbon is None:
                prev_ribbon = moni_chr.get_acs_of_exprop("ribbon-like")
            
            if prev_ribbon != store.mas_acs_ribbon_blank:
                temp_storage["hair.ribbon"] = prev_ribbon
            
            moni_chr.wear_acs(ACS_MAP[desired_ribbon])
        
        
        
        
        if not is_clotheshair_compatible(new_cloth, moni_chr.hair):
            moni_chr.reset_hair(False)


    def hair_exit_pre_change(temp_space, moni_chr, prev_hair, new_hair):
        """
        Runs pre hair change code. This code is ran prior to hair being
        changed and prior to exit prog point.

        IN:
            temp_space - temporary dictionary space
            moni_chr - MASMonika object
            prev_hair - current hair
            new_hair - hair we are changing to
        """
        
        if not is_clotheshair_compatible(moni_chr.clothes, new_hair):
            temp_space["abort"] = True
            return
        
        all_acs = moni_chr.get_acs()
        for acs in all_acs:
            if not is_hairacs_compatible(new_hair, acs):
                moni_chr.remove_acs(acs)


    def hair_exit_pst_change(temp_space, moni_chr, prev_hair, new_hair):
        """
        Runs after exit prog point is ran, before the actual change.

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_hair - current hair
            new_hair - hair we are changing to
        """
        pass


    def hair_entry_pre_change(temp_space, moni_chr, prev_hair, new_hair):
        """
        Runs after change, before entry prog point.

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            preV_hair - current hair
            new_hair - hair we are changing to
        """
        pass


    def hair_entry_pst_change(temp_space, moni_chr, prev_hair, new_hair):
        """
        Runs after entry prog point

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_hair - current hair
            new_hair - hair we are changing to
        """
        startup = temp_space.get("startup", False)
        
        if new_hair.hasprop("ribbon"):
            
            
            if new_hair.hasprop("ribbon-restore"):
                temp_ribbon = temp_storage.get("hair.ribbon", None)
                
                
                if not startup and temp_ribbon is not None:
                    
                    _acs_wear_if_not_wearing_type(
                        moni_chr,
                        "ribbon",
                        temp_ribbon




                    )
            
            elif new_hair.hasprop("ribbon-off"):
                
                _acs_ribbon_save_and_remove(moni_chr)
                _acs_ribbon_like_save_and_remove(_moni_chr)
            
            if not moni_chr.is_wearing_clothes_with_exprop("baked outfit"):
                
                store.mas_filterUnlockGroup(SP_ACS, "ribbon")
            
            
            if moni_chr.is_wearing_ribbon():
                store.mas_selspr.set_prompt("ribbon", "change")
            
            else:
                store.mas_selspr.set_prompt("ribbon", "wear")
        
        else:
            
            _acs_ribbon_save_and_remove(moni_chr)
            _acs_ribbon_like_save_and_remove(moni_chr)



    def is_hairacs_compatible(hair, acs):
        """
        Checks if the given hair is compatible with the given acs

        IN:
            hair - hair to check
            acs - acs to check

        RETURNS: True if hair+acs is compatible, False if not
        """
        
        req_hair_prop = acs.getprop(EXP_A_RQHP, None)
        if req_hair_prop is not None and not hair.hasprop(req_hair_prop):
            return False
        
        
        excl_hair_props = acs.getprop(EXP_A_EXCLHP, None)
        if excl_hair_props is not None:
            for excl_hair_prop in excl_hair_props:
                if hair.hasprop(excl_hair_prop):
                    return False
        
        return True


    def is_clotheshair_compatible(clothes, hair):
        """
        Checks if the given clothes is compatible with the given hair

        IN:
            clothes - clothes to check
            hair - hair to check

        RETURNS: True if clothes+hair is comaptible, False if not
        """
        
        req_cloth_prop = hair.getprop(EXP_H_RQCP, None)
        if req_cloth_prop is not None and not clothes.hasprop(req_cloth_prop):
            return False
        
        
        excl_cloth_props = hair.getprop(EXP_H_EXCLCP, None)
        if excl_cloth_props is not None:
            for excl_cloth_prop in excl_cloth_props:
                if clothes.hasprop(excl_cloth_prop):
                    return False
        
        return True




    def _ms_head(clothing, hair, head):
        """
        Creates head string

        IN:
            clothing - type of clothing
            hair - type of hair
            head - type of head

        RETURNS:
            head string
        """
        
        return "".join([
            build_loc(),
            ',"',
            S_MAIN,
            clothing,
            "/",
            hair,
            ART_DLM,
            head,
            FILE_EXT,
            '"'
        ])


    def _ms_left(clothing, hair, left):
        """
        Creates left side string

        IN:
            clothing - type of clothing
            hair - type of hair
            left - type of left side

        RETURNS:
            left side stirng
        """
        
        return "".join([
            build_loc(),
            ',"',
            S_MAIN,
            clothing,
            "/",
            hair,
            ART_DLM,
            left,
            FILE_EXT,
            '"'
        ])


    def _ms_right(clothing, hair, right):
        """
        Creates right body string

        IN:
            clothing - type of clothing
            hair - type of hair
            right - type of right side

        RETURNS:
            right body string
        """
        
        return "".join([
            build_loc(),
            ',"',
            S_MAIN,
            clothing,
            "/",
            hair,
            ART_DLM,
            head,
            FILE_EXT,
            '"'
        ])


    def _ms_standing(clothing, hair, head, left, right, acs_list):
        """
        Creates the custom standing string
        This is different than the stock ones because of image location

        IN:
            clothing - type of clothing
            hair - type of hair
            head - type of head
            left - type of left side
            right - type of right side
            acs_list - list of MASAccessory objects
                NOTE: this should the combined list because we don't have
                    layering in standing mode

        RETURNS:
            custom standing sprite
        """
        
        return "".join([
            I_COMP,
            "(",
            LOC_STAND,
            ",",
            _ms_left(clothing, hair, left),
            ",",
            _ms_right(clothing, hair, right),
            ",",
            _ms_head(clothing, hair, head),
            _ms_accessorylist(acs_list, False, False),
            ")"
        ])


    def _ms_standingstock(head, left, right, acs_list, single=None):
        """
        Creates the stock standing string
        This is different then the custom ones because of image location

        Also no night version atm.

        IN:
            head - type of head
            left - type of left side
            right - type of right side
            acs_list - list of MASAccessory objects
                NOTE: this should be the combined list because we don't have
                    layering in standing mode
            single - type of single standing picture.
                (Defualt: None)

        RETURNS:
            stock standing string
        """
        
        
        if single:
            return "".join([
                I_COMP,
                "(",
                LOC_STAND,
                ",",
                build_loc(),
                ',"',
                STOCK_ART_PATH,
                single,
                FILE_EXT,
                '"',

                ")"
            ])
        
        return "".join([
            I_COMP,
            "(",
            LOC_STAND,
            ",",
            build_loc(),
            ',"',
            STOCK_ART_PATH,
            left,
            FILE_EXT,
            '",',
            build_loc(),
            ',"',
            STOCK_ART_PATH,
            right,
            FILE_EXT,
            '",',
            build_loc(),
            ',"',
            STOCK_ART_PATH,
            head,
            FILE_EXT,
            '"',

            ")"
        ])



init -10 python:

    class MASHighlightMap(object):
        """SEALED
        Maps arbitrary keys to <MASFilterMap> objects

        DO NOT EXTEND THIS CLASS. If you need similar functionality, make a
        wrapper around this. This class contains functions that may crash
        when used in an unexpected context.

        NOTE: values dont have to be MASFilterMAP objects, but certain
            functions will fail if not.

        NOTE: this can iterated over to retrieve all objects in here
            EXCEPT for the default.

        PROPERTIES:
            None. Use provided functions to manipulate the map.
        """
        _m1_sprite0x2dchart__KEY_ALL = "*"
        
        def __init__(self, keys, default=None):
            """
            Constructor

            IN:
                keys - iterable of keys that we are allowed to use.
                    NOTE: the default catch all key of "*" (KEY_ALL) does NOt
                    need to be in here.
                default - value to use as the default/catch all object. This
                    is assigned to the KEY_ALL key.
            """
            self._m1_sprite0x2dchart__map = { self._m1_sprite0x2dchart__KEY_ALL: default }
            
            
            key_list = list(keys)
            if self._m1_sprite0x2dchart__KEY_ALL in key_list:
                key_list.remove(self._m1_sprite0x2dchart__KEY_ALL)
            
            
            self._m1_sprite0x2dchart__valid_keys = tuple(set(key_list))
        
        def __iter__(self):
            """
            Iterator object (generator)
            """
            for key in self._m1_sprite0x2dchart__valid_keys:
                item = self.get(key)
                if item is not None:
                    yield item
        
        def _add_key(self, new_key, new_value=None):
            """
            Adds a key to the valid keys list. Also adds a value if desired
            NOTE: this is not intended to be done wildly. Please do not
            make a habit of adding keys after construction.
            NOTE: do not use this to add values. if the given key already
            exists, the value is ignored.

            IN:
                new_key - new key to add
                new_value - new value to associate with this key
                    (Default: None)
            """
            if new_key not in self._m1_sprite0x2dchart__valid_keys and new_key != self._m1_sprite0x2dchart__KEY_ALL:
                key_list = list(self._m1_sprite0x2dchart__valid_keys)
                key_list.append(new_key)
                self._m1_sprite0x2dchart__valid_keys = tuple(key_list)
                self.add(new_key, new_value)
        
        def add(self, key, value):
            """
            Adds value to map.
            NOTE: type is enforced here. If the given item is None
            it is ignored.
            NOTE: this will NOT set the default even if KEY_ALL is passed in

            IN:
                key - key to store item to
                value - value to add
                    if None is passed, this is equivalent to clear
            """
            if value is None:
                self.clear(key)
                return
            
            if key == self._m1_sprite0x2dchart__KEY_ALL or key not in self._m1_sprite0x2dchart__valid_keys:
                return
            
            
            self._m1_sprite0x2dchart__map[key] = value
        
        def apply(self, mapping):
            """
            Applies the given dict mapping to this MASHighlightMap.
            NOTE: will not add invalid keys.

            IN:
                mapping - dict of the following format:
                    key: valid key for this map
                    value: value to add
            """
            for key in mapping:
                self.add(key, mapping[key])
        
        def clear(self, key):
            """
            Clears value with the given key.
            NOTE: will NOT clear the default even if KEY_ALL is passed in

            IN:
                key - key to clear with
            """
            if key != self._m1_sprite0x2dchart__KEY_ALL and key in self._m1_sprite0x2dchart__map:
                self._m1_sprite0x2dchart__map.pop(key)
        
        @staticmethod
        def clear_hl_mapping(hl_mpm_data):
            """
            Clears hl mapping in the given hl data object. AKA: Sets the
            hl mapping portion of a pre-MHM MPM to {}.

            NOTE: this should only be used with  the MASPoseMap._transform
            function with MASAccessory

            IN:
                hl_mpm_data - hl data set in a MASPoseMap.

            RETURNS: hl data to set in a MASPoseMap.
            """
            if hl_mpm_data is None:
                return None
            return (hl_mpm_data[0], {})
        
        @staticmethod
        def convert_mpm(hl_keys, mpm):
            """
            Converts hl mappings in a MASPoseMap to MASHighlightMAp objects

            IN:
                hl_keys - highlight keys to use
                mpm - MASPoseMap object to convert
            """
            if mpm is None:
                return
            
            
            pargs = {}
            for param in MASPoseMap.P_PARAM_NAMES:
                hl_data = mpm.get(MASPoseMap.pn2lp(param), None)
                if hl_data is None:
                    pargs[param] = None
                else:
                    pargs[param] = MASHighlightMap.create_from_mapping(
                        hl_keys,
                        hl_data[0],
                        hl_data[1]
                    )
            
            
            mpm._modify(**pargs)
        
        @staticmethod
        def create_from_mapping(hl_keys, hl_def, hl_mapping):
            """
            Creates a MASHighlightMap using keys/default/mapping

            IN:
                hl_keys - list of keys to use
                hl_def - default highlight to use. Can be None
                hl_mapping - mapping to use.

            RETURNS: created MASHighlightMap
            """
            mhm = MASHighlightMap(hl_keys, default=hl_def)
            mhm.apply(hl_mapping)
            return mhm
        
        def fltget(self, key, flt, defval=None):
            """
            Combines getting from here and getting the resulting MASFilterMap
            object.

            IN:
                key - key to get from this map
                flt - filter to get from associated MASFilterMap, if found
                defval - default value to return if no flt value could be
                    found.
                    (Default: None)

            RETURNS: value in the MASFilterMap associated with the given
                flt, using the MASFilterMap associated with the given key.
                or defval if no valid MASfilterMap or value found.
            """
            mfm = self.get(key)
            if mfm is None:
                return defval
            
            return mfm.get(flt, defval=defval)
        
        @staticmethod
        def fromJSON(json_obj, msg_log, ind_lvl, hl_keys):
            """
            Builds hl data from JSON data

            IN:
                json_obj - JSON object to parse
                ind_lvl - indentation level
                    NOTE: this function handles loading/success log so
                    do NOT increment indent when passing in
                hl_keys - expected keys of this highlight map

            OUT:
                msg_log - list to add messagse to

            RETURNS: hl_data, ready to passed split and passed into
                create_from_mapping. Tuple:
                [0] - default MASFilterMap object
                [1] - dict:
                    key: hl_key
                    value: MASFilterMap object
                or None if no data, False if failure in parsing occured
            """
            
            msg_log.append((
                store.mas_sprites_json.MSG_INFO_T,
                ind_lvl,
                store.mas_sprites_json.MHM_LOADING
            ))
            
            
            hl_data = MASHighlightMap._fromJSON_hl_data(
                json_obj,
                msg_log,
                ind_lvl + 1,
                hl_keys
            )
            
            
            if hl_data is False:
                
                return False
            
            
            msg_log.append((
                store.mas_sprites_json.MSG_INFO_T,
                ind_lvl,
                store.mas_sprites_json.MHM_SUCCESS
            ))
            
            return hl_data
        
        def get(self, key):
            """
            Gets value wth the given key.

            IN:
                key - key of item to get

            RETURNS: MASFilterMap object, or None if not found
            """
            if key in self._m1_sprite0x2dchart__map:
                return self._m1_sprite0x2dchart__map[key]
            
            
            return self.getdef()
        
        def getdef(self):
            """
            Gets the default value

            RETURNS: MASFilterMap object, or NOne if not found
            """
            return self._m1_sprite0x2dchart__map.get(self._m1_sprite0x2dchart__KEY_ALL, None)
        
        def keys(self):
            """
            gets keys in this map

            RETURNS: tuple of keys
            """
            return self._m1_sprite0x2dchart__valid_keys
        
        @staticmethod
        def o_fltget(mhm, key, flt, defval=None):
            """
            Similar to fltget, but on a MASHighlightMap object.
            NOTE: does None checks of mhm and flt.

            IN:
                mhm - MASHighlightMap object to run fltget on
                key - key to get MASFilterMap from mhm
                flt - filter to get from associated MASFilterMap
                defval - default value to return if no flt value could be found
                    (Default: None)

            RETURNS: See fltget
            """
            if mhm is None or flt is None:
                return defval
            
            return mhm.fltget(key, flt, defval=defval)
        
        def setdefault(self, value):
            """
            Sets the default value

            IN:
                value - value to use as default
            """
            if value is None or isinstance(value, MASFilterMap):
                self._m1_sprite0x2dchart__map[self._m1_sprite0x2dchart__KEY_ALL] = value


init -3 python:



    import math
    from collections import namedtuple


    class MASMonika(renpy.store.object):
        import store.mas_sprites as mas_sprites
        
        
        PRE_ACS = 0 
        MID_ACS = 1 
        PST_ACS = 2 
        BBH_ACS = 3 
        BFH_ACS = 4 
        AFH_ACS = 5 
        BBA_ACS = 6 
        MAB_ACS = 7 
        BSE_ACS = 8 
        ASE_ACS = 9 
        BAT_ACS = 10 
        MAT_ACS = 11 
        
        
        
        
        
        
        REC_LAYERS = (
            PRE_ACS,
            BBH_ACS,
            BFH_ACS,
            AFH_ACS,
            MID_ACS,
            PST_ACS,
            BBA_ACS,
            MAB_ACS,
            BSE_ACS,
            ASE_ACS,
            BAT_ACS,
            MAT_ACS,
        )
        
        
        SPL_LAYERS = (
            BSE_ACS,
            ASE_ACS,
        )

        RENDER_ORDER = (
            PRE_ACS,
            BBH_ACS,
            BSE_ACS,
            BBA_ACS,
            ASE_ACS,
            BAT_ACS,
            MAT_ACS,
            MAB_ACS,
            BFH_ACS,
            AFH_ACS,
            MID_ACS,
            PST_ACS,
        )
        
        def __init__(self):
            """
            Constructor
            """
            self.name="Monika"
            self.haircut="default"
            self.haircolor="default"
            self.skin_hue=0 
            self.lipstick="default" 
            
            self.clothes = mas_clothes_def 
            self.hair = mas_hair_def 
            
            
            
            self.lean_acs_blacklist = []
            
            self.acs = {
                
                self.PRE_ACS: [],

                
                self.BBH_ACS: [],

                
                self.BSE_ACS: [],

                
                self.BBA_ACS: [],

                
                self.ASE_ACS: [],

                
                self.BAT_ACS: [],

                
                self.MAT_ACS: [],

                
                self.MAB_ACS: [],

                
                self.BFH_ACS: [],

                
                self.AFH_ACS: [],

                
                self.MID_ACS: [],

                
                self.PST_ACS: [],
            }
            
            
            
            self.acs_list_map = {}
            
            
            
            self.lock_hair = False
            
            
            self.lock_clothes = False
            
            
            self.lock_acs = False
            
            
            self._override_rec_layer = False
            
            
            
            
            
            
            self.tablechair = MASTableChair("def", "def")
        
        def __repr__(self):
            """
            this is lengthy and will contain all objects
            """
            
            
            acs_str_map = (
                "PRE",
                "BBH",
                "BSE",
                "BBA",
                "ASE",
                "BAT",
                "MAT",
                "MAB",
                "BFH",
                "AFH",
                "MID",
                "PST",
            )
            acs_str = []
            for idx, pfx in enumerate(acs_str_map):
                rec_layer = self.RENDER_ORDER[idx]
                acs_list = self._m1_sprite0x2dchart__get_acs(rec_layer)
                if len(acs_list) > 0:
                    acs_str.append("{0}: {1}".format(pfx, acs_list))
            
            return "<Monika: ({0}, {1}, {2}, {3})>".format(
                self.clothes,
                self.hair,
                ", ".join(acs_str),
                self.tablechair
            )
        
        def _m1_sprite0x2dchart__get_acs(self, acs_type):
            """
            Returns the accessory list associated with the given type

            IN:
                acs_type - the accessory type to get

            RETURNS:
                accessory list, or None if the given acs_type is not valid
            """
            return self.acs.get(acs_type, None)
        
        def _determine_poses(self, lean, arms):
            """
            determines the lean/pose/hair/baked data for monika based on
            the requested lean and arms

            IN:
                lean - requested lean
                arms - requested arms

            RETURNS: tuple of the following format:
                [0] - lean to use
                [1] - leanpose to use
                [2] - arms to use
                [3] - hair to use
                [4] - base arms to use
                [5] - pose arms to use
            """
            
            if store.mas_sprites.should_disable_lean(lean, arms, self):
                
                
                lean = None
                arms = "steepling"
            
            
            if self.hair.pose_map.is_fallback():
                arms, lean = self.hair.get_fallback(arms, lean)
            
            if self.clothes.pose_map.is_fallback():
                arms, lean = self.clothes.get_fallback(arms, lean)
            
            
            if self.clothes.has_hair_map():
                hair = store.mas_sprites.HAIR_MAP.get(
                    self.clothes.get_hair(self.hair.name),
                    mas_hair_def
                )
            
            else:
                hair = self.hair
            
            
            if lean is not None:
                leanpose = lean + "|" + arms
            else:
                leanpose = arms
            
            
            
            
            
            
            
            
            
            
            
            base_arms = [
                store.mas_sprites.base_arms.get(arm_id)
                for arm_id in store.mas_sprites.base_mpm.get(leanpose, [7])
            ]
            if self.clothes.pose_arms is None:
                pose_arms = base_arms
            
            else:
                pose_arms = self.clothes.pose_arms.getflp(leanpose)
            
            return (lean, leanpose, arms, hair, base_arms, pose_arms)
        
        def _same_state_acs(self, a1, a2):
            """
            Compares given acs lists as acs objects

            NOTE: order does not matter

            IN:
                a1 - list of acs objects to compare
                a2 - list of acs objects to compare

            RETURNS: True if the same, False if not
            """
            
            if len(a1) != len(a2):
                return False
            
            
            a2_names = [acs.name for acs in a2]
            
            
            same_count = 0
            for a1_acs in a1:
                if a1_acs.name in a2_names:
                    same_count += 1
                else:
                    return False
            
            return len(a2_names) == same_count
        
        def _same_state_acs_prims(self, a1, a2):
            """
            Compares given acs lists as primitive data.

            NOTE: order does not matter

            IN:
                a1 - list of acs names to compare
                a2 - list of acs names to compare

            RETURNS: True if the same, False if not
            """
            
            if len(a1) != len(a2):
                return False
            
            same_count = 0
            for a1_name in a1:
                if a1_name in a2:
                    same_count += 1
                else:
                    return False
            
            return len(a2) == same_count
        
        def _same_state(self, data):
            """
            Compares the given state as objects

            IN:
                data - previous object state

            RETURNS: True if the same, False if not
            """
            
            
            
            curr_state = self.save_state(True, True, True, False)
            
            
            if len(data) != len(curr_state):
                return False
            
            
            if data[0].name != curr_state[0].name:
                return False
            
            
            if data[1].name != curr_state[1].name:
                return False
            
            
            for index in range(2, len(data)):
                if not self._same_state_acs(data[index], curr_state[index]):
                    return False
            
            return True
        
        def _same_state_prims(self, data):
            """
            Compares the given state as primitives

            IN:
                data - previous primitive state

            RETURNS: True if the same, False if not
            """
            
            
            
            curr_state = self.save_state(True, True, True, True)
            
            
            if len(data) != len(curr_state):
                return False
            
            
            if data[0] != curr_state[0]:
                return False
            
            
            if data[1] != curr_state[1]:
                return False
            
            
            for index in range(2, len(data)):
                if not self._same_state_acs_prims(data[index], curr_state[index]):
                    return False
            
            return True
        
        def _load(self,
                _clothes_name,
                _hair_name,
                _acs_pre_names,
                _acs_bbh_names,
                _acs_bfh_names,
                _acs_afh_names,
                _acs_mid_names,
                _acs_pst_names,
                _acs_bba_names,
                _acs_mab_names,
                _acs_bse_names,
                _acs_ase_names,
                _acs_bat_names,
                _acs_mat_names,
                startup=False
            ):
            """
            INTERNAL

            load function using names/IDs

            IN:
                _clothes_name - name of clothing to load
                _hair_name - name of hair to load
                _acs_pre_names - list of pre acs names to load
                _acs_bbh_names - list of bbh acs names to load
                _acs_bfh_names - list of bfh acs names to load
                _acs_afh_names - list of afh acs names to load
                _acs_mid_names - list of mid acs names to load
                _acs_pst_names - list of pst acs names to load
                _acs_bba_names - list of bba acs names to load
                _acs_mab_names - list of mab acs names to load
                _acs_bse_names - list of bse acs names to load
                _acs_ase_names - list of ase acs names to load
                _acs_bat_names - list of bat acs names to load
                _acs_mat_names - list of mat acs names to load
                startup - True if we are loading on start, False if not
                    (Default: False)
            """
            
            self.change_outfit(
                store.mas_sprites.CLOTH_MAP.get(_clothes_name, store.mas_clothes_def),
                store.mas_sprites.HAIR_MAP.get(_hair_name, store.mas_hair_def),
                startup=startup
            )
            
            
            self._load_acs(_acs_pre_names, self.PRE_ACS)
            self._load_acs(_acs_bbh_names, self.BBH_ACS)
            self._load_acs(_acs_bse_names, self.BSE_ACS)
            self._load_acs(_acs_bba_names, self.BBA_ACS)
            self._load_acs(_acs_ase_names, self.ASE_ACS)
            self._load_acs(_acs_bat_names, self.BAT_ACS)
            self._load_acs(_acs_mat_names, self.MAT_ACS)
            self._load_acs(_acs_mab_names, self.MAB_ACS)
            self._load_acs(_acs_bfh_names, self.BFH_ACS)
            self._load_acs(_acs_afh_names, self.AFH_ACS)
            self._load_acs(_acs_mid_names, self.MID_ACS)
            self._load_acs(_acs_pst_names, self.PST_ACS)
        
        def _load_acs(self, per_acs, acs_type):
            """
            Loads accessories from the given persistent into the given
            acs type.

            IN:
                per_acs - persistent list to grab acs from
                acs_type - acs type to load acs into
            """
            for acs_name in per_acs:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs:
                    self.wear_acs_in(_acs, acs_type)
        
        def _load_acs_obj(self, acs_objs, acs_type):
            """
            Loads accessories from a given list of accessory objects into
            the given acs type

            IN:
                acs_objs - list of acs to load
                acs_type - acs type to load acs into
            """
            for _acs in acs_objs:
                
                if _acs.name in store.mas_sprites.ACS_MAP:
                    self.wear_acs_in(_acs, acs_type)
        
        def _save_acs(self, acs_type, force_acs=False):
            """
            Generates list of accessory names to save to persistent.

            IN:
                acs_type - acs type to build acs names list
                force_acs - True means to save acs even if stay_on_start is
                    False
                    (Default: False)

            RETURNS:
                list of acs names to save to persistent
            """
            return [
                acs.name
                for acs in self.acs[acs_type]
                if force_acs or acs.stay_on_start
            ]
        
        def _save_acs_obj(self, acs_type, force_acs=False):
            """
            Generaltes list of acs objects to save

            IN:
                acs_type - acs type to buld acs list
                force_acs - True means to save acs even if stay_on_start is
                    False
                    (Default: False)

            RETURNS:
                list of acs objects to save
            """
            return [
                acs
                for acs in self.acs[acs_type]
                if force_acs or acs.stay_on_start
            ]
        
        @staticmethod
        def _verify_rec_layer(val, allow_none=True):
            if val is None:
                return allow_none
            return val in MASMonika.REC_LAYERS
        
        @staticmethod
        def _verify_spl_layer(val, allow_none=True):
            if val is None:
                return allow_none
            return val in MASMonika.SPL_LAYERS
        
        def change_clothes(
                self,
                new_cloth,
                by_user=None,
                startup=False,
                outfit_mode=False
        ):
            """
            Changes clothes to the given cloth. also sets the persistent
            force clothes var to by_user, if its not None

            IN:
                new_cloth - new clothes to wear
                by_user - True if this action was mandated by the user, False
                    if not. If None, we do NOT set the forced clothes var
                    (Default: None)
                startup - True if we are loading on startup, False if not
                    When True, we dont respect locking
                    (Default: False)
                outfit_mode - True means we should change hair/acs if it
                    completes the outfit. False means we should not.
                    NOTE: this does NOT affect hair/acs that must change for
                        consistency purposes.
                    (Default: False)
            """
            if self.lock_clothes and not startup:
                return
            
            
            temp_space = {
                "by_user": by_user,
                "startup": startup,
                "outfit_mode": outfit_mode
            }
            
            prev_cloth = self.clothes
            
            
            store.mas_sprites.clothes_exit_pre_change(
                temp_space,
                self,
                prev_cloth,
                new_cloth
            )
            
            
            if temp_space.get("abort", False):
                return
            
            
            self.clothes.exit(
                self,
                new_clothes=new_cloth,
                outfit_mode=outfit_mode
            )
            
            
            store.mas_sprites.clothes_exit_pst_change(
                temp_space,
                self,
                prev_cloth,
                new_cloth
            )
            
            
            self.clothes = new_cloth
            
            
            store.mas_sprites.clothes_entry_pre_change(
                temp_space,
                self,
                prev_cloth,
                new_cloth
            )
            
            
            self.clothes.entry(
                self,
                prev_clothes=prev_cloth,
                outfit_mode=outfit_mode
            )
            
            
            store.mas_sprites.clothes_entry_pst_change(
                temp_space,
                self,
                prev_cloth,
                new_cloth
            )
            
            if by_user is not None:
                persistent._mas_force_clothes = bool(by_user)
        
        def change_hair(self, new_hair, by_user=None, startup=False):
            """
            Changes hair to the given hair. also sets the persistent force
            hair var to by_user, if its not None

            IN:
                new_hair - new hair to wear
                by_user - True if this action was mandated by the user, False
                    if not. If None, we do NOT set the forced hair var
                    (Default: None)
                startup - True if we are loading on startup, False if not
                    When True, we dont respect locking
                    (Default: False)
            """
            if self.lock_hair and not startup:
                return
            
            
            temp_space = {
                "by_user": by_user,
                "startup": startup,
            }
            
            prev_hair = self.hair
            
            
            store.mas_sprites.hair_exit_pre_change(
                temp_space,
                self,
                prev_hair,
                new_hair
            )
            
            
            if temp_space.get("abort", False):
                return
            
            
            self.hair.exit(self, new_hair=new_hair)
            
            
            store.mas_sprites.hair_exit_pst_change(
                temp_space,
                self,
                prev_hair,
                new_hair
            )
            
            
            self.hair = new_hair
            
            
            store.mas_sprites.hair_entry_pre_change(
                temp_space,
                self,
                prev_hair,
                new_hair
            )
            
            
            self.hair.entry(self, prev_hair=prev_hair)
            
            
            store.mas_sprites.hair_entry_pst_change(
                temp_space,
                self,
                prev_hair,
                new_hair
            )
            
            if by_user is not None:
                persistent._mas_force_hair = bool(by_user)
        
        
        def change_outfit(
                self,
                new_cloth,
                new_hair,
                by_user=None,
                startup=False
            ):
            """
            Changes both clothes and hair. also sets the persisten forced vars
            to by_user, if its not None

            IN:
                new_cloth - new clothes to wear
                new_hair - new hair to wear
                by_user - True if this action ws mandated by user, False if not
                    If None, we do NOT set the forced vars
                    (Default: None)
                startup - True if we are loading on startup, False if not
                    (Default: False)
            """
            self.change_clothes(new_cloth, by_user=by_user, startup=startup)
            self.change_hair(new_hair, by_user=by_user, startup=startup)
        
        
        def get_acs(self):
            """
            Gets all acs objects currently worn by Monika

            RETURNS: list of all acs objects being worn
            """
            acs_items = []
            for acs_name in self.acs_list_map:
                acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if acs is not None:
                    acs_items.append(acs)
            
            return acs_items
        
        
        def get_acs_by_desk(self, flag_value=True):
            """
            Returns all acs that have a keep_on_desk flag set to flag_value

            IN:
                flag_value - flag value to check for
                    (Default: True)

            RETURNS: list of ACS objects with a keep_on_desk flag set to
                flag_value
            """
            acs_items = []
            for acs_name in self.acs_list.map:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.keep_on_desk == flag_value:
                    acs_items.append(_acs)
            
            return acs_items
        
        
        def get_acs_of_exprop(self, exprop, get_all=False):
            """
            Gets the acs objects currently being work of a given ex prop

            IN:
                exprop - extended property to check for
                get_all - True means we get all acs being worn of this exprop
                    False will return the first one
                    (Default: False)

            RETURNS: single matching acs or None if get_all is False, list of 
                matching acs or empty list if get_all is True.
            """
            if get_all:
                acs_items = []
            else:
                acs_items = None
            
            for acs_name in self.acs_list_map:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.hasprop(exprop):
                    if get_all:
                        acs_items.append(_acs)
                    
                    else:
                        return _acs
            
            return acs_items
        
        
        def get_acs_of_type(self, acs_type, get_all=False):
            """
            Gets the acs objects currently being worn of a given type.

            IN:
                acs_type - acs type to check for
                get_all - True means we get all acs being worn of this type,
                    False will just return the first one
                    (Default: False)

            RETURNS: single matchin acs or None if get_all is False. list of
                matching acs or empty list if get_all is True.
            """
            if get_all:
                acs_items = []
            else:
                acs_items = None
            
            for acs_name in self.acs_list_map:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.acs_type == acs_type:
                    if get_all:
                        acs_items.append(_acs)
                    else:
                        return _acs
            
            return acs_items
        
        
        def get_outfit(self):
            """
            Returns the current outfit

            RETURNS:
                tuple:
                    [0] - current clothes
                    [1] - current hair
            """
            return (self.clothes, self.hair)
        
        
        def is_wearing_acs(self, accessory):
            """
            Checks if currently wearing the given accessory

            IN:
                accessory - accessory to check

            RETURNS:
                True if wearing accessory, false if not
            """
            return accessory.name in self.acs_list_map
        
        
        def is_wearing_acs_with_exprop(self, exprop):
            """
            Checks if currently wearing any accessory with given exprop

            IN:
                exprop - extended property to check

            RETURNS: True if wearing accessory, False if not
            """
            for acs_name in self.acs_list_map:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.hasprop(exprop):
                    return True
            
            return False
        
        
        def is_wearing_acs_type(self, acs_type):
            """
            Checks if currently wearing any accessory with given type

            IN:
                acs_type - accessory type to check

            RETURNS: True if wearing acccesroy, False if not
            """
            for acs_name in self.acs_list_map:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.acs_type == acs_type:
                    return True
            
            return False
        
        
        def is_wearing_acs_types(self, *acs_types):
            """
            multiple arg version of is_wearing_acs_type

            IN:
                *acs_types - any number of acs types to check

            RETURNS: True if any the ACS types checks are True, False if not
            """
            for acs_type in acs_types:
                if self.is_wearing_acs_type(acs_type):
                    return True
            
            return False
        
        def is_wearing_acs_with_mux(self, acs_type):
            """
            Checks if currently wearing any ACS with the given acs_type in its
            mux type

            IN:
                acs_type - acceessory type to check
            """
            for acs_name in self.acs_list_map:
                acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if (
                        acs
                        and acs.mux_type is not None
                        and acs_type in acs.mux_type
                ):
                    return True
            
            return False
        
        def is_wearing_acs_in(self, accessory, acs_type):
            """
            Checks if the currently wearing the given accessory as the given
            accessory type

            IN:
                accessory - accessory to check
                acs_type - accessory type to check

            RETURNS:
                True if wearing accessory, False if not
            """
            acs_list = self._m1_sprite0x2dchart__get_acs(acs_type)
            
            if acs_list is not None:
                return accessory in acs_list
            
            return False
        
        
        def is_wearing_clothes_with_exprop(self, exprop):
            """
            Checks if we are currently wearing clothes with the given exprop

            IN:
                exprop - extended property to check

            RETURNS: True if wearing clothes with the exprop, False if not
            """
            return self.clothes.hasprop(exprop)
        
        
        def is_wearing_hair_with_exprop(self, exprop):
            """
            Checks if we are currently wearing hair with the given exprop

            IN:
                exprop - extend property to check

            RETURNS: True if wearing hair with the exprop, False if not
            """
            return self.hair.hasprop(exprop)
        
        
        def is_wearing_ribbon(self):
            """
            Checks if we are currently wearing a ribbon or ribbon-like ACS

            RETURNS: True if wearing ACS with ribbon type or ACS with
                ribbon-like ex prop
            """
            return (
                self.is_wearing_acs_type("ribbon") 
                or self.is_wearing_acs_with_exprop("ribbon-like")
            )
        
        def load(self, startup=False):
            """
            Loads hair/clothes/accessories from persistent.

            IN:
                startup - True if loading on start, False if not
                    When True, we dont respesct locking
                    (Default: False)
            """
            self._load(
                store.persistent._mas_monika_clothes,
                store.persistent._mas_monika_hair,
                store.persistent._mas_acs_pre_list,
                store.persistent._mas_acs_bbh_list,
                store.persistent._mas_acs_bfh_list,
                store.persistent._mas_acs_afh_list,
                store.persistent._mas_acs_mid_list,
                store.persistent._mas_acs_pst_list,
                store.persistent._mas_acs_bba_list,
                store.persistent._mas_acs_mab_list,
                store.persistent._mas_acs_bse_list,
                store.persistent._mas_acs_ase_list,
                store.persistent._mas_acs_bat_list,
                store.persistent._mas_acs_mat_list,
                startup=startup
            )
        
        
        def load_state(self, _data, as_prims=False):
            """
            Loads clothes/hair/acs from a tuple data format that was saved
            using the save_state function.

            IN:
                _data - data to load from. tuple of the following format:
                    [0]: clothes data
                    [1]: hair data
                    [2]: pre acs data
                    [3]: bbh acs data
                    [4]: bfh acs data
                    [5]: afh acs data
                    [6]: mid acs data
                    [7]: pst acs data
                    [8]: bba acs data
                    [9]: mab acs data
                    [10]: bse acs data
                    [11]: ase acs data
                    [12]: bat acs data
                    [13]: mat acs data
                as_prims - True if this data was saved as primitive data types,
                    false if as objects
                    (Default: False)
            """
            if as_prims:
                
                self._load(*_data)
                return
            
            
            
            self.change_outfit(_data[0], _data[1])
            
            
            for index, rec_layer in enumerate(self.REC_LAYERS):
                self._load_acs_obj(_data[index+2], rec_layer)
        
        def reset_all(self, by_user=None):
            """
            Resets all of monika

            IN:
                by_user - True if this action was mandated by user, False if
                    not. If None, we do NOT set force vars.
                    (Default: None)
            """
            self.reset_clothes(by_user)
            self.reset_hair(by_user)
            self.remove_all_acs()
        
        def remove_acs(self, accessory):
            """
            Removes the given accessory. this uses the map to determine where
            the accessory is located.

            IN:
                accessory - accessory to remove
            """
            self.remove_acs_in(
                accessory,
                self.acs_list_map.get(accessory.name, None)
            )
        
        
        def remove_acs_exprop(self, exprop):
            """
            Removes all ACS of given exprop.

            IN:
                exprop - exprop to check for
            """
            for acs_name in self.acs_list_map.keys():
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.hasprop(exprop):
                    self.remove_acs_in(_acs, self.acs_list_map[acs_name])
        
        
        def remove_acs_mux(self, mux_types):
            """
            Removes all ACS with a mux type in the given list.

            IN:
                mux_types - list of acs_types to remove from acs
            """
            for acs_name in self.acs_list_map.keys():
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.acs_type in mux_types:
                    self.remove_acs_in(_acs, self.acs_list_map[acs_name])
        
        
        def remove_acs_in(self, accessory, acs_type):
            """
            Removes the given accessory from the given accessory list type

            IN:
                accessory - accessory to remove
                acs_type - ACS type
            """
            if self.lock_acs:
                return
            
            acs_list = self._m1_sprite0x2dchart__get_acs(acs_type)
            temp_space = {
                "acs_list": acs_list,
            }
            
            if acs_list is not None and accessory in acs_list:
                
                
                store.mas_sprites.acs_rm_exit_pre_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )
                
                
                if temp_space.get("abort", False):
                    return
                
                
                accessory.exit(self)
                
                
                store.mas_sprites.acs_rm_exit_pst_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )
                
                
                if accessory.name in self.lean_acs_blacklist:
                    self.lean_acs_blacklist.remove(accessory.name)
                
                
                if accessory.name in self.acs_list_map:
                    self.acs_list_map.pop(accessory.name)
                
                
                acs_list.remove(accessory)
        
        def remove_all_acs(self):
            """
            Removes all accessories from all accessory lists
            """
            for rec_layer in self.REC_LAYERS:
                self.remove_all_acs_in(rec_layer)
        
        def remove_all_acs_in(self, acs_type):
            """
            Removes all accessories from the given accessory type

            IN:
                acs_type - ACS type to remove all
            """
            if self.lock_acs:
                return
            
            if acs_type in self.acs:
                
                for acs in self.acs[acs_type]:
                    
                    acs.exit(self)
                    
                    
                    if acs.name in self.lean_acs_blacklist:
                        self.lean_acs_blacklist.remove(acs.name)
                    
                    
                    if acs.name in self.acs_list_map:
                        self.acs_list_map.pop(acs.name)
                
                self.acs[acs_type] = list()
        
        
        def reset_clothes(self, by_user=None):
            """
            Resets clothing to default

            IN:
                by_user - True if this action was mandated by user, False if
                    not. If None, then we do NOT set force clothed vars
                    (Default: None)
            """
            self.change_clothes(mas_clothes_def, by_user)
        
        
        def reset_hair(self, by_user=None):
            """
            Resets hair to default

            IN:
                by_user - True if this action was mandated by user, False if
                    not. If None, then we do NOT set forced hair vars
                    (Default: None)
            """
            self.change_hair(mas_hair_def, by_user)
        
        
        def reset_outfit(self, by_user=None):
            """
            Resetse clothing and hair to default

            IN:
                by_user - True if this action was mandated by user, False if
                    not. If None, then we do NOT set forced vars
                    (Default: None)
            """
            self.reset_clothes(by_user)
            self.reset_hair(by_user)
        
        def restore(self, _data, as_prims=False):
            """
            Restores monika to a previous state. This will reset outfit and
            clear ACS before loading.

            IN:
                _data - see load_state
                as_prims - see load_state
            """
            self.reset_outfit()
            self.remove_all_acs()
            self.load_state(_data, as_prims=as_prims)
        
        def save(self, force_hair=False, force_clothes=False, force_acs=False):
            """
            Saves hair/clothes/acs to persistent

            IN:
                force_hair - True means we force hair saving even if
                    stay_on_start is False
                    (Default: False)
                force_clothes - True means we force clothes saving even if
                    stay_on_start is False
                    (Default: False)
                force_acs - True means we force acs saving even if
                    stay_on_start is False
                    (Default: False)
            """
            
            if force_hair or self.hair.stay_on_start:
                store.persistent._mas_monika_hair = self.hair.name
            
            if force_clothes or self.clothes.stay_on_start:
                store.persistent._mas_monika_clothes = self.clothes.name
            
            
            store.persistent._mas_acs_pre_list = self._save_acs(
                self.PRE_ACS,
                force_acs
            )
            store.persistent._mas_acs_bbh_list = self._save_acs(
                self.BBH_ACS,
                force_acs
            )
            store.persistent._mas_acs_bse_list = self._save_acs(
                self.BSE_ACS,
                force_acs
            )
            store.persistent._mas_acs_bba_list = self._save_acs(
                self.BBA_ACS,
                force_acs
            )
            store.persistent._mas_acs_ase_list = self._save_acs(
                self.ASE_ACS,
                force_acs
            )
            store.persistent._mas_acs_mab_list = self._save_acs(
                self.MAB_ACS,
                force_acs
            )
            store.persistent._mas_acs_bfh_list = self._save_acs(
                self.BFH_ACS,
                force_acs
            )
            store.persistent._mas_acs_afh_list = self._save_acs(
                self.AFH_ACS,
                force_acs
            )
            store.persistent._mas_acs_mid_list = self._save_acs(
                self.MID_ACS,
                force_acs
            )
            store.persistent._mas_acs_pst_list = self._save_acs(
                self.PST_ACS,
                force_acs
            )
        
        
        def same_state(self, data, as_prims=False):
            """
            compares if the given state is the same as current monika

            IN:
                data - data to compare
                as_prims - True if prims, False if not

            RETURNS: True if same state, False if not
            """
            if as_prims:
                return self._same_state_prims(data)
            
            return self._same_state(data)
        
        def save_state(self,
                force_hair=False,
                force_clothes=False,
                force_acs=False,
                as_prims=False
            ):
            """
            Saves hair/clothes/acs to a tuple data format that can be loaded
            later using the load_state function.

            IN:
                force_hair - True means force hair saving even if stay_on_start
                    is False. If False and stay_on_start is False, the default
                    hair will be returned.
                    (Default: False)
                force_clothes - True meanas force clothes saving even if
                    stay_on_start is False. If False and stay_on_start is
                    False, the default clothes will be returned.
                    (Default: False)
                force_acs - True means force acs saving even if stay_on_start
                    is False. At minimum, this will be an empty list.
                    (Default: False)
                as_prims - True means to save the data as primitive types
                    for persistent saving. False will save the data as
                    objects.
                    (Default: False)

            RETURNS tuple of the following format:
                [0]: clothes data (Default: mas_clothes_def)
                [1]: hair data (Default: mas_hair_def)
                [2]: pre acs data (Default: [])
                [3]: bbh acs data (Default: [])
                [4]: bfh acs data (Default: [])
                [5]: afh acs data (Default: [])
                [6]: mid acs data (Default: [])
                [7]: pst acs data (Default: [])
                [8]: bba acs data (Default: [])
                [9]: mab acs data (Default: [])
                [10]: bse acs data (Default: [])
                [11]: ase acs data (Default: [])
                [12]: bat acs data (Default: [])
                [13]: mat acs data (Default: [])
            """
            
            if force_clothes or self.clothes.stay_on_start:
                cloth_data = self.clothes
            else:
                cloth_data = mas_clothes_def
            
            
            if force_hair or self.hair.stay_on_start:
                hair_data = self.hair
            else:
                hair_data = mas_hair_def
            
            state_data = []
            
            
            if as_prims:
                state_data.extend((cloth_data.name, hair_data.name))
            else:
                state_data.extend((cloth_data, hair_data))
            
            
            for rec_layer in self.REC_LAYERS:
                if as_prims:
                    state_data.append(self._save_acs(rec_layer, force_acs))
                else:
                    state_data.append(self._save_acs_obj(rec_layer, force_acs))
            
            
            return tuple(state_data)
        
        def wear_acs(self, acs):
            """
            Wears the given accessory in that accessory's recommended
            spot, as defined by the accessory.

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, acs.get_rec_layer())
        
        def wear_acs_in(self, accessory, acs_type):
            """
            Wears the given accessory

            NOTE: will not allow mismatching layers, unless overrides are
                enabled.

            IN:
                accessory - accessory to wear
                acs_type - layer to wear the acs in.
            """
            if self.lock_acs or accessory.name in self.acs_list_map:
                
                return
            
            
            
            if (
                    acs_type != accessory.get_rec_layer()
                    and not self._override_rec_layer
            ):
                acs_type = accessory.get_rec_layer()
            
            
            
            if not self._override_rec_layer:
                if acs_type in (self.BSE_ACS, self.ASE_ACS):
                    valid_aso_type = MASAccessoryBase.ASO_SPLIT
                else:
                    valid_aso_type = MASAccessoryBase.ASO_REG
                
                if accessory.aso_type != valid_aso_type:
                    return
            
            acs_list = self._m1_sprite0x2dchart__get_acs(acs_type)
            temp_space = {
                "acs_list": acs_list,
            }
            
            if acs_list is not None and accessory not in acs_list:
                
                
                store.mas_sprites.acs_wear_mux_pre_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )
                
                
                if temp_space.get("abort", False):
                    return
                
                
                if accessory.mux_type is not None:
                    self.remove_acs_mux(accessory.mux_type)
                
                
                store.mas_sprites.acs_wear_mux_pst_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )
                
                
                mas_insertSort(acs_list, accessory, MASAccessory.get_priority)
                
                
                self.acs_list_map[accessory.name] = acs_type
                
                if accessory.name in mas_sprites.lean_acs_blacklist:
                    self.lean_acs_blacklist.append(accessory.name)
                
                
                store.mas_sprites.acs_wear_entry_pre_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )
                
                
                accessory.entry(self)
                
                
                store.mas_sprites.acs_wear_entry_pst_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )
        
        def wear_acs_pre(self, acs):
            """DEPRECATED
            Wears the given accessory in the pre body accessory mode

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.PRE_ACS)
        
        
        def wear_acs_bbh(self, acs):
            """DEPRECATED
            Wears the given accessory in the post back hair accessory loc

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.BBH_ACS)
        
        
        def wear_acs_bfh(self, acs):
            """DEPRECATED
            Wears the given accessory in the pre front hair accesory log

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.BFH_ACS)
        
        
        def wear_acs_afh(self, acs):
            """DEPRECATED
            Wears the given accessory in the between front hair and arms
            acs log

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.AFH_ACS)
        
        
        def wear_acs_mid(self, acs):
            """DEPRECATED
            Wears the given accessory in the mid body acessory mode

            IN:
                acs - acessory to wear
            """
            self.wear_acs_in(acs, self.MID_ACS)
        
        
        def wear_acs_pst(self, acs):
            """DEPRECATED
            Wears the given accessory in the post body accessory mode

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.PST_ACS)


































    class MASTableChair(object):
        """
        Representation of an available table + chair combo.

        PROPERTIES:
            has_shadow - True if this table has a shadow
            table - table tag associated with this table chair combo
                This will be used in bulding the table sprite string
            chair - chair tag associated with tihs table chair combo
                This will be used in building the chair sprite string
            hl_map - MASHighlightMap associated with this table chair
                keys:
                    t - table
                    ts - table shadow - Used instead of table whenever shadow
                        is applied.
                    c - chair
        """
        from store.mas_sprites import TC_GEN, PREFIX_TABLE, SHADOW_SUFFIX, NIGHT_SUFFIX
        _m1_sprite0x2dchart__MHM_KEYS = ("t", "ts", "c")
        
        def __init__(self, table, chair, hl_data=None):
            """
            constructor

            IN:
                table - table tag to use 
                chair - chair tag to use
                hl_data - highlight mapping data. format:
                    [0] - default highilght to use. Pass in None to not set
                        a default.
                    [1] - highlight mapping to use. Format:
                        key: "t" for table, "c" for chair
                        value: MASFilterMap object, or None if no highlight
                    pass in None if no highlights shoudl be used at all
            """
            self.table = table
            self.chair = chair
            self.has_shadow = False
            self.prepare()
            
            if hl_data is None:
                self.hl_map = None
            else:
                self.hl_map = MASHighlightMap.create_from_mapping(
                    self._m1_sprite0x2dchart__MHM_KEYS,
                    hl_data[0],
                    hl_data[1]
                )
        
        def __repr__(self):
            return "<TableChair: (table: {0}, chair: {1})>".format(
                self.table,
                self.chair
            )

        def prepare(self):
            """
            Prepares this table chair combo by checking for shadow.
            """
            self.has_shadow = (
                renpy.loadable(self.TC_GEN.format(
                    self.PREFIX_TABLE,
                    self.table,
                    self.SHADOW_SUFFIX,
                    ""
                ))
            )
        
        def setTable(self, new_table):
            """
            sets the table tag and checks shadow

            IN:
                new_table - the new table tag to set
                    if an invalid string or NOne is passed in, we reset to 
                    default
            """
            if new_table:
                self.table = new_table
            else:
                self.table = "def"
            
            self.prepare()


    class MASArm(object):
        """
        Representation of an "Arm" 

        Each Arm consists of of a layered combination:
        NOTE: we re using spaced layers so we can insert more if needed.
        0 - bottom layer. after body-0 but before table. Primary bottom layer.
        5 - middle layer. after table but before body-1.
        10 - top layer. after body-1.

        PROPERTIES:
            tag - the tag string of this arm
            layer_map - mapping of layer exiestence to image code
                key: layer code
                value: True if exists, False if not
            hl_map - MASHighlightMap with layer code keys
        """
        
        LAYER_BOT = "0"
        LAYER_MID = "5"
        LAYER_MID_2 = "5^10"
        LAYER_TOP = "10"
        
        _m1_sprite0x2dchart__MPA_KEYS = (LAYER_BOT, LAYER_MID, LAYER_MID_2, LAYER_TOP)
        
        def __init__(self, tag, layer_map, hl_data=None):
            """
            Constructor

            IN:
                tag - tag string for this arm
                layer_map - layer map to use
                    key: image layer code
                    value: True if exists, False if not
                hl_data - highlght map data. tuple of the following formaT:
                    [0] - default MASFilterMap to use. Pass in None to 
                        not set a default highlight
                    [1] - highlight mapping to use. Format:
                        key: image layer code
                        value: MASFilterMap object, or None if no highlight
                    pass in None if no highlights should be used at all
            """
            self.tag = tag
            self.clean_map(layer_map)
            self.layer_map = layer_map
            
            if hl_data is not None:
                self.hl_map = MASHighlightMap.create_from_mapping(
                    self._m1_sprite0x2dchart__MPA_KEYS,
                    hl_data[0],
                    hl_data[1]
                )
            else:
                self.hl_map = None
        
        def _m1_sprite0x2dchart__build_loadstrs_hl(self, prefix, layer_code):
            """
            Builds load strings for a hlight from a given map

            IN:
                prefix - prefix to apply
                layer_code - layer code to generate loadstrings for

            RETURNS: list of lists of strings representing image path for all
                highlights for a layer code
            """
            if self.hl_map is None:
                return []
            
            mfm = self.hl_map.get(layer_code)
            if mfm is None:
                return []
            
            
            return [
                prefix + [
                    store.mas_sprites.HLITE_SUFFIX,
                    hlc,
                    store.mas_sprites.FILE_EXT
                ]
                for hlc in mfm.unique_values()
            ]
        
        @classmethod
        def _fromJSON(cls, json_obj, msg_log, ind_lvl, build_class):
            """
            Builds a MASArm object based on the given JSON format of it

            IN:
                json_obj - JSON object to parse
                ind_lvl - indent level
                build_class - actual MASArm derivative to build

            OUT:
                msg_log - list to save messages to

            RETURNS: MASArm instance built with the JSON, or None if failed
            """
            params = {}
            
            
            
            if not store.mas_sprites_json._validate_params(
                    json_obj,
                    params,
                    {
                        "tag": (str, store.mas_sprites_json._verify_str),
                        "layers": (str, store.mas_sprites_json._verify_str),
                    },
                    True,
                    msg_log,
                    ind_lvl
            ):
                return None
            
            
            layer_map = {}
            for layer in params.pop("layers").split("^"):
                if layer in cls._m1_sprite0x2dchart__MPA_KEYS:
                    layer_map[layer] = True
                
                else:
                    
                    
                    msg_log.append((
                        store.mas_sprites_json.MSG_WARN_T,
                        ind_lvl,
                        store.mas_sprites_json.MA_INVALID_LAYER.format(layer)
                    ))
            
            
            
            if len(layer_map) == 0:
                msg_log.append((
                    store.mas_sprites_json.MSG_ERR_T,
                    ind_lvl,
                    store.mas_sprites_json.MA_NO_LAYERS
                ))
                return None
            
            
            params["layer_map"] = layer_map
            
            
            if store.mas_sprites_json.HLITE in json_obj:
                
                
                vhl_data = {}
                
                if store.mas_sprites_json._validate_highlight(
                        json_obj,
                        vhl_data,
                        msg_log,
                        ind_lvl,
                        layer_map.keys()
                ):
                    
                    hl_data = vhl_data.get("hl_data", None)
                    if hl_data is not None:
                        params["hl_data"] = hl_data
                
                else:
                    
                    return None
            
            
            for extra_prop in json_obj:
                msg_log.append((
                    store.mas_sprites_json.MSG_WARN_T,
                    ind_lvl,
                    store.mas_sprites_json.EXTRA_PROP.format(extra_prop)
                ))
            
            
            return build_class(**params)
        
        def build_loadstrs(self, prefix):
            """
            Builds loadstrs for this arm

            IN:
                prefix - prefix to apply to the loadstrs
                    should be list of strings

            RETURNS: list of lists of strings representing the load strings 
                for this arm, + highlights 
            """
            if not self.tag:
                return []
            
            loadstrs = []
            
            
            for layer_code in self._m1_sprite0x2dchart__MPA_KEYS:
                
                
                
                if self.layer_map.get(layer_code, False):
                    
                    
                    new_img = prefix + [
                        self.tag,
                        store.mas_sprites.ART_DLM,
                        str(layer_code)
                    ]
                    
                    
                    loadstrs.append(new_img + [store.mas_sprites.FILE_EXT])
                    
                    
                    loadstrs.extend(self._m1_sprite0x2dchart__build_loadstrs_hl(
                        new_img,
                        layer_code
                    ))
            
            return loadstrs
        
        def clean_map(self, mapping):
            """
            cleans the given map, ensuring it contains only valid layer
            keys. No errors are logged.

            IN:
                mapping - mapping to clean
            """
            for map_key in mapping.keys():
                if map_key not in self._m1_sprite0x2dchart__MPA_KEYS:
                    mapping.pop(map_key)
        
        def get(self, layer_code, prefix=[]):
            """
            Generates tag name + suffixes to use for
            a given layer code. A tag name is a tuple of strings
            that can be joined to build the full tag name,
            Tag Names do NOT include file extensions

            IN:
                layer_code - layer code to fetch tag names for
                prefix - prefix to apply to the tag string if desired
                    (Default: [])

            RETURNS: list consisting of the tag strings and
                appropriate suffixes
            """
            if not self.tag:
                return []
            
            
            if not self.layer_map.get(layer_code, False):
                return []
            
            
            return prefix + [
                self.tag,
                store.mas_sprites.ART_DLM,
                str(layer_code)
            ]
        
        def gethlc(self, layer_code, flt, defval=None):
            """
            Gets highlight code.

            IN:
                layer_code - layer to get highlight for
                flt - filter to get highilght for
                defval - default value to return
                    (Default: None)

            RETURNS: highlight code, or None if no highligiht
            """
            return MASHighlightMap.o_fltget(
                self.hl_map,
                layer_code,
                flt,
                defval
            )
        
        def hl_keys(self):
            """
            Returns hl keys for a MASArm

            RETURNS: tuple of hl keys
            """
            return self._m1_sprite0x2dchart__MPA_KEYS
        
        @classmethod
        def hl_keys_c(cls):
            """
            Class method version of hl_keys

            RETURNS: tuple of hl keys
            """
            return cls._m1_sprite0x2dchart__MPA_KEYS


    class MASArmBoth(MASArm):
        """
        Representation of an "arm" that actually covers both arms

        This currently has no additional behavior.
        It's primary use is to act as a type of MASArm

        PROPERTIES:
            see MASArm
        """
        pass


    class MASArmLeft(MASArm):
        """
        Representation of a left arm.

        Overrides prefix-based functions

        PROPERTIES:
            see MASArm
        """
        
        def build_loadstrs(self, prefix):
            """
            Generates loadstrs for this arm

            IN:
                prefix - prefix to apply to the loadstrs
                    list of strings

            RETURNS: list of lists of strings representing the loadstrs
            """
            return super(MASArmLeft, self).build_loadstrs(
                prefix + [store.mas_sprites.PREFIX_ARMS_LEFT]
            )
        
        def get(self, layer_code):
            """
            See MASArm.get

            This adds left- prefix to result
            """
            return super(MASArmLeft, self).get(
                layer_code,
                prefix=["left", store.mas_sprites.ART_DLM]
            )


    class MASArmRight(MASArm):
        """
        Representation of a right arm.

        Overrides prefix-based functions

        PROPERTIES:
            see MASArm
        """
        
        def build_loadstrs(self, prefix):
            """
            Generates loadstrs for this arm

            IN:
                prefix - prefix to apply to the loadstrs
                    list of strings

            RETURNS: list of lists of strings representing the loadstrs
            """
            return super(MASArmRight, self).build_loadstrs(
                prefix + [store.mas_sprites.PREFIX_ARMS_RIGHT]
            )
        
        def get(self, layer_code):
            """
            See MASArm.get

            This adds right- prefix to result
            """
            return super(MASArmRight, self).get(
                layer_code,
                prefix=["right", store.mas_sprites.ART_DLM]
            )


    class MASPoseArms(object):
        """
        Collection of MASArm objects. An Arm object is the representation of
        an arm sprite.

        PROPERTIES:
            arms - dict mapping arms to MASArm objects
                keys: number from NUM_ARMS
                value: MASArm object. None means no arm for this arm

        """
        import store.mas_sprites_json as msj
        
        def __init__(self, arm_data, def_base=True):
            """
            Constructor

            IN:
                arm_data - see arms property
                def_base - True will use base arms for all missing data
                    False will not
                    (Default: True)
            """
            
            if not store.mas_ev_data_ver._verify_dict(
                    arm_data,
                    allow_none=False
            ):
                raise Exception("arm data required for MASPoseArms")
            
            
            self._clean_arms(arm_data, def_base)
            self.arms = arm_data
        
        def _clean_arms(self, arm_data, def_base):
            """
            Cleans arm data given
            Will Noneify invalid-typed data

            IN:
                arm_data - arm data to clean
                def_base - True will use base arms for all missing data
                    False will not

            OUT:
                arm_data - cleaned arm data
            """
            
            for arm_key in arm_data.keys():
                
                
                if arm_key in store.mas_sprites.NUM_ARMS:
                    
                    if not isinstance(arm_data[arm_key], MASArm):
                        store.mas_utils.writelog(
                            "Invalid arm data at '{0}'\n".format(arm_key)
                        )
                        arm_data[arm_key] = None
                
                else:
                    
                    arm_data.pop(arm_key)
            
            
            
            if def_base:
                for arm_key in store.mas_sprites.NUM_ARMS:
                    if arm_key not in arm_data:
                        arm_data[arm_key] = store.mas_sprites.use_bma(arm_key)
        
        
        
        
        def build_loadstrs(self, prefix):
            """
            Generates loadstrs for this PoseArms object

            IN:
                prefix - list of strings to apply as prefix

            RETURNS: list of lists of strings representing the load strs
            """
            loadstrs = []
            
            
            for arm_key in self.arms:
                
                arm = self.arms[arm_key]
                
                if arm is not None:
                    
                    
                    lean = store.mas_sprites.ARMS_LEAN.get(arm_key, None)
                    if lean is None:
                        
                        arm_prefix = prefix + [store.mas_sprites.PREFIX_ARMS]
                    else:
                        
                        arm_prefix = prefix + [
                            store.mas_sprites.PREFIX_ARMS_LEAN,
                            lean,
                            store.mas_sprites.ART_DLM
                        ]
                    
                    
                    loadstrs.extend(arm.build_loadstrs(arm_prefix))
            
            return loadstrs
        
        @staticmethod
        def fromJSON(json_obj, msg_log, ind_lvl):
            """
            Builds a MASPoseArms object given a JSON format of it

            IN:
                json_obj - json object to parse
                ind_lvl - indent level

            OUT:
                msg_log - list to save messages to

            RETURNS: MASPoseArms object built using the JSON, None if no
                data to be made, False if error occured
            """
            
            
            arm_data = {}
            
            
            isbad = False
            for arm_id, arm_sid in store.mas_sprites.NUM_ARMS.iteritems():
                if arm_sid in json_obj:
                    arm_obj = json_obj.pop(arm_sid)
                    
                    
                    if arm_obj is None:
                        
                        arm_data[arm_id] = None
                    
                    elif not store.mas_sprites_json._verify_dict(arm_obj):
                        
                        msg_log.append((
                            store.mas_sprites_json.MSG_ERR_T,
                            ind_lvl,
                            store.mas_sprites_json.MPA_BAD_TYPE.format(
                                arm_sid,
                                dict,
                                type(arm_obj)
                            )
                        ))
                        isbad = True
                    
                    else:
                        
                        
                        
                        msg_log.append((
                            store.mas_sprites_json.MSG_INFO_T,
                            ind_lvl,
                            store.mas_sprites_json.MA_LOADING.format(arm_sid)
                        ))
                        
                        
                        arm = MASArm._fromJSON(
                            arm_obj,
                            msg_log,
                            ind_lvl + 1,
                            store.mas_sprites.NUM_MARMS[arm_id]
                        )
                        
                        
                        if arm is None:
                            
                            isbad = True
                        
                        else:
                            
                            msg_log.append((
                                store.mas_sprites_json.MSG_INFO_T,
                                ind_lvl,
                                store.mas_sprites_json.MA_SUCCESS.format(
                                    arm_sid
                                )
                            ))
                            
                            
                            arm_data[arm_id] = arm
            
            
            for extra_prop in json_obj:
                msg_log.append((
                    store.mas_sprites_json.MSG_WARN_T,
                    ind_lvl,
                    store.mas_sprites_json.EXTRA_PROP.format(extra_prop)
                ))
            
            
            if isbad:
                return False
            
            
            
            
            
            
            
            
            return MASPoseArms(arm_data, def_base=False)
        
        def get(self, arm_key):
            """
            Gets the arm data associated with the given arm key

            IN:
                arm_key - key of the arm data to get

            RETURNS: MASArm object requested, or NOne if not available for the
                arm key
            """
            return self.arms.get(arm_key, None)
        
        def getflp(self, leanpose):
            """
            Retrieves arms assocaited with the given leanpose

            IN:
                leanpose - the leanpose to get arms for

            RETURNS: Tuple of arms associated with the leanpose. None may be
                returned if no arms for the leanpose. The number of arms is 
                not a guarantee.
            """
            arm_data = []
            for arm_key in store.mas_sprites.base_mpm.get(leanpose, []):
                arm = self.get(arm_key)
                if arm is not None:
                    arm_data.append(arm)
            
            if len(arm_data) > 0:
                return tuple(arm_data)
            
            
            return None


    class MASPoseMap(renpy.store.object):
        """
        The Posemap helps connect pose names to images

        NOTE: the internal maps are public, but should be converted to
            private.

        This is done via a dict containing pose names and where they
        map to.

        There is also a seperate dict to handle lean variants
        """
        from store.mas_sprites import POSES, L_POSES
        import store.mas_sprites_json as msj
        
        
        
        PARAM_NAMES = (
            "p1", 
            "p2", 
            "p3", 
            "p4", 

            "p6", 
            "p7", 
        )
        
        
        L_PARAM_NAMES = (
            "p5", 
        )
        
        P_PARAM_NAMES = tuple(list(PARAM_NAMES) + list(L_PARAM_NAMES))
        
        
        CONS_PARAM_NAMES = (
            "default",
            "l_default",

        ) + P_PARAM_NAMES
        
        MPM_TYPE_ED = 0
        
        
        
        
        MPM_TYPE_FB = 1
        
        
        
        
        MPM_TYPE_AS = 2
        
        
        
        
        MPM_TYPE_PA = 3
        
        
        
        MPM_TYPE_IC = 4
        
        
        
        
        MPM_TYPES = (
            MPM_TYPE_ED,
            MPM_TYPE_FB,
            MPM_TYPE_AS,
            MPM_TYPE_PA,
            MPM_TYPE_IC
        )
        
        def __init__(self,
                
                
                mpm_type=0,
                default=None,
                l_default=None,
                use_reg_for_l=False,
                **pargs
            ):
            """
            Constructor

            If None is passed in for any var, we assume that no image should
            be shown for that pose

            IN:
                mpm_type - MASPoseMap type of this posemap
                    Default is 0 (enable/disble mode)
                default - default pose id to use for poses that are not
                    specified (aka are None).
                l_default - default pose id to use for lean poses that are not
                    specified (aka are None).
                use_reg_for_l - if True and default is not None and l_default
                    is None, then we use the default instead of l_default
                    when rendering for lean poses
                **pargs - the remaining name value pairs are checked in param
                    names. Each apply to specific pose. 
                    (See MASPoseArms.PARAM_NAMES and L_PARAM_NAMES)
            """
            
            poses, lposes = self._m1_sprite0x2dchart__listify(pargs)
            
            self.map = {}
            for index in range(len(self.POSES)):
                self.map[self.POSES[index]] = poses[index]
            
            self.l_map = {}
            for index in range(len(self.L_POSES)):
                self.l_map[self.L_POSES[index]] = lposes[index]
            
            
            self._m1_sprite0x2dchart__default = default
            self._m1_sprite0x2dchart__l_default = l_default
            self.use_reg_for_l = use_reg_for_l
            self._m1_sprite0x2dchart__set_defaults()
            
            
            self._m1_sprite0x2dchart__all_map = {}
            self._m1_sprite0x2dchart__sync_all()
            
            self._mpm_type = mpm_type
        
        def _m1_sprite0x2dchart__associate(self, pargs):
            """
            Associates the given pargs (retrieved from **pargs) and with
            index values related to POSES and L_POSES

            IN:
                pargs - dict retrieved from a **pargs var

            RETURNS: tuple of the following format:
                [0] - POSES associations. List of tuples:
                    [0] - index to map
                    [1] - parg value to map to
                [1] - L_POSES associations. List of tuples:
                    [0] - index to map
                    [1] - parg value to map to
            """
            return (
                [
                    (index, pargs[self.PARAM_NAMES[index]])
                    for index in range(len(self.POSES))
                    if self.PARAM_NAMES[index] in pargs
                ],
                [
                    (index, pargs[self.L_PARAM_NAMES[index]])
                    for index in range(len(self.L_POSES))
                    if self.L_PARAM_NAMES[index] in pargs
                ]
            )
        
        def _m1_sprite0x2dchart__listify(self, pargs):
            """
            Takes the pargs and generates lists of them in the same order as
            POSES and L_POSES.

            If an item doesnt exist in pargs, None is used

            IN:
                pargs - dict retrieved from a **pargs var

            RETURNS: tuple of hte following format:
                [0] - list of pose values from pargs, in order of POSES
                [1] - list of lean values from pargs, in order of L_POSES
            """
            return (
                [ pargs.get(param, None) for param in self.PARAM_NAMES ],
                [ pargs.get(lparam, None) for lparam in self.L_PARAM_NAMES ],
            )
        
        def _m1_sprite0x2dchart__set_defaults(self):
            """
            Sets all pose defaults
            """
            self._m1_sprite0x2dchart__set_posedefs(self.map, self._m1_sprite0x2dchart__default)
            if (
                    self.use_reg_for_l
                    and self._m1_sprite0x2dchart__l_default is None
                    and self._m1_sprite0x2dchart__default is not None
            ):
                self._m1_sprite0x2dchart__set_posedefs(self.l_map, self._m1_sprite0x2dchart__default)
            else:
                self._m1_sprite0x2dchart__set_posedefs(self.l_map, self._m1_sprite0x2dchart__l_default)
        
        def _m1_sprite0x2dchart__set_posedefs(self, pose_dict, _def):
            """
            Sets pose defaults

            IN:
                pose_dict - dict of poses
                _def - default to use here
            """
            for k in pose_dict:
                if pose_dict[k] is None:
                    pose_dict[k] = _def
        
        def _m1_sprite0x2dchart__sync_all(self):
            """
            Syncs internal all map with the internal maps
            """
            self._m1_sprite0x2dchart__all_map.update(self.map)
            self._m1_sprite0x2dchart__all_map.update(self.l_map)
        
        def _modify(self, **pargs):
            """
            Modifes poses based on given pargs.
            NOTE: this can damage the sprite system if done incorrectly. 

            IN:
                **pargs - param name-value pairs. See MASPoseArms.PARAM_NAMES
                    and MASPoseArms.L_PARAM_NAMES
            """
            pose_changes, lpose_changes = self._m1_sprite0x2dchart__associate(pargs)
            for index, new_value in pose_changes:
                self.map[self.POSES[index]] = new_value
            
            for index, new_value in lpose_changes:
                self.l_map[self.L_POSES[index]] = new_value
            
            
            self._m1_sprite0x2dchart__set_defaults()
            
            
            self._m1_sprite0x2dchart__sync_all()
        
        def _transform(self, func):
            """
            Applies the given function to transform value in each pose
            NOTE: this can damage the sprite system if done incorrectly

            IN:
                func - function to call for each pose. The current vlaue for
                    each pose is passed in. The return value of this function
                    is set to the pose.
            """
            for pose in self.map:
                self.map[pose] = func(self.map[pose])
            for lpose in self.l_map:
                self.l_map[lpose] = func(self.l_map[lpose])
            
            
            self._m1_sprite0x2dchart__set_defaults()
            
            
            self._m1_sprite0x2dchart__sync_all()
        
        @classmethod
        def _verify_mpm_item(cls,
                mpm_data,
                msg_log,
                ind_lvl,
                mpm_type,
                prop_name,
                prop_val
        ):
            """
            Verifies data for an mpm item based on type

            IN:
                ind_lvl - indent lvl
                mpm_type - mpm type to check values for
                prop_name - name of the item to check
                prop_val - value of the item to check

            OUT:
                mpm_data - dict to save data to
                msg_log - list to add messages to

            RETURNS: True if successful verification, False if not
            """
            if mpm_type == cls.MPM_TYPE_IC:
                
                
                if cls.msj._verify_str(prop_val):
                    mpm_data[prop_name] = prop_val
                
                else:
                    msg_log.append((
                        cls.msj.MSG_ERR_T,
                        ind_lvl,
                        cls.msj.MPM_BAD_POSE_TYPE.format(
                            prop_name,
                            str,
                            type(prop_val)
                        )
                    ))
                    return False
            
            if mpm_type == cls.MPM_TYPE_AS:
                
                
                if MASSplitAccessory.verify_arm_split_val(prop_val):
                    mpm_data[prop_name] = prop_val
                
                else:
                    msg_log.append((
                        cls.msj.MSG_ERR_T,
                        ind_lvl,
                        cls.msj.MPM_AS_BAD_TYPE.format(
                            prop_name,
                            str(MASSplitAccessory.hl_keys()),
                            prop_val
                        )
                    ))
                    return False
            
            if mpm_type == cls.MPM_TYPE_ED:
                
                
                if cls.msj._verify_bool(prop_val):
                    mpm_data[prop_name] = prop_val
                
                else:
                    msg_log.append((
                        cls.msj.MSG_ERR_T,
                        ind_lvl,
                        cls.msj.MPM_BAD_POSE_TYPE.format(
                            prop_name,
                            bool,
                            type(prop_val)
                        )
                    ))
                    return False
            
            if mpm_type == cls.MPM_TYPE_FB:
                
                
                if cls.msj._verify_pose(prop_val, allow_none=False):
                    mpm_data[prop_name] = prop_val
                
                else:
                    msg_log.append((
                        cls.msj.MSG_ERR_T,
                        ind_lvl,
                        cls.msj.MPM_BAD_POSE.format(
                            prop_name,
                            prop_val
                        )
                    ))
                    return False
            
            
            return True
        
        @classmethod
        def fromJSON(cls, json_obj, msg_log, ind_lvl, valid_types=None):
            """
            Builds a MASPoseMap given a JSON format of it

            IN:
                json_obj - json object to parse
                ind_lvl - indent lvl
                valid_types - tuple/list of MPM types we should consider valid.
                    NOTE: this should be used by the caller to ensure that
                    the MPM being loaded is the correct one.
                    If not passed, then we don't check for valid types

            OUT:
                msg_log - list to add messages to

            RETURNS: MASPoseMap object built using the JSON, or None if failed
            """
            mpm_prop = "mpm_type"
            urfl_prop = "use_reg_for_l"
            mpm_data = {}
            
            
            if mpm_prop not in json_obj:
                msg_log.append((
                    cls.msj.MSG_ERR_T,
                    ind_lvl,
                    cls.msj.REQ_MISS.format(mpm_prop)
                ))
                return None
            
            mpm_type = json_obj.pop(mpm_prop)
            
            if not cls.msj._verify_int(mpm_type, allow_none=False):
                msg_log.append((
                    cls.msj.MSG_ERR_T,
                    ind_lvl,
                    cls.msj.BAD_TYPE.format(mpm_prop, int, type(mpm_type))
                ))
                return None
            
            if mpm_type not in cls.MPM_TYPES:
                msg_log.append((
                    cls.msj.MSG_ERR_T,
                    ind_lvl,
                    cls.msj.MPM_BAD_TYPE.format(mpm_type)
                ))
                return None
            
            if valid_types is not None and mpm_type not in valid_types:
                msg_log.append((
                    cls.msj.MSG_ERR_T,
                    ind_lvl,
                    cls.msj.MPM_TYPE_MISS.format(valid_types, mpm_type)
                ))
                return None
            
            mpm_data[mpm_prop] = mpm_type
            
            
            if urfl_prop in json_obj:
                use_reg_for_l = json_obj.pop(urfl_prop)
                if not cls.msj._verify_bool(use_reg_for_l, allow_none=False):
                    msg_log.append((
                        cls.msj.MSG_ERR_T,
                        ind_lvl,
                        cls.msj.BAD_TYPE.format(
                            urfl_prop,
                            str, 
                            type(use_reg_for_l)
                        )
                    ))
                    return None
                
                mpm_data[urfl_prop] = use_reg_for_l
            
            else:
                use_reg_for_l = None
            
            
            isbad = False
            for prop_name in json_obj.keys():
                prop_val = json_obj.pop(prop_name)
                if prop_name in cls.CONS_PARAM_NAMES:
                    if not cls._verify_mpm_item(
                            mpm_data,
                            msg_log,
                            ind_lvl,
                            mpm_type,
                            prop_name,
                            prop_val
                    ):
                        isbad = True
                
                else:
                    
                    msg_log.append((
                        cls.msj.MSG_WARN_T,
                        ind_lvl,
                        cls.msj.EXTRA_PROP.format(prop_name)
                    ))
            
            
            if isbad:
                return None
            
            
            _param_urfl = mpm_data.get("use_reg_for_l", False)
            if "default" not in mpm_data:
                msg_log.append((
                    cls.msj.MSG_WARN_T,
                    ind_lvl,
                    cls.msj.MPM_DEF
                ))
            
            if "l_default" not in mpm_data and not _param_urfl:
                
                
                
                msg_log.append((
                    cls.msj.MSG_WARN_T,
                    ind_lvl,
                    cls.msj.MPM_DEF_L
                ))
            
            return MASPoseMap(**mpm_data)
        
        def get(self, pose, defval):
            """
            Get passed to the internal pose map
            only because its common to call get on this object. 

            IN:
                pose - pose to get from pose map
                defval - default value to return if pose not found

            RETURNS:
                value of pose in internal dict, or defval if not found
            """
            return self._m1_sprite0x2dchart__all_map.get(pose, defval)
        
        def is_fallback(self):
            """
            Checks if this posemap is a fallback one via type.

            RETURNS: True if this posemap is a fallback one, False if not
            """
            return self._mpm_type == self.MPM_TYPE_FB
        
        def unique_values(self):
            """
            Gets all unique non-None values in this MASPoseMap.
            NOTE: because MPM's may not include hashable values, this is 
            try/excepted to handle those cases. If something is non-hashable,
            we always return all values.

            RETURNS: list of unique non-None values in this MASPoseMap
            """
            try:
                values = []
                for value in self._m1_sprite0x2dchart__all_map.itervalues():
                    if value is not None and value not in values:
                        values.append(value)
                
                return values
            except:
                return self.values()
        
        def values(self):
            """
            Gets all non-None values in this MASPoseMap.

            RETURNS: list of all non-None values in this MASPoseMap
            """
            return [
                value
                for value in self._m1_sprite0x2dchart__all_map.itervalues()
                if value is not None
            ]
        
        @staticmethod
        def lp2pn(leanpose):
            """
            Converts a leanpose to a PARAM NAME

            IN:
                leanpose - leanpose to convert

            RETURNS: param name associated with leanpose, or "" if not valid
            """
            if leanpose in MASPoseMap.POSES:
                return MASPoseMap.PARAM_NAMES[MASPoseMap.POSES.index(leanpose)]
            
            if leanpose in MASPoseMap.L_POSES:
                return MASPoseMap.L_PARAM_NAMES[MASPoseMap.L_POSES.index(
                    leanpose
                )]
            
            return ""
        
        @staticmethod
        def pn2lp(name):
            """
            Converts a PARAM NAME to a leanpose

            IN:
                name - name of the param to convert

            RETURNS: leanpose associated with param name, or "" if not valid
            """
            if name in MASPoseMap.PARAM_NAMES:
                return MASPoseMap.POSES[MASPoseMap.PARAM_NAMES.index(name)]
            
            if name in MASPoseMap.L_PARAM_NAMES:
                return MASPoseMap.L_POSES[MASPoseMap.L_PARAM_NAMES.index(name)]
            
            return ""


    class MASSpriteBase(renpy.store.object):
        """
        Base class for MAS sprite objects

        PROPERTIES:
            name - name of the item
            img_sit - filename of the sitting version of the item
            img_stand - filename of the standing version of the item
            pose_map - MASPoseMap object that contains pose mappings
            stay_on_start - determines if the item stays on startup
            entry_pp - programmign point to call when wearing this sprite
                the MASMonika object that is being changed is fed into this
                function
                NOTE: this is called after the item is added to MASMonika
            exit_pp - programming point to call when taking off this sprite
                the MASMonika object that is being changed is fed into this
                function
                NOTE: this is called before the item is removed from MASMonika
            is_custom - True if this is a custom object. False if not.
                NOTE: this must be set AFTER object creation
            hl_map - MASHighlightMap. Actual implementation may vary by extended
                classes
        """
        import store.mas_sprites_json as msj
        
        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                stay_on_start=False,
                entry_pp=None,
                exit_pp=None,
                ex_props=None,
                full_hl_data=None
            ):
            """
            MASSpriteBase constructor

            IN:
                name - name of this item
                img_sit - filename of the sitting image
                pose_map - MASPoseMAp object that contains pose mappings
                img_stand - filename of the standing image
                    If this is not passed in, this is considered blacklisted
                    from standing sprites.
                    (Default: "")
                stay_on_start - True means the item should reappear on startup
                    False means the item should always drop when restarting.
                    (Default: False)
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: None)
                full_hl_data - tuple of the following format:
                    [0] - keys to use for MASHighlightMap
                    [1] - default value for MASHighlightMap
                        if None, no default highlights
                    [2] - mapping dict of the following format:
                        key: key in [0]
                        value: value to use for key
                            if None, no highlight for this key
                        if None, no mapped highlights
                    if None, no highlights at all
                    (Default: None)
            """
            self._m1_sprite0x2dchart__sp_type = -1
            self.name = name
            self.img_sit = img_sit
            self.img_stand = img_stand
            self.stay_on_start = stay_on_start
            self.pose_map = pose_map
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp
            self.is_custom = False
            
            if type(pose_map) != MASPoseMap:
                raise Exception("PoseMap is REQUIRED")
            
            
            if ex_props is None:
                self.ex_props = {}
            else:
                self.ex_props = ex_props
            
            
            self._m1_sprite0x2dchart__setup_hl_map(full_hl_data)
        
        def __eq__(self, other):
            """
            Equality override
            """
            if isinstance(other, MASSpriteBase):
                return self.name == other.name
            
            return NotImplemented
        
        def __ne__(self, other):
            """
            Not equal override
            """
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result
        
        def _m1_sprite0x2dchart__setup_hl_map(self, hl_data):
            """
            Sets up the highlight map

            IN:
                hl_data - See constructor for description
            """
            if hl_data is None:
                self.hl_map = None
                return
            
            
            hl_keys, hl_def, hl_mapping = hl_data
            if hl_def is None and hl_mapping is None:
                self.hl_map = None
                return
            
            
            self.hl_map = MASHighlightMap.create_from_mapping(
                hl_keys,
                hl_def,
                hl_mapping
            )
        
        def addprop(self, prop):
            """
            Adds the given prop to the ex_props list

            IN:
                prop - prop to add
            """
            self.ex_props[prop] = True
        
        def build_loadstrs(self, prefix):
            """
            Build list of strings representing each image that may be used
            in this sprite.

            NOTE: this should be implemented by the extending classes

            IN:
                prefix - prefix to apply to each image. should be list of
                    strings
                    (DEfault: "")
            
            RETURNS: list of lists of strings represented in this image.
                use .join on each inner list to make the image
            """
            raise NotImplementedError
        
        def entry(self, _monika_chr, **kwargs):
            """
            Calls the entry programming point if it exists

            IN:
                _monika_chr - the MASMonika object being changed
                **kwargs - other keyword args to pass
            """
            if self.entry_pp is not None:
                self.entry_pp(_monika_chr, **kwargs)
        
        def exit(self, _monika_chr, **kwargs):
            """
            Calls the exit programming point if it exists

            IN:
                _monika_chr - the MASMonika object being changed
                **kwargs - other keyword args to pass
            """
            if self.exit_pp is not None:
                self.exit_pp(_monika_chr, **kwargs)
        
        def gethlc(self, *args, **kwargs):
            """
            Gets highlight code

            NOTE: actual args and implementation should be handled by the
                extended classes

            RETURNS: highlight code, or defval if no highlight
            """
            raise NotImplementedError
        
        def getprop(self, prop, defval=None):
            """
            Gets the exprop

            IN:
                prop - prop to get
                defval - default value to return if prop not found
            """
            return self.ex_props.get(prop, defval)
        
        def gettype(self):
            """
            Gets the type of this sprite object

            RETURNS: type of this sprite object
            """
            return self._m1_sprite0x2dchart__sp_type
        
        def hasprogpoints(self):
            """
            RETURNS: true if this sprite object has at least 1 non-null prog
                point, False otherwise
            """
            return self.entry_pp is not None or self.exit_pp is not None
        
        def hasprop(self, prop):
            """
            Checks if this sprite object has the given prop

            IN:
                prop - prop in ex_props to look for

            RETURNS: True if this sprite object has the ex_prop, False if not
            """
            return prop in self.ex_props
        
        def hl_keys(self):
            """
            Gets keys used for the MASHighlightMap

            RETURNS: keys used in the primary level of this MASHighlightMap.
            An empty list is returned if no hl map or no keys
            """
            if self.hl_map is None:
                return []
            
            return self.hl_map.keys()
        
        def rmprop(self, prop):
            """
            Removes the prop from this sprite's ex_props, if it exists

            IN:
                prop - prop to remove

            RETURNS: True if the prop was found and removed, False otherwise
            """
            if prop in self.ex_props:
                self.ex_props.pop(prop)
                return True
            
            return False
        
        @staticmethod
        def sortkey(sprite_base):
            """
            Returns the sorting key of the given MASSpriteBase object
            """
            if isinstance(sprite_base, MASSpriteBase):
                return sprite_base.name
            
            return ""

    class MASSpriteFallbackBase(MASSpriteBase):
        """
        MAS sprites that can use pose maps as fallback maps.

        PROPERTIES:
            None

        SEE MASSpriteBase for inherited properties
        """
        
        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                stay_on_start=False,
                fallback=False,
                entry_pp=None,
                exit_pp=None,
                ex_props=None,
                full_hl_data=None
            ):
            """
            MASSpriteFallbackBase constructor

            IN:
                name - name of this item
                img_sit - filename of the sitting image for this item
                pose_map - MASPoseMap object that contains pose mappings or
                    fallback mappings
                img_stand - filename of the stnading image
                    If this is not passed in, this is considered blacklisted
                    from standing sprites.
                    (Default: "")
                stay_on_start - True means the item should reappear on startup
                    False means the item should always drop when restarting
                    (Default: False)
                fallback - Unused
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: None)
                hl_data - tuple of the following format:
                    [0] - keys to use for MASHighlightMap
                    [1] - default value for MASHighlightMap
                        if None, no default highlights
                    [2] - mapping dict of the following format:
                        key: key in [0]
                        value: value to use for key
                            if None, no highlight for this key
                        if None, no mapped highlights
                    if None, no highlights at all
                    (Default: None)
            """
            super(MASSpriteFallbackBase, self).__init__(
                name,
                img_sit,
                pose_map,
                img_stand,
                stay_on_start,
                entry_pp,
                exit_pp,
                ex_props,
                full_hl_data
            )
            self._m1_sprite0x2dchart__sp_type = -2
        
        def get_fallback(self, pose, lean):
            """
            Gets the fallback pose for a given pose or lean

            NOTE: the fallback variable is NOT checked

            Lean is checked first if its not None.

            IN:
                pose - pose to retrieve fallback for
                lean - lean to retrieve fallback for

            RETURNS:
                tuple fo thef ollowing format:
                [0]: arms type
                    - default for this is steepling
                [1]: lean type
                    - defualt for this is None
            """
            
            if lean is not None:
                
                fb_lean = self.pose_map.l_map.get(lean + "|" + pose, None)
                
                
                if fb_lean is None:
                    return ("steepling", None)
                
                
                if "|" in fb_lean:
                    return fb_lean.split("|")
                
                
                return (fb_lean, None)
            
            
            return (self.pose_map.map.get(pose, "steepling"), None)
        
        def get_leanpose(self, leanpose, defval=None):
            """
            Gets actual leanpose based on posemaps + fallback settings

            IN:
                leanpose - leanpose we are trying to get actual leanpose for
                defval - default value to return if no leanpose
                    (Default: None)
                    

            RETURNS: actual leanpose, or defval if not found
            """
            
            if self.pose_map.is_fallback():
                return self.pose_map.get(leanpose, defval)
            
            
            if self.pose_map.get(leanpose, False):
                return leanpose
            
            
            return defval



    class MASAccessoryBase(MASSpriteBase):
        """
        MASAccesory base objects

        PROPERTIES:
            priority - render priority. Lower is rendered first
            acs_type - an optional type to help organize acs
            mux_type - list of acs types that we shoudl treat
                as mutally exclusive with this type. Basically if this acs is
                worn, all acs with a type in this property are removed.
            dlg_desc - user friendly way to describe this accessory in dialogue
                Think "black bow" or "silver earrings"
            dlg_plur - True if the dlg_desc should be used in the plural 
                sense, like "these silver earrings", False if not, like:
                "this black bow"
            keep_on_desk - Set to True to keep the ACS on the desk when monika
                leaves, False if not
            hl_map - MASHighlightMap object where keys are defined by the given
                posemap. Value determined by extending classes.

        SEE MASSpriteBase for inherited properties
        """
        
        
        
        ASO_REG = 1
        
        
        ASO_SPLIT = 2
        
        
        ASO_TYPES = (
            ASO_REG,
            ASO_SPLIT
        )
        
        def __init__(self,
                aso_type,
                name,
                img_sit,
                pose_map,
                img_stand="",
                rec_layer=MASMonika.PST_ACS,
                priority=10,
                stay_on_start=False,
                entry_pp=None,
                exit_pp=None,
                acs_type=None,
                mux_type=None,
                ex_props=None,
                dlg_data=None,
                keep_on_desk=False,
                hl_data=None
            ):
            """
            MASAccessory constructor

            IN:
                aso_type - Accessory Sprite Object type
                name - name of this accessory
                img_sit - file name of the sitting image
                pose_map - MASPoseMap object that contains pose mappings
                img_stand - file name of the standing image
                    IF this is not passed in, we assume the standing version
                        has no accessory.
                    (Default: "")
                rec_layer - recommended layer to place this accessory
                    (Must be one the ACS types in MASMonika)
                    (Default: MASMonika.PST_ACS)
                priority - render priority. Lower is rendered first
                    (Default: 10)
                stay_on_start - True means the accessory is saved for next
                    startup. False means the accessory is dropped on next
                    startup.
                    (Default: False)
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                acs_type - type, for ease of organization of acs
                    This works with mux type to determine if an ACS can work
                    with another ACS.
                    (Default: None)
                mux_type - list of acs types that should be
                    mutually exclusive with this acs.
                    this works with acs_type to determine if this works with
                    other ACS.
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: None)
                dlg_data - tuple of the following format:
                    [0] - string to use for dlg_desc
                    [1] - boolean value for dlg_plur
                    (Default: None)
                keep_on_desk - determines if ACS should be shown if monika 
                    leaves
                    (Default: False)
                hl_data - tuple of the following format:
                    [0] - default value for MASHighlightMap
                        if None, no default highlight
                    [1] - dict-based highlight map data:
                        key: string. should match values used in pose_map
                        value: highlight data. Determined by extended classes. 
                            if None, then no highlight for the key
                        if None, then no mapped highlights
                    if None, no highlights at all
                    (Default: None)
            """
            super(MASAccessoryBase, self).__init__(
                name,
                img_sit,
                pose_map,
                img_stand,
                stay_on_start,
                entry_pp,
                exit_pp,
                ex_props,
                MASAccessoryBase._prepare_hl_data(hl_data, pose_map)
            )
            self.aso_type = aso_type
            self._m1_sprite0x2dchart__rec_layer = rec_layer
            self._m1_sprite0x2dchart__sp_type = store.mas_sprites_json.SP_ACS
            self.priority=priority
            self.acs_type = acs_type
            self.mux_type = mux_type
            self.keep_on_desk = keep_on_desk
            
            if dlg_data is not None and len(dlg_data) == 2:
                self.dlg_desc, self.dlg_plur = dlg_data
            else:
                self.dlg_desc = None
                self.dlg_plur = None
        
        @staticmethod
        def _prepare_hl_data(hl_data, pose_map):
            """
            Generates hl-ready data from ahldata

            IN:
                hl_data - ahl data. See constructor for info
                pose_map - pose map. see constructor for info

            RETURNS: hl data to pass into MASSpriteBase
            """
            
            if hl_data is None or pose_map is None:
                return None
            
            
            hl_def, hl_mapping = hl_data
            
            
            hl_keys = pose_map.unique_values()
            
            
            return (hl_keys, hl_def, hl_mapping)
        
        @staticmethod
        def get_priority(acs):
            """
            Gets the priority of the given accessory

            This is for sorting
            """
            return acs.priority
        
        def get_arm_split_code(self, poseid):
            """DEPRECATED
            NOTE: we are keeping this around for compatiblity purposes

            IN:
                poseid - ignored

            RETURNS: empty list
            """
            return []
        
        def get_rec_layer(self):
            """
            Returns the recommended layer ofr this accessory

            RETURNS:
                recommend MASMOnika accessory type for this accessory
            """
            return self._m1_sprite0x2dchart__rec_layer
        
        def opt_gethlc(self, poseid, flt, arm_split, defval=None):
            """
            Optimized highlight code getter. Implementation varies in 
            extended classes.
            The point of this is to avoid additional lookups during render.
            """
            raise NotImplementedError


    class MASAccessory(MASAccessoryBase):
        """
        Standard MASAccessory object.

        PROPERTIES:
            hl_map - MASHighlightMap containing MASFilterMap objects.

        See MASAccessoryBase for inherited properties.
        """
        
        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                rec_layer=MASMonika.PST_ACS,
                priority=10,
                stay_on_start=False,
                entry_pp=None,
                exit_pp=None,
                acs_type=None,
                mux_type=None,
                ex_props=None,
                dlg_data=None,
                keep_on_desk=False,
                hl_data=None
        ):
            """
            Constructor.

            IN:
                name - name of this accessory
                img_sit - file name of the sitting image
                pose_map - MASPoseMap object that contains pose mappings
                img_stand - file name of the standing image
                    IF this is not passed in, we assume the standing version
                        has no accessory.
                    (Default: "")
                rec_layer - recommended layer to place this accessory
                    (Must be one the ACS types in MASMonika)
                    (Default: MASMonika.PST_ACS)
                priority - render priority. Lower is rendered first
                    (Default: 10)
                stay_on_start - True means the accessory is saved for next
                    startup. False means the accessory is dropped on next
                    startup.
                    (Default: False)
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                acs_type - type, for ease of organization of acs
                    This works with mux type to determine if an ACS can work
                    with another ACS.
                    (Default: None)
                mux_type - list of acs types that should be
                    mutually exclusive with this acs.
                    this works with acs_type to determine if this works with
                    other ACS.
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: None)
                dlg_data - tuple of the following format:
                    [0] - string to use for dlg_desc
                    [1] - boolean value for dlg_plur
                    (Default: None)
                keep_on_desk - determines if ACS should be shown if monika 
                    leaves
                    (Default: False)
                hl_data - ACS highlight data. Format: tuple:
                    [0] - default MASFilterMap highlight to use
                        if None, then no default highlight
                    [1] - dict of the following format:
                        key: values used for pose_map
                        value: MASFilterMap to associate with that pose id
                            None means no highlight for the pose code
                        if None, then no mapped highlights
                    if None, then no highlights at all
                    (Default: None)
            """
            super(MASAccessory, self).__init__(
                self.ASO_REG,
                name,
                img_sit,
                pose_map,
                img_stand,
                rec_layer,
                priority,
                stay_on_start,
                entry_pp,
                exit_pp,
                acs_type,
                mux_type,
                ex_props,
                dlg_data,
                keep_on_desk,
                hl_data
            )
        
        def __repr__(self):
            return "<ACS: {0}>".format(self.name)

        def _m1_sprite0x2dchart__build_loadstrs_hl(self, prefix, poseid):
            """
            Builds highlight load strs for a pose

            IN:
                prefix - prefix to apply to the load strings
                    should be a list of strings
                poseid - pose id to find highlights for

            RETURNS: list of lists of strings
            """
            if self.hl_map is None:
                return []
            
            
            mfm = self.hl_map.get(poseid)
            if mfm is None:
                return []
            
            
            return [
                prefix + [
                    store.mas_sprites.HLITE_SUFFIX,
                    hlc,
                    store.mas_sprites.FILE_EXT
                ]
                for hlc in mfm.unique_values()
            ]
        
        def build_loadstrs(self, prefix):
            """
            See MASSpriteBase.build_loadstrs
            """
            loadstrs = []
            
            
            for poseid in self.pose_map.unique_values():
                
                new_img = prefix + [
                    store.mas_sprites.PREFIX_ACS,
                    self.img_sit,
                    store.mas_sprites.ART_DLM,
                    poseid,
                ]
                
                
                loadstrs.append(new_img + [store.mas_sprites.FILE_EXT])
                
                
                loadstrs.extend(self._m1_sprite0x2dchart__build_loadstrs_hl(new_img, poseid))
            
            return loadstrs
        
        def gethlc(self, leanpose, flt, hl_key, defval=None):
            """
            Gets highlight code.
            NOTE: if you already know the poseid, use opt_gethlc

            IN:
                leanpose - leanpose to get highlight for
                flt - filter to get highlight for
                hl_key - unused
                defval - default value to return
                    (Default: None)

            RETURNS: highlight code, or None if no highlight
            """
            return self.opt_gethlc(
                self.pose_map.get(leanpose, None),
                flt,
                None,
                defval
            )
        
        def opt_gethlc(self, poseid, flt, arm_split, defval=None):
            """
            MASAccessory-specific gethlc. 
            Optimized to only accept the args that actually matter for
            MASAccessory objects.

            IN:
                poseid - string from pose_map
                flt - fitler to get highlight for
                arm_split - unused
                defval - default value to return
                    (Default: None)

            RETURNS: highlight code, or None if no highlight
            """
            return MASHighlightMap.o_fltget(self.hl_map, poseid, flt, defval)


    class MASSplitAccessory(MASAccessoryBase):
        """
        MASSplitAccessory object. For accessories that should be placeable
        at split layers (ASE/BSE)

        PROPERTIES:
            arm_split - MASPoseMap determining which arm position the ACS 
                should be visible in. This only applies to ACS that are
                intended to be used in a BSE or ASE ACS layer. 
                This accepts the following values for poses;
                    "0" - sprite has "-0" version, and should be used for
                        arms-0 for this pose or body-0
                    "1" - sprite has "-1" version, and should be used for
                        body-1
                    "5" - sprite has "-5" version, and should be used for
                        arms-5 for this pose
                    "10" - sprite has "-10" version, and should be used for
                        arms-10
                    "" - sprite does not have any arm split for this pose
                    "*" - sprite has an arm split for all poses.
                    A ^ (caret) delimted string is also acceptable:
                        1^5^10
            hl_map - MASHighlightMap (with same keys as pose_map values) of
                MASHighlightMap objects (with same keys as arm_split values)
                of MASFilterMap objects.

        See MASAccessoryBase for inherited propeties
        """
        
        _m1_sprite0x2dchart__MHM_KEYS = ("0", "1", "5", "10")
        
        
        
        _m1_sprite0x2dchart__ASE_KEYS = ("0", "5", "10")
        _m1_sprite0x2dchart__BSE_KEYS = ("0", "1")
        
        
        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                rec_layer=MASMonika.PST_ACS,
                priority=10,
                stay_on_start=False,
                entry_pp=None,
                exit_pp=None,
                acs_type=None,
                mux_type=None,
                ex_props=None,
                arm_split=None,
                dlg_data=None,
                keep_on_desk=False,
                hl_data=None
            ):
            """
            MASSplitAccessory constructor

            IN:
                name - name of this accessory
                img_sit - file name of the sitting image
                pose_map - MASPoseMap object that contains pose mappings
                img_stand - file name of the standing image
                    IF this is not passed in, we assume the standing version
                        has no accessory.
                    (Default: "")
                rec_layer - recommended layer to place this accessory
                    (Must be one the ACS types in MASMonika)
                    (Default: MASMonika.PST_ACS)
                priority - render priority. Lower is rendered first
                    (Default: 10)
                stay_on_start - True means the accessory is saved for next
                    startup. False means the accessory is dropped on next
                    startup.
                    (Default: False)
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                acs_type - type, for ease of organization of acs
                    This works with mux type to determine if an ACS can work
                    with another ACS.
                    (Default: None)
                mux_type - list of acs types that should be
                    mutually exclusive with this acs.
                    this works with acs_type to determine if this works with
                    other ACS.
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: None)
                arm_split - MASPoseMap object for determining arm splits. See
                    property list above for more info.
                    (Default: None)
                dlg_data - tuple of the following format:
                    [0] - string to use for dlg_desc
                    [1] - boolean value for dlg_plur
                    (Default: None)
                keep_on_desk - determines if ACS should be shown if monika 
                    leaves
                    (Default: False)
                hl_data - highlight data. Format: 
                    key: values used for pose_map
                    value: tuple:
                        [0] - default highlight ot use. pass in None to not
                            set a default (MASFilterMap object)
                        [1] - highlight mapping to use. format:
                            key: see arm_split property
                            value: MASFilterMap objects
                                None means no highlight for this layer
                        None means no highlight for this pose
                    if None, then no highlights at all
                    (Default: None)
            """
            super(MASSplitAccessory, self).__init__(
                self.ASO_SPLIT,
                name,
                img_sit,
                pose_map,
                img_stand,
                rec_layer,
                priority,
                stay_on_start,
                entry_pp,
                exit_pp,
                acs_type,
                mux_type,
                ex_props,
                dlg_data,
                keep_on_desk,
                MASSplitAccessory._prepare_hl_data(hl_data)
            )
            
            self.arm_split = arm_split
        
        def __repr__(self):
            return "<SACS: {0}>".format(self.name)

        def _m1_sprite0x2dchart__build_loadstrs_hl(self, prefix, poseid, armcode):
            """
            Builds highlight load strs for a pose and arm layer

            IN:
                prefix - prefix to apply to the load strings
                    should be a list of strings
                poseid - pose id to find highlight for
                armcode - arm_split code to find highlight for

            RETURNS: list of lists of strings
            """
            if self.hl_map is None:
                return []
            
            
            mhm = self.hl_map.get(poseid)
            if mhm is None:
                return []
            
            
            mfm = mhm.get(armcode)
            if mfm is None:
                return []
            
            
            return [
                prefix + [
                    store.mas_sprites.HLITE_SUFFIX,
                    hlc,
                    store.mas_sprites.FILE_EXT
                ]
                for hlc in mfm.unique_values()
            ]
        
        @classmethod
        def _prepare_hl_data(cls, hl_data):
            """
            Generates hl-ready data from ahl data for MASAccessoryBase
                processing

            IN:
                hl_data - ahl data. See constructor for info

            RETURNS: hl_data to pass into MASAccessoryBase
            """
            if hl_data is None:
                return None
            
            
            for key in hl_data:
                data = hl_data[key]
                if data is not None:
                    hl_data[key] = MASHighlightMap.create_from_mapping(
                        cls._m1_sprite0x2dchart__MHM_KEYS,
                        data[0],
                        data[1]
                    )
            
            return (None, hl_data)
        
        def build_loadstrs(self, prefix):
            """
            See MASSpriteBase.build_loadstrs
            """
            loadstrs = []
            
            
            for poseid in self.pose_map.unique_values():
                
                
                new_img = prefix + [
                    store.mas_sprites.PREFIX_ACS,
                    self.img_sit,
                    store.mas_sprites.ART_DLM,
                    poseid,
                ]
                
                
                for armcode in self.get_arm_split_code(poseid):
                    
                    
                    ac_img = new_img + [store.mas_sprites.ART_DLM, arm_code]
                    
                    
                    loadstrs.append(ac_img + [store.mas_sprites.FILE_EXT])
                    
                    
                    loadstrs.extend(self._m1_sprite0x2dchart__build_loadstrs_hl(
                        ac_img,
                        poseid,
                        armcode
                    ))
            
            return loadstrs
        
        @classmethod
        def fromJSON_hl_data(cls,
                json_obj,
                msg_log,
                ind_lvl,
                pm_keys,
                rec_layer
        ):
            """
            Parses JSOn data for a highlight split object

            IN:
                json_obj - JSON object to parse
                ind_lvl - indentation level
                    NOTE: this function handles loading/success so do NOT
                        incrememnt indent
                pm_keys - pose map keys
                rec_layer - the layer that this ACS wants to be on

            OUT:
                msg_log - list to add messages to

            RETURNS: split hl_data, completely validated:
                dict:
                key: pose map keys
                value: tuple:
                    [0] - default MASFilterMap object
                    [1] - dict:
                        key: arm split keys
                        value: MASFilterMap object
                or None if no data, False if failure in parsing occured
            """
            
            if rec_layer == MASMonika.BSE_ACS:
                as_keys = cls._m1_sprite0x2dchart__BSE_KEYS
            elif rec_layer == MASMonika.ASE_ACS:
                as_keys = cls._m1_sprite0x2dchart__ASE_KEYS
            else:
                
                
                return None
            
            
            msg_log.append((
                store.mas_sprites_json.MSG_INFO_T,
                ind_lvl,
                store.mas_sprites_json.MHM_S_LOADING
            ))
            
            
            if not store.mas_sprites_json._verify_dict(json_obj, False):
                msg_log.append((
                    store.mas_sprites_json.MSG_ERR_T,
                    ind_lvl + 1,
                    store.mas_sprites_json.MHM_S_NOT_DICT.format(
                        dict,
                        type(json_obj)
                    )
                ))
                return False
            
            shl_data = {}
            
            
            
            has_map_data = False
            isbad = False
            for pm_key in pm_keys:
                if pm_key in json_obj:
                    hl_obj = json_obj.pop(pm_key)
                    
                    
                    msg_log.append((
                        store.mas_sprites_json.MSG_INFO_T,
                        ind_lvl + 1,
                        store.mas_sprites_json.MHM_SK_LOADING.format(pm_key)
                    ))
                    
                    
                    vhl_data = {}
                    if store.mas_sprites_json._validate_highlight_core(
                            hl_obj,
                            vhl_data,
                            msg_log,
                            ind_lvl + 2,
                            as_keys
                    ):
                        
                        
                        
                        msg_log.append((
                            store.mas_sprites_json.MSG_INFO_T,
                            ind_lvl + 1,
                            store.mas_sprites_json.MHM_SK_SUCCESS.format(
                                pm_key
                            )
                        ))
                        
                        hl_data = vhl_data.get("hl_data", None)
                        
                        if hl_data is not None:
                            
                            has_map_data = True
                        
                        shl_data[pm_key] = hl_data
                    
                    else:
                        
                        isbad = True
            
            
            for extra_prop in json_obj:
                msg_log.append((
                    store.mas_sprites_json.MSG_WARN_T,
                    ind_lvl,
                    store.mas_sprites_json.EXTRA_PROP.format(extra_prop)
                ))
            
            
            if isbad:
                return False
            
            
            if len(shl_data) == 0 or not has_map_data:
                
                msg_log.append((
                    store.mas_sprites_json.MSG_WARN_T,
                    ind_lvl,
                    store.mas_sprites_json.MHM_S_NO_DATA
                ))
                shl_data = None
            
            
            msg_log.append((
                store.mas_sprites_json.MSG_INFO_T,
                ind_lvl,
                store.mas_sprites_json.MHM_S_SUCCESS
            ))
            
            return shl_data
        
        def get_arm_split_code(self, poseid):
            """
            Gets arm split code if needed

            IN:
                poseid - poseid to get arm split code for

            RETURNS: arms split code as iterable, or empty list 
            """
            if self.arm_split is None:
                return []
            
            
            arm_code = self.arm_split.get(poseid, None)
            if not arm_code:
                return []
            
            
            if arm_code == "*":
                return self._m1_sprite0x2dchart__MHM_KEYS
            
            
            return arm_code.split("^")
        
        def gethlc(self, leanpose, flt, hl_key, defval=None):
            """
            Gets highlight code.
            NOTE: if you already know the pose id, use opt_gethlc

            IN:
                leanpose - leanpose to get highlight for
                flt - filter to get highlight for
                hl_key - arm_spilt code
                defval - default value to use
                    (Default: None)

            RETURNS: highlight code, or none if no highlight
            """
            return self.opt_gethlc(
                self.pose_map.get(leanpose, None),
                flt, 
                hl_key,
                defval
            )
        
        def hl_keys(self):
            """
            Returns keys used for MASHighlightMap.

            RETURNS: keys used for all MASHighlightMaps for MASAccessories.
            """
            return self._m1_sprite0x2dchart__MHM_KEYS
        
        @classmethod
        def hl_keys_c(cls):
            """
            Class method version of hl_keys

            RETURNS: tuple of hl keys
            """
            return cls._m1_sprite0x2dchart__MHM_KEYS
        
        def opt_gethlc(self, poseid, flt, arm_split, defval=None):
            """
            MASSplitAccessory-specific gethlc.
            Optimized to only accept the args that actually matter for
            MASSplitAccessory objects

            IN:
                poseid - string from pose_map
                flt - filter to get highlight for
                arm_split - arm split code to get highlight for
                defval - default value to return
                    (Default: None)

            RETURNS: highlight code, or None if no highlight
            """
            if self.hl_map is None or arm_split is None:
                return defval
            
            return MASHighlightMap.o_fltget(
                self.hl_map.get(poseid),
                arm_split,
                flt,
                defval
            )
        
        @classmethod
        def verify_arm_split_val(cls, value):
            """
            Verifies if an arm split value is valid

            IN:
                value - arm split value to check

            RETURNS: True if valid, false if not
            """
            return value in cls._m1_sprite0x2dchart__MHM_KEYS


    class MASHair(MASSpriteFallbackBase):
        """
        MASHair objects

        Representations of hair items

        PROPERTIES:
            split - MASPoseMap object that determins if a pose has split hair
                or not.
                if a pose has True, it is split. False or None means no split.
            hl_map - MASHighlightMap with the following format:
                keys:
                    "front" - front hair
                    "back" - back hair
                    "<lean>|front" - front hair for a leaning type
                        NOTE: can be multiple of this format
                    "<lean>|back" - back hair for a leaning type
                        NOTE: can be multiple of this format
                values:
                    MASFilterMap objects

        SEE MASSpriteFallbackBase for inherited properties

        POSEMAP explanations:
            Use an empty string to
        """
        
        _m1_sprite0x2dchart__MHM_KEYS = store.mas_sprites._genLK(("front", "back"))
        
        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                stay_on_start=True,
                fallback=False,
                entry_pp=None,
                exit_pp=None,
                split=None,
                ex_props=None,
                hl_data=None
            ):
            """
            MASHair constructor

            IN;
                name - name of this hairstyle
                img_sit - filename of the sitting image for this hairstyle
                pose_map - MASPoseMap object that contains pose mappings
                img_stand - filename of the standing image for this hairstyle
                    If this is not passed in, this is considered blacklisted
                        from standing sprites.
                    (Default: "")
                stay_on_strat - True means the hairstyle should reappear on
                    startup. False means a restart clears the hairstyle
                    (Default: True)
                fallback - Unused
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                split - MASPoseMap object saying which hair has splits or Not.
                    If None, we assume hair has splits for everything.
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: None)
                hl_data - tuple of the following format:
                    [0] - default MASFilterMap to use.
                        NOTE: it almost certain that you do NOT want to set
                            this
                        If None, no default highlight
                    [1] - mapping dict. Format:
                        key: see hl_map property
                        value: MASFilterMap object, or None if no highlight
                    if None, then no highlights at all.
                    (Default: None)
            """
            super(MASHair, self).__init__(
                name,
                img_sit,
                pose_map,
                img_stand,
                stay_on_start,
                fallback,
                entry_pp,
                exit_pp,
                ex_props,
                MASHair._prepare_hl_data(hl_data)
            )
            self._m1_sprite0x2dchart__sp_type = store.mas_sprites_json.SP_HAIR
            
            if split is not None and type(split) != MASPoseMap:
                raise Exception("split MUST be PoseMap")
            
            self.split = split
        
        def __repr__(self):
            return "<Hair: {0}>".format(self.name)

        def _m1_sprite0x2dchart__build_loadstrs_hl(self, prefix, hl_key):
            """
            Builds highlight load strs for a split layer

            IN:
                prefix - prefix to apply to the load strings
                    should be a list of strings
                hl_key - key of the hl to use
                
            RETURNS: list of lists of strings
            """
            if self.hl_map is None:
                return []
            
            
            mfm = self.hl_map.get(hl_key)
            if mfm is None:
                return []
            
            return [
                prefix + [
                    store.mas_sprites.HLITE_SUFFIX,
                    hlc,
                    store.mas_sprites.FILE_EXT
                ]
                for hlc in mfm.unique_values()
            ]
        
        @classmethod
        def _prepare_hl_data(cls, hl_data):
            """
            Generates hl-ready data for MASSpriteBase

            IN:
                hl_data - hl data. See Constructor for info

            RETURNS: hl_data to pass into MASSpriteBase
            """
            if hl_data is None:
                return None
            
            hl_def, hl_mapping = hl_data
            if hl_def is None and hl_mapping is None:
                return None
            
            return (cls._m1_sprite0x2dchart__MHM_KEYS, hl_def, hl_mapping)
        
        def build_loadstrs(self, prefix):
            """
            See MASSpriteBase.build_loadstrs
            """
            loadstrs = []
            
            
            
            all_split = self.split is None
            
            
            for leanpose in store.mas_sprites.ALL_POSES:
                
                
                actual_pose = self.get_leanpose(leanpose)
                
                
                
                if (
                        actual_pose
                        and (all_split or self.split.get(actual_pose, False))
                ):
                    
                    islean = "|" in leanpose
                    
                    
                    new_img = list(prefix)
                    
                    
                    if islean:
                        lean = leanpose.partition("|")[0]
                        hl_key = lean + "|{0}"
                        new_img.extend((
                            store.mas_sprites.PREFIX_HAIR_LEAN,
                            lean,
                            store.mas_sprites.ART_DLM
                        ))
                    else:
                        hl_key = "{0}"
                        new_img.append(store.mas_sprites.PREFIX_HAIR)
                    
                    
                    new_img.append(self.img_sit)
                    
                    
                    back_img = new_img + [store.mas_sprites.BHAIR_SUFFIX]
                    front_img = new_img + [store.mas_sprites.FHAIR_SUFFIX]
                    
                    
                    loadstrs.append(back_img + [store.mas_sprites.FILE_EXT])
                    loadstrs.append(front_img + [store.mas_sprites.FILE_EXT])
                    
                    
                    loadstrs.extend(self._m1_sprite0x2dchart__build_loadstrs_hl(
                        back_img,
                        hl_key.format(store.mas_sprites.BHAIR)
                    ))
                    loadstrs.extend(self._m1_sprite0x2dchart__build_loadstrs_hl(
                        front_img,
                        hl_key.format(store.mas_sprites.FHAIR)
                    ))
            
            return loadstrs
        
        def gethlc(self, hair_key, lean, flt, defval=None):
            """
            Gets highlight code

            IN:
                hair_key - the hair key to get hlc for (front/back)
                lean - type of lean to get hlc for
                flt - filter to get highlight for
                defval - the default value to return
                    (Default: None)

            RETURNS: highlight code, or defval if no highlight
            """
            if self.hl_map is None:
                return defval
            
            if lean:
                hl_key = "|".join((lean, hair_key))
            else:
                hl_key = hair_key
            
            return MASHighlightMap.o_fltget(
                self.hl_map,
                hl_key,
                flt,
                defval
            )
        
        def hl_keys(self):
            """
            Returns keys used for MASHighlightMap.

            RETURNS: keys used for all MASHighlightMaps for MASHair objects
            """
            return self._m1_sprite0x2dchart__MHM_KEYS
        
        @classmethod
        def hl_keys_c(cls):
            """
            Class method of hl_keys

            RETURNS: tuple of hl keys
            """
            return cls._m1_sprite0x2dchart__MHM_KEYS


    class MASClothes(MASSpriteFallbackBase):
        """
        MASClothes objects

        Representations of clothes

        PROPERTIES:
            hair_map - dict of available hair styles for these clothes
                keys should be hair name properites. Values should also be
                hair name properties.
                use "all" to signify a default hair style for all mappings that
                are not found.
            pose_arms - MASPoseArms object containing the arms for these
                clothes.
            hl_map - MASHighlightMap with the following format:
                keys:
                    "0" - body-0 layer
                    "1" - body-1 layer
                    "<lean>|0" - body-0 layer for a leaning type
                        NOTE: can be multiple of this format
                    "<lean>|1" - body-1 layer for a leaning type
                        NOTE: can be multiple of this format
                values:
                    MASFilterMap objects

        SEE MASSpriteFallbackBase for inherited properties
        """
        import store.mas_sprites as mas_sprites
        
        _m1_sprite0x2dchart__MHM_KEYS = store.mas_sprites._genLK(("0", "1"))
        
        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                stay_on_start=False,
                fallback=False,
                hair_map={},
                entry_pp=None,
                exit_pp=None,
                ex_props=None,
                pose_arms=None,
                hl_data=None
            ):
            """
            MASClothes constructor

            IN;
                name - name of these clothes
                img_sit - filename of the sitting image for these clothes
                pose_map - MASPoseMap object that contains pose mappings
                img_stand - filename of the standing image for these clothes
                    If this is not passed in, this is considered blacklisted
                        from standing sprites.
                    (Default: "")
                stay_on_start - True means the clothes should reappear on
                    startup. False means a restart clears the clothes
                    (Default: False)
                fallback - Unused
                hair_map - dict of available hair styles and what they map to
                    These should all be strings. To signify a default, add
                    a single item called "all" with the value being the hair
                    to map to.
                    NOTE: use the name property for hairstyles.
                    (Default: {})
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: None)
                pose_arms - MASPoseMap object represneting the arm layers
                    for poses. If None is passed, we assume use the base
                    layers as a guide
                    (Default: None)
                hl_data - tuple of the following format:
                    [0] - default MASFilterMap to use.
                        NOTE: it almost certain that you do NOT want to set
                            this
                        If None, no default highlight
                    [1] - mapping dict. Format:
                        key: see hl_map proprety
                        value: MASFilterMap object, or None if no highlight
                    if None, then no highlights at all.
                    (Default: None)
            """
            super(MASClothes, self).__init__(
                name,
                img_sit,
                pose_map,
                img_stand,
                stay_on_start,
                fallback,
                entry_pp,
                exit_pp,
                ex_props,
                MASClothes._prepare_hl_data(hl_data)
            )
            self._m1_sprite0x2dchart__sp_type = store.mas_sprites_json.SP_CLOTHES
            
            self.hair_map = hair_map
            self.pose_arms = pose_arms
            
            
            if "all" in hair_map:
                for hair_name in mas_sprites.HAIR_MAP:
                    if hair_name not in self.hair_map:
                        self.hair_map[hair_name] = self.hair_map["all"]
        
        def __repr__(self):
            return "<Clothes: {0}>".format(self.name)
        
        def _m1_sprite0x2dchart__build_loadstrs_hl(self, prefix, hl_key):
            """
            Builds loadstrs for body highlights

            IN:
                prefix - prefix to apply
                    should be a list of strings
                hl_key - key of the hl to use

            RETURNS: list of lists of strings representing image paths
            """
            if self.hl_map is None:
                return []
            
            
            mfm = self.hl_map.get(hl_key)
            if mfm is None:
                return []
            
            return [
                prefix + [
                    store.mas_sprites.HLITE_SUFFIX,
                    hlc,
                    store.mas_sprites.FILE_EXT
                ]
                for hlc in mfm.unique_values()
            ]
        
        @classmethod
        def _prepare_hl_data(cls, hl_data):
            """
            Generates hl-ready data for MASSpriteBase

            IN:
                hl_data - hl data. See constructor for info

            RETURNS: hl_data to pass into MASSpriteBase
            """
            if hl_data is None:
                return None
            
            hl_def, hl_mapping = hl_data
            if hl_def is None and hl_mapping is None:
                return None
            
            return (cls._m1_sprite0x2dchart__MHM_KEYS, hl_def, hl_mapping)
        
        def build_loadstrs(self, prefix):
            """
            See MASSpriteBase.build_loadstrs
            """
            loadstrs = []
            
            
            c_prefix = prefix + [
                self.img_sit,
                "/"
            ]
            
            
            
            
            
            loadstrs.append(c_prefix + [
                store.mas_sprites.NEW_BODY_STR,
                store.mas_sprites.ART_DLM,
                "0",
                store.mas_sprites.FILE_EXT
            ])
            loadstrs.append(c_prefix + [
                store.mas_sprites.NEW_BODY_STR,
                store.mas_sprites.ART_DLM,
                "1",
                store.mas_sprites.FILE_EXT
            ])
            
            
            for lpose in store.mas_sprites.L_POSES:
                
                
                actual_pose = self.get_leanpose(lpose)
                
                
                if actual_pose and "|" in actual_pose:
                    
                    lean, pose = actual_pose.split("|")
                    
                    
                    l_prefix = c_prefix + [
                        store.mas_sprites.PREFIX_BODY_LEAN,
                        lean,
                        store.mas_sprites.ART_DLM
                    ]
                    l0_prefix = l_prefix + ["0"]
                    l1_prefix = l_prefix + ["1"]
                    loadstrs.append(l0_prefix + [store.mas_sprites.FILE_EXT])
                    loadstrs.append(l1_prefix + [store.mas_sprites.FILE_EXT])
                    
                    
                    loadstrs.extend(self._m1_sprite0x2dchart__build_loadstrs_hl(
                        l0_prefix,
                        lean + "|0"
                    ))
                    loadstrs.extend(self._m1_sprite0x2dchart__build_loadstrs_hl(
                        l1_prefix,
                        lean + "|1"
                    ))
            
            
            if self.pose_arms is None:
                
                pose_arms = store.mas_sprites.base_arms
            else:
                pose_arms = self.pose_arms
            
            loadstrs.extend(pose_arms.build_loadstrs(c_prefix))
            
            return loadstrs
        
        def determine_arms(self, leanpose):
            """
            Determines arms pose to use for a given leanpose

            IN:
                leanpose - leanpose to determine arms pose for

            RETURNS: MASPoseArms object to use for this leanpose, or None if
                no MASPoseArms to use
            """
            
            
            if self.pose_arms is None:
                return store.mas_sprites.base_pose_arms_map.get(
                    leanpose,
                    None
                )
            
            
            return self.pose_arms.get(leanpose, None)
        
        def get_hair(self, hair):
            """
            Given a hair type, grabs the available mapping for this hair type

            IN:
                hair - hair type to get mapping for

            RETURNS:
                the hair mapping to use inplace for the given hair type
            """
            return self.hair_map.get(hair, self.hair_map.get("all", hair))
        
        def gethlc(self, bcode, lean, flt, defval=None):
            """
            Gets highlight code

            IN:
                bcode - base code to get hlc for (0,1)
                lean - type of lean
                flt - filter to get highlight for
                defval - the default value to return
                    (Default: None)

            RETURNS: highlight code, or defval is no highlight
            """
            if self.hl_map is None:
                return defval
            
            if lean:
                hl_key = "|".join((lean, bcode))
            else:
                hl_key = bcode
            
            return MASHighlightMap.o_fltget(
                self.hl_map,
                hl_key,
                flt,
                defval
            )
        
        def has_hair_map(self):
            """
            RETURNS: True if we have a mapping to check, False otherwise
            """
            return len(self.hair_map) > 0
        
        def hl_keys(self):
            """
            Returns keys used for MASHighlightMap.

            RETURNS: keys used for all MASHighlightMaps for MASHair objects
            """
            return self._m1_sprite0x2dchart__MHM_KEYS
        
        @classmethod
        def hl_keys_c(cls):
            """
            Class method version of hl_keys

            RETURNS: tuple of hl keys
            """
            return cls._m1_sprite0x2dchart__MHM_KEYS
        
        @staticmethod
        def by_exprop(exprop, value=True):
            """
            Gets all clothes that have the given exprop.

            IN:
                exprop - exprop to look for
                value - value the exprop should be. Set to None to ignore.

            RETURNS: list of MASClothes objects with the given exprop and value
            """
            clothes = []
            
            for c_name in store.mas_sprites.CLOTH_MAP:
                clothing = store.mas_sprites.CLOTH_MAP[c_name]
                if (
                        clothing.hasprop(exprop)
                        and (
                            value is None
                            or value == clothing.getprop(exprop)
                        )
                ):
                    clothes.append(clothing)
            
            return clothes



    def mas_drawmonika(
            st,
            at,
            character,

            
            eyebrows,
            eyes,
            nose,
            mouth,

            
            lean=None,
            arms="steepling",
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None,

            
            head="",
            left="",
            right="",
            stock=True,
            single=None
        ):
        """DEPRECATED
        This function has been gutted and only draws standing

        IN:
            st - renpy related
            at - renpy related
            character - MASMonika character object
            eyebrows - type of eyebrows (sitting)
            eyes - type of eyes (sitting)
            nose - type of nose (sitting)
            mouth - type of mouth (sitting)
            head - type of head (standing)
            left - type of left side (standing)
            right - type of right side (standing)
            lean - type of lean (sitting)
                (Default: None)
            arms - type of arms (sitting)
                (Default: "steepling")
            eyebags - type of eyebags (sitting)
                (Default: None)
            sweat - type of sweatdrop (sitting)
                (Default: None)
            blush - type of blush (sitting)
                (Default: None)
            tears - type of tears (sitting)
                (Default: None)
            emote - type of emote (sitting)
                (Default: None)
            stock - True means we are using stock standing, False means not
                (standing)
                (Default: True)
            single - type of single standing image (standing)
                (Default: None)
        """
        
        
        
        
        
        
        cmd = store.mas_sprites._ms_standingstock(
            head,
            left,
            right,
            [], 
            single=single
        )
        
        
        return eval(cmd),None 


init -2 python in mas_sprites:




    NUM_MARMS = {
        1: store.MASArmBoth,
        2: store.MASArmLeft,
        3: store.MASArmLeft,
        4: store.MASArmRight,
        5: store.MASArmRight,
        6: store.MASArmRight,
        7: store.MASArmBoth,
        8: store.MASArmLeft,
        9: store.MASArmRight,
    }


    base_arms = store.MASPoseArms({
        
        
        1: NUM_MARMS[1](
            "crossed",
            {
                store.MASArm.LAYER_MID: True,
                store.MASArm.LAYER_TOP: True,
            }
        ),

        
        2: NUM_MARMS[2](
            "down",
            {
                store.MASArm.LAYER_BOT: True,
            }
        ),

        
        3: NUM_MARMS[3](
            "rest",
            {
                store.MASArm.LAYER_TOP: True,
            }
        ),

        
        4: NUM_MARMS[4](
            "down",
            {
                store.MASArm.LAYER_BOT: True,
            }
        ),

        
        5: NUM_MARMS[5](
            "point",
            {
                store.MASArm.LAYER_BOT: True,
            }
        ),

        
        6: NUM_MARMS[6](
            "restpoint",
            {
                store.MASArm.LAYER_TOP: True,
            }
        ),

        
        7: NUM_MARMS[7](
            "steepling",
            {
                store.MASArm.LAYER_TOP: True,
            }
        ),

        
        8: NUM_MARMS[8](
            "def",
            {
                store.MASArm.LAYER_TOP: True,
            }
        ),

        
        9: NUM_MARMS[9](
            "def",
            {
                store.MASArm.LAYER_MID: True,
                store.MASArm.LAYER_TOP: True,
            }
        ),
    })


    base_mpm = store.MASPoseMap(

        
        p1=(7,),

        
        p2=(1,),

        
        p3=(3, 6),

        
        p4=(2, 5),

        
        p5=(8, 9),

        
        p6=(2, 4),

        
        p7=(2, 6)

    )


    def use_bma(arm_id):
        """
        Returns base MASArm for an armid

        IN:
            arm_id - numerical digit for an arm. Corresponds to NUM_ARMS

        RETURNS: base MASArm for this arm, or None if no Arm
        """
        return base_arms.get(arm_id)

    def use_bmpm(posenum):
        """
        Returns tuple of MASArms for a pose num
        
        IN:
            posenum - numerical digit for a pose. This corresponds to
                NUM_POSE.

        RETURNS: base MASArms for this poes, or None if no arms
        """
        return use_bpam_s(NUM_POSE.get(posenum, None))


    def use_bmpm_s(leanpose):
        """
        Version of use_bpam that uses leanpose

        IN:
            leanpose - leanpose string

        RETURNS: base MASArms for this pose, or None if no arms
        """
        return base_mpm.get(leanpose, None)


init -1 python in mas_sprites:


    def show_empty_desk():
        """
        shows empty desk
        """
        renpy.show(
            "emptydesk",
            tag="emptydesk",
            at_list=[store.i11],
            zorder=store.MAS_MONIKA_Z - 1
        )


define monika_chr = MASMonika()


image emptydesk = DynamicDisplayable(
    mas_drawemptydesk_rk,
    character=monika_chr
)


















































































image monika 6ATL_cryleftright:
    block:


        block:
            choice:
                "monika 6lktsc"
            choice:
                "monika 6rktsc"
        block:


            choice:
                0.9
            choice:
                1.0
            choice:
                0.5
            choice:
                0.7
            choice:
                0.8

        repeat



image monika 6ATL_lookleftright:


    block:
        choice:
            "monika 6rkc"
        choice:
            "monika 6lkc"
    block:


        choice:
            5.0
        choice:
            6.0
        choice:
            7.0
        choice:
            8.0
        choice:
            9.0
        choice:
            10.0
    repeat





image monika ATL_0_to_upset:


    "monika 2esc"
    5.0
    block:



        block:
            choice 0.95:
                "monika 2esc"
            choice 0.05:
                "monika 5tsc"
        block:


            choice:
                10.0
            choice:
                12.0
            choice:
                14.0
            choice:
                16.0
            choice:
                18.0
            choice:
                20.0

        repeat


image monika ATL_affectionate:

    block:
        choice 0.02:
            "monika 1eua"
            1.0
            choice:
                "monika 1sua"
                4.0
            choice:
                "monika 1kua"
                1.5
            "monika 1eua"
        choice 0.98:

            choice 0.94898:
                "monika 1eua"
            choice 0.051020:
                "monika 1hua"
    block:


        choice:
            20.0
        choice:
            22.0
        choice:
            24.0
        choice:
            26.0
        choice:
            28.0
        choice:
            30.0

    repeat


image monika ATL_enamored:


    "monika 1eua"
    5.0
    block:



        block:
            choice 0.02:
                "monika 1eua"
                1.0
                choice:
                    "monika 1sua"
                    4.0
                choice:
                    "monika 1kua"
                    1.5
                "monika 1eua"
            choice 0.98:

                choice 0.765306:
                    "monika 1eua"
                choice 0.112245:
                    "monika 5esu"
                choice 0.061224:
                    "monika 5tsu"
                choice 0.061224:
                    "monika 1huu"
        block:


            choice:
                20.0
            choice:
                22.0
            choice:
                24.0
            choice:
                26.0
            choice:
                28.0
            choice:
                30.0

        repeat


image monika ATL_love:


    "monika 1eua"
    5.0
    block:



        block:
            choice 0.02:
                "monika 1eua"
                1.0
                choice:
                    "monika 1sua"
                    4.0
                choice:
                    "monika 1kua"
                    1.5
                "monika 1eua"
            choice 0.98:

                choice 0.510104:
                    "monika 1eua"
                choice 0.255102:
                    "monika 5esu"
                choice 0.091837:
                    "monika 5tsu"
                choice 0.091837:
                    "monika 1huu"
                choice 0.051020:
                    "monika 5eubla"
        block:


            choice:
                20.0
            choice:
                22.0
            choice:
                24.0
            choice:
                26.0
            choice:
                28.0
            choice:
                30.0

        repeat


image monika ATL_love_too_norm_plus:
    block:
        choice:
            "monika 1hua"
        choice:
            "monika 1huu"
        choice:
            "monika 1ekbsu"
        choice:
            "monika 1ekbsa"
        choice:
            "monika 1dkbsu"
        choice:
            "monika 1dubsu"
        choice:
            "monika 1dkbsa"
        choice:
            "monika 5ekbsa"
        choice:
            "monika 5esu"
        choice:
            "monika 5eka"


image monika ATL_love_too_enam_plus:
    block:
        choice 0.05:
            "monika 1sua"
        choice 0.05:
            "monika 1subsa"
        choice 0.10:
            "monika 1hua"
        choice 0.10:
            "monika 1huu"
        choice 0.10:
            "monika 1ekbsu"
        choice 0.10:
            "monika 1ekbsa"
        choice 0.10:
            "monika 1dkbsu"
        choice 0.10:
            "monika 1dubsu"
        choice 0.10:
            "monika 1dkbsa"
        choice 0.10:
            "monika 5ekbsa"
        choice 0.10:
            "monika 5esu"



image monika idle = ConditionSwitch(
    "mas_isMoniBroken(lower=True)", "monika 6ckc",
    "mas_isMoniDis()", "monika 6ATL_lookleftright",


    "mas_isBelowZero()", "monika ATL_0_to_upset",
    "mas_isMoniHappy()", "monika 1eua",
    "mas_isMoniAff()", "monika ATL_affectionate",
    "mas_isMoniEnamored()", "monika ATL_enamored",
    "mas_isMoniLove()", "monika ATL_love",
    "True", "monika 1esa",
    predict_all=True
)




image chibika smile = "gui/poemgame/m_sticker_1.png"
image chibika sad = "mod_assets/other/m_sticker_sad.png"
image chibika 3 = "gui/poemgame/m_sticker_2.png"


image ghost_monika:
    "mod_assets/other/ghost_monika.png"
    zoom 1.25






label mas_transition_to_emptydesk:
    $ store.mas_sprites.show_empty_desk()
    hide monika with dissolve_monika
    return





label mas_transition_from_emptydesk(exp="monika 1eua"):
    $ renpy.show(exp, tag="monika", at_list=[i11], zorder=MAS_MONIKA_Z)
    $ renpy.with_statement(dissolve)
    hide emptydesk
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
